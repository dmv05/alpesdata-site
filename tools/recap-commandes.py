#!/usr/bin/env python3
"""Régénère le récap de tournée Iodman (page privée alpesdata.com) depuis le Google Sheet des commandes.

Usage :
    python3 tools/recap-commandes.py                # régénère le HTML et affiche les contrôles
    python3 tools/recap-commandes.py --deploy       # + commit, push et déploiement Coolify
    python3 tools/recap-commandes.py --check        # ne réécrit rien, imprime seulement l'état

Le gabarit (design) vit dans recap-commandes-9f2c.html : le script ne remplace que
les blocs délimités par <!-- recap:orders:start/end -->, recap:grand, recap:foot,
le badge « N commandes », le <title> et le sous-titre.
"""
import argparse
import json
import re
import subprocess
import sys
import unicodedata
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PAGE = REPO / "recap-commandes-9f2c.html"
SHEET_ID = "1vdBVm4DG9ZmxFh_NDQxAfoscCUP-wBXIqhEpD8Hl0fw"
TOURNEE = "3 au 5 décembre 2026"          # à ajuster à chaque tournée
COOLIFY_APP = "630c13132dea4f79b3d93444"  # app alpesdata-site (VPS2)
VPS2 = "root@147.93.94.187"

sys.path.insert(0, "/root/.hermes/skills/productivity/google-workspace/scripts")

# Libellés courts + familles de produits (colonne du formulaire -> (libellé, famille))
PRODUCTS = {
    "N°4 Bourriche de 25": ("N°4 — bourriche de 25 huîtres", "bourriche"),
    "N°4 Bourriche de 50": ("N°4 — bourriche de 50 huîtres", "bourriche"),
    "N°4 Bourriche de 100": ("N°4 — bourriche de 100 huîtres", "bourriche"),
    "N°3 Bourriche de 25": ("N°3 — bourriche de 25 huîtres", "bourriche"),
    "N°3 Bourriche de 50": ("N°3 — bourriche de 50 huîtres", "bourriche"),
    "N°3 Bourriche de 100": ("N°3 — bourriche de 100 huîtres", "bourriche"),
    "N°2 Bourriche de 25": ("N°2 — bourriche de 25 huîtres", "bourriche"),
    "N°2 Bourriche de 50": ("N°2 — bourriche de 50 huîtres", "bourriche"),
    "N°2 Bourriche de 100": ("N°2 — bourriche de 100 huîtres", "bourriche"),
    "St Jacques Barquettes de 0,5": ("Noix de St-Jacques 0,5 kg", "st-jacques"),
    "St Jacques Barquettes de 1 KG": ("Noix de St-Jacques 1 kg", "st-jacques"),
    "Caisse de Palourdes": ("Palourdes 1 kg", "palourdes"),
    "Moules de Bouchot à consommer dans les 8 jours 1kg400": ("Moules de bouchot 1 kg 400", "moules"),
    "Moules de Bouchot à consommer dans les 8 jours 2kgs": ("Moules de bouchot 2 kg", "moules"),
    "Rillettes  Père Billard : Saumon": ("Rillettes de saumon 100 g", "rillettes"),
    "Rillettes  Père Billard : Sardines": ("Rillettes de sardines 100 g", "rillettes"),
    "Rillettes  Père Billard : Saint Jacques": ("Rillettes de St-Jacques 100 g", "rillettes"),
    "Rillettes  Père Billard : Bulots": ("Rillettes de bulots 100 g", "rillettes"),
    "Carton de 6 Soupes": ("Carton de 6 soupes de poisson", "soupe"),
    "1 bocal de Soupe": ("Soupe de poisson 760 g", "soupe"),
    "carton 12 Soupes": ("Carton 12 soupes La Cancalaise", "soupe"),
    "ENCORNETS BLANCS": ("Encornets blancs 500 g", "encornets"),
    "Tartare d'Algues Galatée Pot de 90 Gramme : Classique": ("Tartare d'algues classique 90 g", "tartare"),
    "Tartare d'Algues Galatée Pot de 90 Gramme : Confit": ("Tartare d'algues oignons rouges 90 g", "tartare"),
}

FAMILY_PLURAL = {
    "bourriche": ("bourriche", "bourriches"),
    "moules": ("sachet de moules", "sachets de moules"),
    "soupe": ("soupe", "soupes"),
    "encornets": ("barquette d'encornets", "barquettes d'encornets"),
    "st-jacques": ("barquette de St-Jacques", "barquettes de St-Jacques"),
    "palourdes": ("caisse de palourdes", "caisses de palourdes"),
    "rillettes": ("pot de rillettes", "pots de rillettes"),
    "tartare": ("pot de tartare", "pots de tartare"),
}

MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
        "août", "septembre", "octobre", "novembre", "décembre"]


def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def euro(v):
    return f"{v:,.2f} €".replace(",", " ").replace(".", ",")


def parse_price(label):
    m = re.search(r"(\d+(?:[.,]\d{1,2})?)\s*€", label)
    if not m:
        return None
    return float(m.group(1).replace(",", "."))


def parse_money(cell):
    if not cell:
        return None
    m = re.search(r"(\d+(?:[ ,.]\d{3})*(?:[.,]\d{1,2})?)", cell.replace("\u202f", " "))
    if not m:
        return None
    return float(m.group(1).replace(" ", "").replace(",", "."))


def norm_phone(raw):
    d = re.sub(r"\D", "", raw or "")
    if d.startswith("33"):
        d = "0" + d[2:]
    return d if len(d) == 10 and d.startswith("0") else None


def fmt_phone(d):
    return " ".join([d[0:2], d[2:4], d[4:6], d[6:8], d[8:10]])


def fetch_rows():
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    creds = Credentials.from_authorized_user_file("/root/.hermes/google_token.json")
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    svc = build("sheets", "v4", credentials=creds)
    meta = svc.spreadsheets().get(spreadsheetId=SHEET_ID).execute()
    title = meta["sheets"][0]["properties"]["title"]
    vals = svc.spreadsheets().values().get(
        spreadsheetId=SHEET_ID, range=f"'{title}'!A1:AJ200").execute().get("values", [])
    return vals[0], vals[1:]


def build_orders(header, rows):
    products = {}
    for i, label in enumerate(header):
        if i < 6 or label in ("Total", "Livraison", "Paiement"):
            continue
        short, family = None, None
        for key, (s, f) in PRODUCTS.items():
            if key.lower() in label.lower():
                short, family = s, f
                break
        price = parse_price(label)
        if short is None:                       # produit inconnu : libellé nettoyé
            short = re.sub(r"\d+([.,]\d+)?\s*€.*$", "", label).strip(" :,-")
            short = short[:42]
            family = "autre"
        products[i] = {"label": label, "short": short, "family": family, "price": price}

    orders, warnings = [], []
    for row in rows:
        if not any(c.strip() for c in row):
            continue
        row = row + [""] * (len(header) - len(row))
        nom, prenom = row[2].strip(), row[3].strip()
        if not nom and not prenom:
            continue
        items = []
        for i, p in products.items():
            cell = row[i].strip() if i < len(row) else ""
            if not cell:
                continue
            try:
                qty = float(cell.replace(",", "."))
            except ValueError:
                continue
            if qty <= 0:
                continue
            unit = p["price"] or 0.0
            items.append({"short": p["short"], "family": p["family"], "qty": qty,
                          "unit": unit, "amount": qty * unit})
        if not items:
            continue
        computed = sum(it["amount"] for it in items)
        declared = parse_money(row[30])
        if declared is not None and abs(declared - computed) > 0.01:
            warnings.append(f"{prenom} {nom} : calculé {euro(computed)} ≠ formulaire {euro(declared)}")
        orders.append({
            "nom": nom, "prenom": prenom,
            "display": f"{prenom.capitalize()} {nom.title()}".strip(),
            "phone": norm_phone(row[4]),
            "sector": row[5].strip(),
            "items": items,
            "total": computed,
            "ts": row[0].strip(),
        })
    return orders, warnings


def render_orders(orders):
    out = ['  <div class="orders">']
    for o in orders:
        tel = ""
        if o["phone"]:
            tel = (f'<a class="tel" href="tel:+33{o["phone"][1:]}" '
                   f'aria-label="Appeler {o["display"]}">{fmt_phone(o["phone"])}</a>')
        out.append('    <div class="ord">')
        out.append(f'      <div class="ord-top"><span class="who">{o["display"]}</span>{tel}'
                   f'<span class="sum">{euro(o["total"])}</span></div>')
        out.append('      <div class="lines">')
        for it in o["items"]:
            q = f'×{int(it["qty"])}' if float(it["qty"]).is_integer() else f'×{it["qty"]}'
            out.append(f'        <div class="li"><span class="q">{q}</span>'
                       f'<span class="t">{it["short"]}</span>'
                       f'<span class="p">{euro(it["amount"])}</span></div>')
        out.append('      </div>')
        out.append('    </div>')
    out.append('  </div>')
    return "\n".join(out)


def render_grand(orders):
    total = sum(o["total"] for o in orders)
    return ('  <div class="grand">\n'
            f'    <span class="lab">Total {len(orders)} commande{"s" if len(orders) > 1 else ""}</span>\n'
            f'    <span class="val">{euro(total)}</span>\n'
            '  </div>'), total


def render_foot(orders):
    fam = {}
    for o in orders:
        for it in o["items"]:
            fam[it["family"]] = fam.get(it["family"], 0) + it["qty"]
    parts = []
    for family, qty in fam.items():
        n = int(qty) if float(qty).is_integer() else qty
        label = FAMILY_PLURAL.get(family, (f"article {family}", f"articles {family}"))
        if family == "autre":
            parts.append(f"{n} autre article")
            continue
        parts.append(f"{n} {label[0] if n <= 1 else label[1]}")
    prep = " · ".join(parts)
    return (f'  <p class="foot">À préparer : {prep}<br>'
            'Règlement sur place · CB, chèque ou espèces</p>')


def replace_block(html, name, content):
    start, end = f"<!-- recap:{name}:start -->", f"<!-- recap:{name}:end -->"
    i, j = html.find(start), html.find(end)
    assert i != -1 and j != -1 and i < j, f"marqueurs {name} absents"
    return html[:i + len(start)] + "\n" + content + "\n  " + html[j:]


def apply(html, orders):
    html = replace_block(html, "orders", render_orders(orders))
    grand, total = render_grand(orders)
    html = replace_block(html, "grand", grand)
    html = replace_block(html, "foot", render_foot(orders))

    n = len(orders)
    html = re.sub(r'<span class="chip">\d+ commande[s]?</span>',
                  f'<span class="chip">{n} commande{"s" if n > 1 else ""}</span>', html, count=1)
    html = re.sub(r"<title>.*?</title>",
                  f"<title>Livraison Iodman — {TOURNEE} · {n} commande{'s' if n > 1 else ''}</title>",
                  html, count=1, flags=re.S)

    sectors = sorted({o["sector"] for o in orders if o["sector"]})
    latest = max((o["ts"] for o in orders), default="")
    try:
        dt = datetime.strptime(latest.split(" ")[0], "%d/%m/%Y")
        releve = f"{dt.day} {MOIS[dt.month - 1]} {dt.year}"
    except Exception:
        releve = datetime.now().strftime("%d/%m/%Y")
    zone = " · ".join(s.replace("-", " · ") for s in sectors) if sectors else "secteur à confirmer"
    sub = f"Tournée {zone} — relevé du {releve}"
    html = re.sub(r'<p class="sub">.*?</p>', f'<p class="sub">{sub}</p>', html, count=1, flags=re.S)
    return html, total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--deploy", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    header, rows = fetch_rows()
    orders, warnings = build_orders(header, rows)
    if not orders:
        print("Aucune commande dans le formulaire — page inchangée.")
        return 1

    html, total = apply(PAGE.read_text(encoding="utf-8"), orders)

    print(f"{len(orders)} commandes · total {euro(total)}")
    for o in orders:
        arts = ", ".join(f'{int(i["qty"])}× {i["short"]}' for i in o["items"])
        tel = fmt_phone(o["phone"]) if o["phone"] else "TÉLÉPHONE MANQUANT"
        print(f'  - {o["display"]:20s} {tel:15s} {euro(o["total"]):>9s}  {arts}')
    for w in warnings:
        print("  ⚠", w)

    if args.check:
        print("(check : rien écrit)")
        return 0

    if PAGE.exists() and PAGE.read_text(encoding="utf-8") == html:
        print("page déjà à jour — rien à publier")
        return 0

    PAGE.write_text(html, encoding="utf-8")
    print(f"écrit {PAGE.relative_to(REPO)}")

    if not args.deploy:
        print("→ pour publier : --deploy")
        return 0

    subprocess.run(["git", "add", PAGE.name], cwd=REPO, check=True)
    subprocess.run(["git", "commit", "-q", "-m",
                    f"Récap tournée {TOURNEE} : {len(orders)} commandes, {euro(total)}"],
                   cwd=REPO, check=True)
    subprocess.run(["git", "push", "ssh://git@github.com/dmv05/alpesdata-site.git", "main"],
                   cwd=REPO, check=True,
                   env={"GIT_SSH_COMMAND": "ssh -i /root/.ssh/id_ed25519 -o IdentitiesOnly=yes",
                        "PATH": "/usr/local/bin:/usr/bin:/bin"})
    subprocess.run(["ssh", "-i", "/root/.ssh/id_ed25519", "-o", "IdentitiesOnly=yes", VPS2,
                    'TOKEN=$(cat /root/.coolify-token); curl -s -X POST -H "Authorization: Bearer $TOKEN" '
                    f'"http://localhost:8000/api/v1/applications/{COOLIFY_APP}/start?instant_deploy=true"'],
                   check=True)
    print("déploiement demandé — vérifier https://alpesdata.com/recap-commandes-9f2c.html")
    return 0


if __name__ == "__main__":
    sys.exit(main())
