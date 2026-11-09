#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Génère l'article blog REA à partir du gabarit d'un article existant (même CSS, même nav, même footer)."""
import re
from pathlib import Path

ROOT = Path("/root/alpesdata-site")
TEMPLATE = ROOT / "blog-failles-php-21-octobre.html"
OUT = ROOT / "blog-rea-mcp-ingenierie-inverse.html"

SLUG = "blog-rea-mcp-ingenierie-inverse.html"
URL = f"https://alpesdata.com/{SLUG}"
TITLE = "REA : décompiler n'importe quelle application — ce qu'il fait, et notre avis"
DESC = ("REA, l'outil qui laisse un agent IA décompiler et reconstruire des applications, a viré au phénomène "
        "viral. Ce qu'il fait vraiment, le cadre légal, et la position d'Alpesdata.")
DATE = "2026-11-09"
DATE_FR = "9 novembre 2026"
CATEGORY = "🤖 IA &amp; Développement"
READ = "8 min de lecture"
TAGS = "#IA #IngénierieInverse #REA #MCP #Développement"

src = TEMPLATE.read_text(encoding="utf-8")

# --- style + favicons, récupérés tels quels du gabarit ---
style = re.search(r"<style>.*?</style>", src, re.S).group(0)
favicons = re.search(r'<link rel="icon" type="image/svg\+xml".*?</head>', src, re.S).group(0)[:-len("</head>")]
nav = re.search(r'<nav class="nav">.*?</nav>', src, re.S).group(0)
footer = re.search(r'<footer class="footer">.*?</footer>', src, re.S).group(0)
script = re.search(r'<script>\ndocument\.addEventListener\("DOMContentLoaded".*?</script>', src, re.S).group(0)

HEAD = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{TITLE}</title>
<meta name="description" content="{DESC}">
    <meta property="og:title" content="{TITLE}" />
    <meta property="og:description" content="{DESC}" />
    <meta property="og:type" content="article" />
    <meta property="og:url" content="{URL}" />
    <meta property="og:image" content="https://alpesdata.com/images/og-alpesdata.jpg" />
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Alpesdata — développement web, IA et dépannage à Briançon">
    <meta property="og:locale" content="fr_FR" />
    <meta property="og:site_name" content="Alpesdata" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{TITLE}" />
    <meta name="twitter:description" content="{DESC}" />
    <meta name="twitter:image" content="https://alpesdata.com/images/og-alpesdata.jpg" />
    <link rel="canonical" href="{URL}" />
    <script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "{TITLE}",
  "description": "{DESC}",
  "url": "{URL}",
  "mainEntityOfPage": {{
    "@type": "WebPage",
    "@id": "{URL}"
  }},
  "image": "https://alpesdata.com/images/og-alpesdata.jpg",
  "datePublished": "{DATE}",
  "dateModified": "{DATE}",
  "author": {{
    "@type": "Person",
    "name": "Didier Moranval-Vincent",
    "url": "https://alpesdata.com/"
  }},
  "publisher": {{
    "@type": "Organization",
    "name": "Alpesdata",
    "url": "https://alpesdata.com",
    "logo": {{
      "@type": "ImageObject",
      "url": "https://alpesdata.com/favicon-192.png"
    }}
  }}
}}
  </script>


<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Syne:wght@400;600;700&display=swap" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Syne:wght@400;600;700&display=swap"></noscript>
{style}
{favicons}</head>
"""

BODY = f"""<body>
    {nav.replace('class="active"', '')}

    <article class="article-page">
      <div class="article-container">
        <a href="/blog.html" class="back-link">← Retour au blog</a>

        <header class="article-header fade-in">
          <span class="article-category">{CATEGORY}</span>
          <h1>REA&nbsp;: l'outil qui décompilait n'importe quelle application — ce qu'il fait vraiment, et ce qu'Alpesdata en pense</h1>
          <div class="article-meta">
            <span>{DATE_FR}</span>
            <span>{READ}</span>
            <span>{TAGS}</span>
          </div>
          <p style="font-size:1.1rem;color:var(--text-light);line-height:1.7">
            En octobre 2026, un dépôt GitHub passé inaperçu pendant l'été a viré au phénomène&nbsp;: <strong>REA</strong>,
            «&nbsp;Reverse Engineer Anything&nbsp;», promet de laisser un agent IA décompiler n'importe quel logiciel
            et le reconstruire. Les démos montrent des clones de Calendly et de Trello obtenus en quelques minutes.
            Derrière le buzz, il y a une vraie question technique, une vraie question juridique — et une position à
            prendre. Voici la nôtre.
          </p>
        </header>

        <div class="fade-in">
          <h2>📌 Ce que c'est, en une phrase</h2>

          <p>
            REA est un <strong>serveur MCP</strong> doublé d'une <strong>ligne de commande</strong>, écrit en
            TypeScript, publié sous licence MIT par un développeur indépendant (<code>morluto</code>), et installable
            en une commande&nbsp;: <code>npx --yes rea-agents@latest setup</code>.
          </p>

          <p>
            Le point à comprendre&nbsp;: <strong>REA ne décompile rien lui-même</strong>. Il ne contient ni désassembleur
            ni moteur d'analyse. C'est une <strong>couche d'orchestration</strong>&nbsp;: il branche un agent de code
            (Claude Code, Cursor, Codex, Gemini CLI, Windsurf…) sur les outils d'ingénierie inverse qui existent depuis
            vingt ans — <strong>Ghidra</strong>, <strong>Hopper</strong>, <strong>IDA</strong> — et il leur donne un
            vocabulaire commun. L'agent demande&nbsp;; REA traduit&nbsp;; l'outil exécute&nbsp;; le résultat revient avec
            ses preuves et ses limites.
          </p>

          <blockquote>
            REA est au décompilateur ce qu'un standard téléphonique est à la conversation&nbsp;:
            <strong>il ne parle pas à votre place, il met les bonnes personnes en ligne.</strong>
          </blockquote>

          <div class="stats-grid">
            <div class="stat-card">
              <span class="number">≈ 143 700</span>
              <span class="label">étoiles GitHub fin octobre 2026<br>(111 en juillet, selon les décomptes publics)</span>
            </div>
            <div class="stat-card">
              <span class="number">MIT</span>
              <span class="label">licence open source, code entièrement lisible</span>
            </div>
            <div class="stat-card">
              <span class="number">6+</span>
              <span class="label">assistants compatibles, de Claude Code à Gemini CLI</span>
            </div>
          </div>
        </div>

        <div class="fade-in">
          <h2>🧰 Ce qu'il sait ouvrir</h2>

          <p>
            La couverture est plus large que le mot «&nbsp;décompilation&nbsp;» ne le laisse croire, et c'est ce qui
            explique une partie de l'engouement&nbsp;:
          </p>

          <ul>
            <li><strong>Binaires natifs</strong> — Mach-O (macOS), ELF (Linux), PE (Windows), y compris les métadonnées
            Swift et Objective-C. C'est là que l'outil est le plus profond.</li>
            <li><strong>Assemblages .NET</strong> — inspection statique, sans exécuter le programme.</li>
            <li><strong>JavaScript et applications Electron</strong> — lecture du code embarqué, sans lancement.</li>
            <li><strong>Archives d'applications</strong> — APK Android, IPA iOS, ASAR, MSIX, ZIP&nbsp;: inventaire et
            exploration avant toute analyse.</li>
            <li><strong>Sites web</strong> — via les outils d'inspection du navigateur.</li>
          </ul>

          <p>
            Deux précautions que l'outil affiche lui-même&nbsp;: l'analyse native suppose que vous possédiez déjà une
            licence <strong>Hopper</strong> ou <strong>IDA</strong> (outils commerciaux, plusieurs centaines d'euros),
            et la capture d'exécution se fait avec vos propres droits sur votre propre machine.
          </p>
        </div>

        <div class="fade-in">
          <h2>🎬 Pourquoi tout le monde en parle</h2>

          <p>
            Ce qui a fait décoller REA n'est pas une avancée technique, c'est une série de démonstrations&nbsp;:
            on montre une capture d'écran de Calendly, de Typeform ou de Trello, on demande à l'agent de «&nbsp;faire
            pareil&nbsp;», et quelques minutes plus tard une application qui y ressemble tourne sur la machine.
            Le récit s'écrit tout seul&nbsp;: <em>les abonnements SaaS à 30&nbsp;€ par mois sont morts</em>.
          </p>

          <p>
            La nuance est importante, et elle est rarement dite&nbsp;: <strong>dans ces démos, REA ne décompile
            rien</strong>. Une capture d'écran ne contient aucun code. Ce qui est reconstruit, c'est l'apparence et
            deux ou trois flux principaux. Il n'y a derrière ni la vérification des conflits d'agenda, ni la
            synchronisation des fuseaux horaires, ni les années de corrections de bugs, ni le support quand
            quelque chose casse un mardi matin.
          </p>

          <div class="highlight-box">
            <h3>Cloner l'écran n'est pas remplacer l'abonnement</h3>
            <p>
              Une interface se copie en une après-midi. Ce qu'on achète dans un abonnement, ce sont les mille
              décisions invisibles qui la font tenir debout — et elles ne sont pas dans la capture d'écran.
            </p>
          </div>
        </div>

        <div class="fade-in">
          <h2>⚖️ Ce que dit le droit, en France</h2>

          <p>
            Un logiciel est protégé par le droit d'auteur, code source compris. La décompilation n'est donc pas
            libre. Le Code de la propriété intellectuelle prévoit <strong>une exception étroite</strong>, à l'article
            L122-6-1&nbsp;IV&nbsp;: reproduire le code et traduire sa forme est permis lorsque c'est indispensable pour
            permettre à un logiciel <strong>créé indépendamment</strong> de fonctionner avec un autre. À trois
            conditions cumulatives&nbsp;: avoir le droit d'utiliser le logiciel, se limiter aux parties réellement
            nécessaires, et ne pas porter atteinte à son exploitation normale.
          </p>

          <p>
            En dehors de ce cadre — dupliquer un logiciel pour le revendre, le redistribuer, ou se dispenser de payer
            une licence tout en utilisant son travail — on ne parle plus d'interopérabilité. On parle de
            <strong>contrefaçon</strong>, et c'est un délit.
          </p>

          <p>
            Le README du projet dit d'ailleurs la même chose, en anglais et en trois lignes&nbsp;: usage réservé à la
            recherche légale, à l'interopérabilité, à la préservation, et aux logiciels que vous possédez ou que vous
            êtes autorisé à examiner. Ce n'est pas une clause de style&nbsp;: c'est le périmètre dans lequel l'outil
            est distribué.
          </p>
        </div>

        <div class="fade-in">
          <h2>🧭 Notre avis</h2>

          <blockquote>
            <strong>Alpesdata ne cautionne pas la duplication pirate de logiciels.</strong> Copier le travail de
            quelqu'un d'autre pour ne pas le payer, ce n'est pas de l'ingénierie&nbsp;: c'est du vol, et en France
            c'est un délit. Nous ne le ferons pas, et nous ne le recommanderons à personne.
          </blockquote>

          <p>
            Cela étant dit, deux choses doivent être dites, parce qu'elles sont vraies et qu'elles vont compter dans
            les mois qui viennent.
          </p>

          <p>
            <strong>Un — l'outil n'est pas l'usage.</strong> Le même marteau sert à monter une charpente ou à
            défoncer une porte. L'ingénierie inverse est une pratique ancienne et parfaitement légitime dans son
            cadre&nbsp;: comprendre un format pour récupérer ses propres données, vérifier ce qu'un prestataire a
            réellement livré, faire dialoguer deux logiciels qu'un client possède déjà, documenter un système avant
            de le remplacer. Ce sont des travaux que nous faisons, et qu'aucune loi n'interdit.
          </p>

          <p>
            <strong>Deux — si cette technologie peut accélérer le développement en diminuant le coût, pourquoi
            pas&nbsp;?</strong> Un artisan qui paie 40&nbsp;€ par mois depuis six ans pour un outil dont il utilise
            5&nbsp;% des fonctions a le droit de se demander ce que coûterait la fonction qu'il utilise vraiment.
            Ce n'est pas une opinion, c'est une soustraction. Refuser de la faire au nom du confort, c'est laisser
            le client payer la différence. Nous préférons lui poser la question — et lui dire honnêtement quand la
            réponse est «&nbsp;gardez votre abonnement&nbsp;», ce qui arrive souvent.
          </p>

          <p>
            <strong>Trois — cette technologie existe.</strong> Elle est open source, gratuite, documentée, et
            plusieurs centaines de milliers de personnes l'ont déjà regardée. Faire comme si elle n'existait pas ne
            la fait pas disparaître&nbsp;: ça garantit seulement d'être le dernier à comprendre ce qui arrive à son
            métier. On peut refuser d'utiliser un outil&nbsp;; on ne peut pas refuser de savoir qu'il existe.
          </p>
        </div>

        <div class="fade-in">
          <h2>🏢 Ce que ça change pour un éditeur ou une PME</h2>

          <p>
            La question utile n'est pas «&nbsp;est-ce que mon logiciel peut être copié&nbsp;?&nbsp;» — la réponse est
            oui, et elle l'était avant REA. La question est&nbsp;: <strong>si mon produit était reconstruit en une
            semaine, que resterait-il de mon avantage&nbsp;?</strong>
          </p>

          <ul>
            <li><strong>Si votre valeur est une interface</strong>, elle est copiable. Le rempart est ailleurs&nbsp;:
            vos données, vos intégrations, votre support, votre marque, la relation avec vos clients.</li>
            <li><strong>Si votre valeur est un savoir accumulé</strong> — quinze ans de règles métier, d'exceptions,
            de cas particuliers — un clone de surface ne vous atteindra pas. C'est le bon endroit pour mettre ses
            efforts.</li>
            <li><strong>Ce qu'il faut surveiller</strong>&nbsp;: vos conditions d'utilisation, vos marques déposées, vos
            bases de données (et le RGPD), et la façon dont vos propres prestataires accèdent à votre code.</li>
          </ul>
        </div>

        <div class="fade-in">
          <h2>🔧 Ce que nous en faisons, concrètement</h2>

          <p>
            Nous ne clonons pas de logiciels. Ce que nous regardons dans ce type d'outil, c'est un usage précis et
            documenté&nbsp;:
          </p>

          <ul>
            <li>récupérer les données d'un logiciel abandonné dont le format n'est plus documenté&nbsp;;</li>
            <li>vérifier ce qu'un prestataire a réellement livré, quand le code source n'est pas disponible&nbsp;;</li>
            <li>documenter un système existant avant migration, plutôt que de le remplacer à l'aveugle&nbsp;;</li>
            <li>assurer l'interopérabilité entre deux outils que le client possède déjà.</li>
          </ul>

          <p>
            Dans ces quatre cas, le client possède le logiciel ou est autorisé à l'examiner, et l'objectif n'est jamais
            de revendre une copie. C'est la ligne&nbsp;: à l'intérieur, c'est du travail&nbsp;; au-delà, c'est un délit.
          </p>
        </div>

        <div class="fade-in">
          <h2>✅ En résumé</h2>
          <ul>
            <li>REA n'est pas magique&nbsp;: c'est une couche d'orchestration posée sur des outils de 2005.</li>
            <li>Il ne transforme pas une capture d'écran en produit fini&nbsp;: il aide un agent à comprendre du code compilé.</li>
            <li>La décompilation est légale dans un cadre étroit&nbsp;; la duplication ne l'est pas.</li>
            <li>Le coût du logiciel va baisser. Ce n'est pas une raison pour copier&nbsp;; c'est une raison pour se poser la bonne question.</li>
          </ul>
        </div>

        <div class="cta-box">
          <h3>Un logiciel que vous voulez quitter, reprendre ou faire évoluer&nbsp;?</h3>
          <p>
            Nous regardons ce qu'il fait réellement, ce qu'il vous coûte chaque année, et ce qu'il faudrait pour le
            remplacer — ou pour continuer avec, si c'est plus raisonnable. Premier échange gratuit.
          </p>
          <a href="/contact.html" class="btn">Parler de votre projet →</a>
        </div>

        <p style="font-size:0.85rem;color:var(--text-light);font-style:italic">
          Sources&nbsp;:
          <a href="https://github.com/morluto/rea" target="_blank" rel="noopener">morluto/rea</a>, dépôt officiel (périmètre
          d'usage, outils pris en charge, licence MIT) ·
          <a href="https://www.mindstudio.ai/blog/reverse-engineer-anything-mcp" target="_blank" rel="noopener">Reverse Engineer
          Anything&nbsp;: what the viral REA MCP actually does</a>, MindStudio, 2026 ·
          <a href="https://www.eigent.ai/blog/rea-reverse-engineer-anything" target="_blank" rel="noopener">REA&nbsp;: Reverse
          Engineer Anything with AI agents</a>, Eigent ·
          <a href="https://dev.to/arshtechpro/rea-let-your-ai-agent-reverse-engineer-the-app-features-you-wish-you-had-3en7" target="_blank" rel="noopener">REA&nbsp;: let your
          AI agent reverse engineer the app features you wish you had</a>, DEV Community ·
          <a href="https://medium.com/@info.booststash/reverse-engineer-anything-went-viral-the-calendly-clone-demos-are-a-different-trick-dc9511769f5e" target="_blank" rel="noopener">Reverse Engineer
          Anything went viral — the Calendly clone demos are a different trick</a>, Medium, octobre 2026 (décomptes d'étoiles, v4.1) ·
          Code de la propriété intellectuelle, article L122-6-1 IV (exception d'interopérabilité).
          <br>Cet article a été rédigé avec <strong>Hermes</strong>, l'agent open source que nous déployons pour nos clients.
        </p>
      </div>
    </article>
    {footer}
{script}
</body>
</html>
"""

OUT.write_text(HEAD + BODY, encoding="utf-8")
print("écrit:", OUT, len(HEAD + BODY), "octets")
