#!/usr/bin/env python3
"""
SEO Dashboard — Alpesdata
Vérifie l'état SEO de tous les sites Alpesdata et génère un rapport HTML.

Usage:
  python3 check.py [--serve]    # Génère le dashboard
  python3 check.py --update     # Met à jour et déploie sur le site
"""

import os
import sys
import ssl
import json
import socket
import urllib.request
import urllib.error
import datetime
import textwrap
import re
from typing import Optional
from html import escape

# ── Configuration ──────────────────────────────────────
SITES = [
    {
        "name": "Alpesdata",
        "url": "https://alpesdata.com",
        "category": "Agence",
    },
    {
        "name": "Ma Thérapie",
        "url": "https://ma-therapie.fr",
        "category": "Santé",
    },
    {
        "name": "Cavalo",
        "url": "https://cavalo.app",
        "category": "App",
    },
]

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
HTML_FILE = os.path.join(OUTPUT_DIR, "index.html")
JSON_FILE = os.path.join(OUTPUT_DIR, "data.json")
DASHBOARD_TARGET = "/var/www/alpesdata/seo-dashboard/"  # VPS path

UA = "Mozilla/5.0 (compatible; Alpesdata-SEO-Bot/1.0)"


# ── Checkers ──────────────────────────────────────────────

def check_http(url: str) -> dict:
    """Check HTTP status, response time, server headers."""
    result = {"status": None, "response_time_ms": None, "server": None, "error": None}
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        start = datetime.datetime.now()
        with urllib.request.urlopen(req, timeout=15) as resp:
            elapsed = (datetime.datetime.now() - start).total_seconds() * 1000
            result["status"] = resp.status
            result["response_time_ms"] = round(elapsed, 1)
            result["server"] = resp.headers.get("Server", "N/A")
            result["content_type"] = resp.headers.get("Content-Type", "N/A")
    except urllib.error.HTTPError as e:
        result["status"] = e.code
        result["error"] = str(e)
    except Exception as e:
        result["error"] = str(e)
    return result


def check_ssl(hostname: str) -> dict:
    """Check SSL certificate validity."""
    result = {"valid": False, "issuer": None, "expiry": None, "days_left": None, "error": None}
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=10) as sock:
            with ctx.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                if cert:
                    result["valid"] = True
                    # Issuer — try various formats
                    issuer = cert.get("issuer", [])
                    if isinstance(issuer, tuple):
                        for pair in issuer:
                            if isinstance(pair, tuple) and len(pair) > 0:
                                for attr in pair:
                                    if isinstance(attr, tuple) and len(attr) >= 2:
                                        if attr[0] == "organizationName":
                                            result["issuer"] = attr[1]
                    if not result["issuer"]:
                        # Try parsing raw
                        result["issuer"] = str(issuer)[:80]
                    not_after = cert.get("notAfter", "")
                    if not_after:
                        result["expiry"] = not_after
                        try:
                            expiry_date = datetime.datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
                            days_left = (expiry_date - datetime.datetime.now()).days
                            result["days_left"] = days_left
                        except ValueError:
                            result["days_left"] = "?"
    except Exception as e:
        result["error"] = str(e)
    return result


def check_seo(url: str) -> dict:
    """Basic on-page SEO check: title, meta description, H1, canonical, robots."""
    result = {
        "title": None, "title_len": None,
        "meta_description": None, "meta_description_len": None,
        "h1": None, "h1_count": 0,
        "canonical": None,
        "has_robots": False,
        "og_title": None, "og_description": None,
        "error": None,
    }
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode("utf-8", errors="replace")

        # Title
        m = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
        if m:
            result["title"] = m.group(1).strip()
            result["title_len"] = len(result["title"])

        # Meta description
        m = re.search(r'<meta\s+[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']', html, re.IGNORECASE)
        if not m:
            m = re.search(r'<meta\s+[^>]*content=["\']([^"\']*)["\']\s+[^>]*name=["\']description["\']', html, re.IGNORECASE)
        if m:
            result["meta_description"] = m.group(1).strip()
            result["meta_description_len"] = len(result["meta_description"])

        # H1
        h1_matches = re.findall(r'<h1[^>]*>(.*?)</h1>', html, re.IGNORECASE | re.DOTALL)
        result["h1_count"] = len(h1_matches)
        if h1_matches:
            result["h1"] = h1_matches[0].strip()[:150]

        # Canonical
        m = re.search(r'<link\s+[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']*)["\']', html, re.IGNORECASE)
        if m:
            result["canonical"] = m.group(1)

        # Robots meta
        if re.search(r'<meta\s+[^>]*name=["\']robots["\']', html, re.IGNORECASE):
            result["has_robots"] = True

        # OG tags
        m = re.search(r'<meta\s+[^>]*property=["\']og:title["\'][^>]*content=["\']([^"\']*)["\']', html, re.IGNORECASE)
        if not m:
            m = re.search(r'<meta\s+[^>]*content=["\']([^"\']*)["\']\s+[^>]*property=["\']og:title["\']', html, re.IGNORECASE)
        if m:
            result["og_title"] = m.group(1)

        m = re.search(r'<meta\s+[^>]*property=["\']og:description["\'][^>]*content=["\']([^"\']*)["\']', html, re.IGNORECASE)
        if not m:
            m = re.search(r'<meta\s+[^>]*content=["\']([^"\']*)["\']\s+[^>]*property=["\']og:description["\']', html, re.IGNORECASE)
        if m:
            result["og_description"] = m.group(1)

    except Exception as e:
        result["error"] = str(e)
    return result


# ── HTML Generator ─────────────────────────────────────

def generate_html(results: list) -> str:
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y à %H:%M")

    cards_html = ""
    for r in results:
        site = r["site"]
        http = r["http"]
        ssl_data = r["ssl"]
        seo_data = r["seo"]

        # Status badge
        status_ok = http["status"] == 200
        status_badge = f'<span class="badge badge-ok">✓ {http["status"]}</span>' if status_ok else f'<span class="badge badge-error">✗ {http["status"]}</span>'

        # Response time color
        rt = http["response_time_ms"]
        if rt is None:
            rt_color = "text-error"
            rt_display = "N/A"
        elif rt < 500:
            rt_color = "text-ok"
            rt_display = f"{rt} ms"
        elif rt < 1500:
            rt_color = "text-warn"
            rt_display = f"{rt} ms"
        else:
            rt_color = "text-error"
            rt_display = f"{rt} ms"

        # SSL status
        ssl_days = ssl_data.get("days_left")
        if ssl_days is None:
            ssl_badge = f'<span class="badge badge-error">✗ {ssl_data.get("error", "N/A")}</span>'
        elif ssl_days < 0:
            ssl_badge = f'<span class="badge badge-error">✗ Expiré</span>'
        elif ssl_days < 14:
            ssl_badge = f'<span class="badge badge-warn">⚠ {ssl_days} jours</span>'
        elif ssl_days < 60:
            ssl_badge = f'<span class="badge badge-ok">✓ {ssl_days} jours</span>'
        else:
            ssl_badge = f'<span class="badge badge-ok">✓ {ssl_days} jours</span>'

        # SEO checks
        seo_issues = []
        if seo_data.get("title"):
            seo_issues.append(f'✅ Title ({seo_data["title_len"]} car.)')
        else:
            seo_issues.append('❌ Title manquant')

        if seo_data.get("meta_description"):
            seo_issues.append(f'✅ Meta desc. ({seo_data["meta_description_len"]} car.)')
        else:
            seo_issues.append('❌ Meta description manquante')

        if seo_data.get("h1_count") == 1:
            seo_issues.append(f'✅ 1 balise H1')
        elif seo_data.get("h1_count") == 0:
            seo_issues.append('❌ Aucune balise H1')
        else:
            seo_issues.append(f'⚠ {seo_data["h1_count"]} balises H1')

        if seo_data.get("canonical"):
            seo_issues.append(f'✅ Canonical présente')
        else:
            seo_issues.append('❌ Canonical manquante')

        if seo_data.get("og_title"):
            seo_issues.append(f'✅ OG tags présentes')
        else:
            seo_issues.append('⚠ OG tags absentes')

        seo_score = sum(1 for s in seo_issues if s.startswith('✅'))
        seo_total = len(seo_issues)

        seo_bar_pct = round(seo_score / seo_total * 100) if seo_total > 0 else 0

        cards_html += f"""
        <div class="site-card">
            <div class="site-header">
                <div class="site-info">
                    <h2><a href="{escape(site['url'])}" target="_blank" rel="noopener">{escape(site['name'])}</a></h2>
                    <span class="site-url">{escape(site['url'])}</span>
                    <span class="site-category">{escape(site.get('category', ''))}</span>
                </div>
                <div class="site-status">{status_badge}</div>
            </div>

            <div class="metrics-grid">
                <div class="metric">
                    <div class="metric-label">Temps réponse</div>
                    <div class="metric-value {rt_color}">{rt_display}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Serveur</div>
                    <div class="metric-value">{escape(http.get('server', 'N/A'))}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">SSL</div>
                    <div class="metric-value">{ssl_badge}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">SEO score</div>
                    <div class="metric-value">{seo_score}/{seo_total}</div>
                    <div class="progress-bar"><div class="progress-fill" style="width:{seo_bar_pct}%"></div></div>
                </div>
            </div>

            <div class="seo-details">
                <div class="seo-row"><span class="seo-label">Title</span><span class="seo-value">{escape(seo_data.get('title') or '—')}</span></div>
                <div class="seo-row"><span class="seo-label">Meta desc.</span><span class="seo-value">{escape((seo_data.get('meta_description') or '—')[:200])}</span></div>
                <div class="seo-row"><span class="seo-label">H1</span><span class="seo-value">{escape(seo_data.get('h1') or '—')}</span></div>
                <div class="seo-row"><span class="seo-label">Canonical</span><span class="seo-value">{escape(seo_data.get('canonical') or '—')}</span></div>
            </div>
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SEO Dashboard — Alpesdata</title>
<meta name="robots" content="noindex, nofollow">
<style>
:root {{
  --bg: #0f172a;
  --card: #1e293b;
  --border: #334155;
  --text: #f1f5f9;
  --text-muted: #94a3b8;
  --green: #22c55e;
  --yellow: #eab308;
  --red: #ef4444;
  --blue: #3b82f6;
  --radius: 12px;
}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:var(--bg);color:var(--text);padding:24px;line-height:1.5}}
.dashboard{{max-width:1100px;margin:0 auto}}
.header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:32px;flex-wrap:wrap;gap:12px}}
.header h1{{font-size:1.5rem;font-weight:700;display:flex;align-items:center;gap:8px}}
.header .timestamp{{color:var(--text-muted);font-size:0.85rem}}
.header .count{{background:var(--card);padding:6px 16px;border-radius:20px;font-size:0.85rem;border:1px solid var(--border)}}
.sites-grid{{display:grid;gap:20px}}
.site-card{{background:var(--card);border-radius:var(--radius);padding:24px;border:1px solid var(--border);transition:border-color .2s}}
.site-card:hover{{border-color:var(--blue)}}
.site-header{{display:flex;justify-content:space-between;align-items:start;margin-bottom:16px;flex-wrap:wrap;gap:8px}}
.site-info h2{{font-size:1.15rem;font-weight:600}}
.site-info h2 a{{color:var(--text);text-decoration:none}}
.site-info h2 a:hover{{color:var(--blue)}}
.site-url{{display:block;font-size:0.8rem;color:var(--text-muted);margin-top:2px}}
.site-category{{display:inline-block;font-size:0.7rem;background:var(--bg);padding:2px 10px;border-radius:10px;margin-top:4px;color:var(--text-muted)}}
.badge{{padding:4px 12px;border-radius:20px;font-size:0.8rem;font-weight:600;white-space:nowrap}}
.badge-ok{{background:rgba(34,197,94,0.15);color:var(--green)}}
.badge-warn{{background:rgba(234,179,8,0.15);color:var(--yellow)}}
.badge-error{{background:rgba(239,68,68,0.15);color:var(--red)}}
.metrics-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-bottom:16px}}
.metric{{background:var(--bg);border-radius:8px;padding:12px}}
.metric-label{{font-size:0.75rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:.5px;margin-bottom:4px}}
.metric-value{{font-size:1rem;font-weight:600}}
.text-ok{{color:var(--green)}}
.text-warn{{color:var(--yellow)}}
.text-error{{color:var(--red)}}
.progress-bar{{height:4px;background:var(--border);border-radius:2px;margin-top:6px;overflow:hidden}}
.progress-fill{{height:100%;background:var(--green);border-radius:2px;transition:width .5s}}
.seo-details{{display:grid;gap:6px}}
.seo-row{{display:flex;gap:8px;font-size:0.82rem}}
.seo-label{{color:var(--text-muted);min-width:85px;flex-shrink:0}}
.seo-value{{color:var(--text);word-break:break-all}}
.footer{{text-align:center;margin-top:32px;color:var(--text-muted);font-size:0.8rem;padding-top:20px;border-top:1px solid var(--border)}}
@media(max-width:600px){{
  .metrics-grid{{grid-template-columns:1fr 1fr}}
}}
</style>
</head>
<body>
<div class="dashboard">
  <div class="header">
    <h1>🔍 SEO Dashboard <span class="count">{len(results)} sites</span></h1>
    <span class="timestamp">Dernière mise à jour : {timestamp}</span>
  </div>
  <div class="sites-grid">
    {cards_html}
  </div>
  <div class="footer">
    <p>Généré automatiquement par Alpesdata SEO Checker · Données indicatives, vérifier régulièrement</p>
  </div>
</div>
</body>
</html>"""


# ── Main ────────────────────────────────────────────────

def run_checks() -> list:
    results = []
    for site in SITES:
        print(f"  → {site['name']} ({site['url']})...", end=" ", flush=True)
        hostname = site["url"].replace("https://", "").replace("http://", "").split("/")[0]
        http = check_http(site["url"])
        ssl_data = check_ssl(hostname)
        seo_data = check_seo(site["url"])
        results.append({
            "site": site,
            "http": http,
            "ssl": ssl_data,
            "seo": seo_data,
            "checked_at": datetime.datetime.now().isoformat(),
        })
        print(f"HTTP {http.get('status', 'ERR')} / SSL {ssl_data.get('days_left', 'ERR')}j / SEO ✓")
    return results


def save_results(results: list):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # HTML
    html = generate_html(results)
    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\n  ✅ Dashboard HTML: {HTML_FILE}")

    # JSON
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"  ✅ Données JSON: {JSON_FILE}")


def deploy():
    """Copie le dashboard vers le serveur de production."""
    import subprocess
    target = DASHBOARD_TARGET
    print(f"\n  📦 Déploiement vers {target}...", end=" ")
    try:
        subprocess.run(
            ["ssh", "root@147.93.94.187", f"mkdir -p {target}"],
            capture_output=True, timeout=10
        )
        subprocess.run(
            ["scp", HTML_FILE, f"root@147.93.94.187:{target}/index.html"],
            capture_output=True, timeout=15
        )
        print("✅ OK")
    except Exception as e:
        print(f"❌ {e}")


if __name__ == "__main__":
    import sys

    print("🔍 SEO Dashboard — Alpesdata")
    print("=" * 40)

    results = run_checks()
    save_results(results)

    if "--serve" in sys.argv or "--update" in sys.argv:
        deploy()

    if "--update" in sys.argv:
        print("\n  ✅ Mise à jour terminée.")
