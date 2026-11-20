#!/usr/bin/env python3
"""Génère blog-anthropic-ipo-nasdaq.html + carte blog.html + sitemap.

Assemblage par découpe (skill alpesdata-client-sites, references/blog-articles.md §1) :
head/CSS/nav/footer repris du dernier article publié, seul le <head> SEO et le corps changent.
Corriger ICI, puis relancer : python3 tools/build-blog-anthropic-ipo.py
"""
import re
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / 'blog-panne-outlook-microsoft-365.html'
OUT = ROOT / 'blog-anthropic-ipo-nasdaq.html'

SLUG = 'blog-anthropic-ipo-nasdaq.html'
URL = 'https://alpesdata.com/' + SLUG
TITLE = ("Anthropic entre en Bourse : 5 ans pour valoir 2 000 milliards "
         "— et 2 000 milliards, ça fait 2 billions")
DESC = ("Le 19 novembre 2026, Anthropic a signé la plus grosse introduction en bourse de l'histoire : "
        "81,3 milliards de dollars levés, 1 270 milliards de capitalisation, et un Nasdaq qui perd 2,3 % "
        "le même jour. Ce que ces chiffres disent vraiment — et pourquoi une entreprise n'est pas un État.")
DATE = '2026-11-19'
CAT = '🤖 Intelligence Artificielle'
READ = '12 min'

NEW_HEAD = f"""<title>{TITLE}</title>
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
  "mainEntityOfPage": {{"@type": "WebPage", "@id": "{URL}"}},
  "image": "https://alpesdata.com/images/og-alpesdata.jpg",
  "datePublished": "{DATE}",
  "dateModified": "{DATE}",
  "author": {{"@type": "Person", "name": "Didier Moranval-Vincent", "url": "https://alpesdata.com/"}},
  "publisher": {{"@type": "Organization", "name": "Alpesdata", "url": "https://alpesdata.com",
    "logo": {{"@type": "ImageObject", "url": "https://alpesdata.com/favicon-192.png"}}}}
}}
  </script>"""

ANT = "https://www.anthropic.com/news/anthropic-prices-initial-public-offering"
REU = ("https://www.reuters.com/business/nasdaq-futures-jump-anthropics-record-ipo-pricing-"
       "fuels-hopes-strong-debut-2026-11-19/")
CNBC = "https://www.cnbc.com/2026/11/19/anthropic-ipo-ant-live-updates.html"
FOOL = ("https://www.fool.com/investing/2026/11/19/"
        "anthropic-just-started-trading-here-s-what-you-need-to-know/")
FMI = "https://www.worldometers.info/fr/pib/pib-par-pays/?source=imf&region=worldwide&year=2026&metric=nominal"
YAH = "https://finance.yahoo.com/markets/article/anthropic-seeks-14-trillion-valuation-in-ipo-130300928.html"

MOBILE_CSS = """<!-- mobile-fix-blog --><style>
@media(max-width:560px){
  .article-page{padding:36px 16px}
  .article-page .stats-grid{grid-template-columns:1fr}
  .article-page .stat-card{padding:18px}
  .article-page .stat-card .number{font-size:1.6rem}
  .article-page .cta-box,.article-page .highlight-box,.article-page .tech-box{padding:22px}
  .article-page blockquote{padding:20px}
}
</style>"""

BODY = f"""
    <article class="article-page">
      <div class="article-container">
        <a href="/blog.html" class="back-link">← Retour au blog</a>

        <header class="article-header fade-in">
          <span class="article-category">{CAT}</span>
          <h1>{TITLE}</h1>
          <div class="article-meta">
            <span>19 novembre 2026</span>
            <span>{READ} de lecture</span>
            <span>#Anthropic #IPO #Nasdaq #Valorisation #IA</span>
          </div>
          <p style="font-size:1.1rem;color:var(--text-light);line-height:1.7">
            Le 19 novembre 2026, l'éditeur de Claude a levé <strong>81,3&nbsp;milliards de dollars</strong> et
            ouvert en hausse de 34&nbsp;% sur le Nasdaq. Dans la journée, sa valeur a brièvement franchi
            <strong>2&nbsp;000&nbsp;milliards de dollars</strong>&nbsp;; à la clôture, elle en valait 1&nbsp;270.
            Trois questions méritent mieux qu'un titre de dépêche&nbsp;: que valent réellement ces 2&nbsp;000
            milliards, est-ce que cela s'écrit «&nbsp;billions&nbsp;», et une entreprise peut-elle être plus riche
            qu'un État&nbsp;? Réponses chiffrées, y compris quand elles déplaisent.
          </p>
        </header>

        <div class="fade-in">
          <h2>📌 Ce qui s'est passé, en chiffres vérifiables</h2>

          <p>
            Anthropic, PBC a fixé le prix de son introduction le <strong>mercredi 18 novembre au soir</strong>&nbsp;:
            <strong>980&nbsp;millions d'actions de classe A à 83&nbsp;dollars</strong>. La cotation a commencé le
            jeudi 19 novembre sur le <strong>Nasdaq Global Select Market</strong>, sous le symbole
            <strong>ANT</strong>, et l'offre doit être réglée le 20 novembre
            (<a href="{ANT}" target="_blank" rel="noopener">communiqué d'Anthropic</a>).
          </p>

          <p>
            Un détail que la plupart des reprises ont sauté, et qui change le sens du mot «&nbsp;levée&nbsp;»&nbsp;:
            sur ces 980&nbsp;millions d'actions, <strong>956,4&nbsp;millions sont vendues par Anthropic</strong>
            et <strong>23,6&nbsp;millions par des actionnaires existants</strong>. La société encaisse donc
            <strong>79,4&nbsp;milliards de dollars</strong>&nbsp;; les 2&nbsp;milliards restants vont dans la poche
            de ceux qui sortent. Le chiffre de 81,3&nbsp;milliards est exact — il n'est simplement pas entièrement
            disponible pour financer les data centers.
          </p>

          <p>
            La séance, maintenant. Ouverture à <strong>111,50&nbsp;$</strong>, soit 34&nbsp;% au-dessus du prix
            d'introduction. Plus haut à 115,10&nbsp;$, plus bas à 92,72&nbsp;$, et une clôture à
            <strong>97,17&nbsp;$</strong>, en hausse de <strong>17,1&nbsp;%</strong> sur 857&nbsp;millions d'actions
            échangées. Autrement dit&nbsp;: celui qui a acheté à l'ouverture a perdu 13&nbsp;% dans la journée.
          </p>

          <div class="stats-grid">
            <div class="stat-card">
              <span class="number">81,3 Md$</span>
              <span class="label">levés au total<br>dont 79,4 Md$ pour la société</span>
            </div>
            <div class="stat-card">
              <span class="number">+17,1 %</span>
              <span class="label">à la clôture (97,17 $)<br>après une ouverture à +34 %</span>
            </div>
            <div class="stat-card">
              <span class="number">1 270 Md$</span>
              <span class="label">capitalisation à la clôture<br>≈ 1 155 Md€</span>
            </div>
            <div class="stat-card">
              <span class="number">−2,3 %</span>
              <span class="label">Nasdaq le même jour<br>S&amp;P 500 −2,0 %</span>
            </div>
          </div>

          <p>
            Car le contexte de la journée n'est pas anecdotique. Le jour de la plus grosse introduction en bourse
            de l'histoire, <strong>Wall Street a fini en nette baisse</strong>&nbsp;: S&amp;P&nbsp;500 −2,0&nbsp;%,
            Dow Jones −2,2&nbsp;%, Nasdaq −2,3&nbsp;%, et même le bitcoin −2,7&nbsp;%. Reuters titre sur une
            introduction qui «&nbsp;ne relance pas le pari sur l'IA&nbsp;».
          </p>
        </div>

        <div class="fade-in">
          <h2>⏱️ Cinq ans, de zéro à 33 milliards de revenus</h2>

          <p>
            Anthropic a été créée en <strong>2021</strong> par Dario Amodei et un petit groupe de chercheurs partis
            d'OpenAI. Claude arrive auprès du public en 2023. En mai 2026, une levée de fonds valorise la société
            à <strong>965&nbsp;milliards de dollars</strong>. Six mois plus tard, l'introduction la porte à
            1&nbsp;270&nbsp;milliards. <strong>Cinq ans entre la création et le Nasdaq.</strong>
          </p>

          <p>
            Ce qui rend le chiffre crédible, ce n'est pas la promesse&nbsp;: c'est le chiffre d'affaires.
            <strong>Plus de 17&nbsp;milliards de dollars au troisième trimestre 2026</strong>, et plus de
            33&nbsp;milliards sur les neuf premiers mois, en progression de <strong>1&nbsp;200&nbsp;%</strong> sur un
            an. Une entreprise qui triple de taille chaque année pendant trois ans finit par peser lourd, quelle que
            soit l'histoire qu'on raconte autour.
          </p>

          <div class="tech-box">
            <h4>La vitesse n'est pas inédite. La taille, si.</h4>
            <p>
              Apple est entrée en bourse en 1980, quatre ans après sa création, à <strong>1,8&nbsp;milliard de
              dollars</strong> de l'époque. Amazon en 1997, trois ans après sa création, à
              <strong>438&nbsp;millions</strong>. Aller vite en bourse n'a donc rien de nouveau&nbsp;: Amazon a été
              plus rapide qu'Anthropic. Ce qui est nouveau, c'est <strong>le montant au moment de l'introduction</strong>&nbsp;:
              la capitalisation d'Anthropic vaut environ <strong>714 fois</strong> celle d'Apple à son entrée, et
              <strong>2&nbsp;900 fois</strong> celle d'Amazon. L'inflation des quarante-cinq dernières années ne
              change rien à l'ordre de grandeur.
            </p>
          </div>
        </div>

        <div class="fade-in">
          <h2>🔢 « Billion » ne veut pas dire « milliard »</h2>

          <p>
            La question mérite d'être posée sérieusement, parce que la confusion est partout et qu'elle se trompe
            d'un facteur mille. En français, l'échelle longue est la règle&nbsp;:
          </p>

          <ul>
            <li><strong>1 million</strong> = 10<sup>6</sup> = 1&nbsp;000&nbsp;000</li>
            <li><strong>1 milliard</strong> = 10<sup>9</sup> = 1&nbsp;000 millions</li>
            <li><strong>1 billion</strong> = 10<sup>12</sup> = <strong>1&nbsp;000 milliards</strong></li>
          </ul>

          <p>
            En anglais, c'est l'échelle courte&nbsp;: <em>billion</em> = 10<sup>9</sup> (notre milliard) et
            <em>trillion</em> = 10<sup>12</sup> (notre billion). Le piège est donc un faux ami pur&nbsp;: quand un
            journaliste traduit «&nbsp;<em>a trillion-dollar company</em>&nbsp;» par «&nbsp;une entreprise à
            billions&nbsp;», il a raison&nbsp;; quand il traduit «&nbsp;<em>a billion dollars</em>&nbsp;» par
            «&nbsp;un billion de dollars&nbsp;», il se trompe de mille fois.
          </p>

          <p>
            Appliqué à Anthropic&nbsp;: <strong>1&nbsp;270&nbsp;milliards de dollars, c'est 1,27 billion de
            dollars</strong> en français — et 1,27 <em>trillion</em> en anglais. Le pic de séance à
            2&nbsp;000&nbsp;milliards, c'est exactement <strong>2 billions</strong>. Oui, on a changé d'unité&nbsp;:
            depuis cette semaine, la bonne façon de parler d'une capitalisation tech en français n'est plus le
            milliard, mais le billion.
          </p>
        </div>

        <div class="fade-in">
          <h2>🌍 Plus riche qu'un État&nbsp;? La comparaison qui ne tient pas</h2>

          <p>
            À 1&nbsp;270&nbsp;milliards de dollars, Anthropic se glisse entre l'Arabie saoudite
            (1&nbsp;340&nbsp;milliards de PIB) et la <strong>Suisse (1&nbsp;140&nbsp;milliards)</strong>&nbsp;: au
            vingtième rang mondial des «&nbsp;économies&nbsp;», juste devant la Pologne et Taïwan. Au plus haut de
            la séance, à 2&nbsp;000&nbsp;milliards, elle dépassait l'<strong>Espagne</strong> et l'Australie, et
            s'installait au seizième rang. Sur le papier, oui&nbsp;: une société de cinq ans vaut plus que la
            Suisse.
          </p>

          <table style="width:100%;border-collapse:collapse;margin:20px 0;font-size:0.9rem">
            <thead>
              <tr>
                <th style="text-align:left;padding:10px 8px;border-bottom:2px solid var(--clay)">Économie</th>
                <th style="text-align:right;padding:10px 8px;border-bottom:2px solid var(--clay)">PIB 2026 (FMI, nominal)</th>
                <th style="text-align:right;padding:10px 8px;border-bottom:2px solid var(--clay)">Capitalisation</th>
              </tr>
            </thead>
            <tbody>
              <tr><td style="padding:8px;border-bottom:1px solid #e8e2d8">France</td><td style="text-align:right;padding:8px;border-bottom:1px solid #e8e2d8">3 550 Md$</td><td style="text-align:right;padding:8px;border-bottom:1px solid #e8e2d8">—</td></tr>
              <tr><td style="padding:8px;border-bottom:1px solid #e8e2d8">Italie</td><td style="text-align:right;padding:8px;border-bottom:1px solid #e8e2d8">2 700 Md$</td><td style="text-align:right;padding:8px;border-bottom:1px solid #e8e2d8">—</td></tr>
              <tr><td style="padding:8px;border-bottom:1px solid #e8e2d8">Espagne</td><td style="text-align:right;padding:8px;border-bottom:1px solid #e8e2d8">2 090 Md$</td><td style="text-align:right;padding:8px;border-bottom:1px solid #e8e2d8">—</td></tr>
              <tr><td style="padding:8px;border-bottom:1px solid #e8e2d8">Arabie saoudite</td><td style="text-align:right;padding:8px;border-bottom:1px solid #e8e2d8">1 340 Md$</td><td style="text-align:right;padding:8px;border-bottom:1px solid #e8e2d8">—</td></tr>
              <tr><td style="padding:8px;border-bottom:1px solid #e8e2d8"><strong>Anthropic (clôture)</strong></td><td style="text-align:right;padding:8px;border-bottom:1px solid #e8e2d8">CA > 33 Md$ sur 9 mois</td><td style="text-align:right;padding:8px;border-bottom:1px solid #e8e2d8"><strong>1 270 Md$</strong></td></tr>
              <tr><td style="padding:8px;border-bottom:1px solid #e8e2d8">Suisse</td><td style="text-align:right;padding:8px;border-bottom:1px solid #e8e2d8">1 140 Md$</td><td style="text-align:right;padding:8px;border-bottom:1px solid #e8e2d8">—</td></tr>
            </tbody>
          </table>

          <p>
            Et pourtant la comparaison est fausse, pour quatre raisons qui ne sont pas des subtilités de
            comptable.
          </p>

          <p>
            <strong>1. Un flux contre un stock.</strong> Le PIB mesure ce qu'un pays <em>produit en un an</em>&nbsp;;
            la capitalisation mesure ce que le marché est prêt à payer <em>aujourd'hui</em> pour les profits futurs.
            Comparer les deux, c'est comparer le prix d'un immeuble à son loyer annuel. Ce sont deux nombres
            légitimes&nbsp;; ce n'est pas la même chose.
          </p>

          <p>
            <strong>2. Une capitalisation n'est pas de l'argent.</strong> Anthropic ne peut pas dépenser
            1&nbsp;270&nbsp;milliards&nbsp;: elle en dispose d'environ 79&nbsp;milliards levés, plus ce qu'elle
            encaisse. Le reste est une opinion collective, révisable chaque matin.
          </p>

          <p>
            <strong>3. 7,5&nbsp;% du capital a fixé le prix de 100&nbsp;%.</strong> Les 980&nbsp;millions d'actions
            vendues représentent environ 7,5&nbsp;% des 13&nbsp;milliards d'actions que suppose la capitalisation.
            Le prix d'une petite fraction sert de mètre à l'ensemble. C'est ce qui rend la valeur si volatile&nbsp;:
            elle peut perdre un tiers sans qu'un seul client ait changé de fournisseur.
          </p>

          <p>
            <strong>4. Un État lève l'impôt, bat monnaie et possède son territoire.</strong> La France encaisse
            environ 1&nbsp;400&nbsp;milliards d'euros de recettes publiques par an&nbsp;; le chiffre d'affaires
            annualisé d'Anthropic tourne autour de 62&nbsp;milliards d'euros. L'État français encaisse donc
            <strong>vingt-deux fois par an</strong> ce que l'entreprise facture. Sur la capacité à financer des
            routes, des hôpitaux ou des écoles, il n'y a pas de match.
          </p>

          <blockquote>
            <strong>La comparaison qui tient n'est pas celle de la richesse, c'est celle de la capacité
            d'investissement.</strong> 81,3&nbsp;milliards de dollars levés en une journée, c'est environ
            <strong>six années</strong> du budget annuel d'Horizon Europe, le programme de recherche de l'Union
            européenne (95,5&nbsp;milliards d'euros sur sept ans). Voilà le vrai basculement&nbsp;: une entreprise
            privée mobilise en un jour ce qu'un continent met six ans à réunir pour la recherche.
          </blockquote>
        </div>

        <div class="fade-in">
          <h2>📉 Pourquoi le marché a décroché le même jour</h2>

          <p>
            Trois explications circulent, et elles ne se valent pas. La première est mécanique&nbsp;:
            <strong>81 milliards de dollars ont été absorbés ce jour-là</strong>. Cet argent ne pouvait pas servir à
            acheter autre chose. Les valeurs qui ont le plus reculé sont d'ailleurs les autres valeurs de l'IA&nbsp;:
            Nvidia −3,3&nbsp;%, Amazon −3,9&nbsp;%, Meta −3,3&nbsp;%. Ce n'est pas un jugement sur Anthropic, c'est
            un transfert de liquidité.
          </p>

          <p>
            La deuxième est boursière, et vieille comme les marchés&nbsp;: <em>sell the news</em>. L'IA porte la
            hausse depuis trois ans. Une introduction en bourse est précisément le moment où les initiés obtiennent
            un prix public et où le dernier acheteur arrive. Statistiquement, les sommets se marquent souvent le
            jour où tout le monde peut enfin acheter.
          </p>

          <p>
            La troisième est plus intéressante&nbsp;: l'action a <strong>perdu la moitié de sa hausse en une
            séance</strong> — +34&nbsp;% à l'ouverture, +17,1&nbsp;% à la clôture, et un passage sous les
            100&nbsp;dollars. L'offre avait été sursouscrite <strong>six fois</strong>, dans une fourchette
            initiale de 70 à 78&nbsp;dollars. Une demande aussi forte qui ne tient pas la journée, ce n'est pas
            l'échec d'Anthropic&nbsp;: c'est la démonstration qu'il n'y a pas d'argent infini, même pour le
            meilleur dossier du moment.
          </p>
        </div>

        <div class="fade-in">
          <h2>🧮 Le chiffre que personne ne regarde&nbsp;: 48,6&nbsp;% de marge brute</h2>

          <p>
            Dans les documents de l'introduction, il y a un ratio qui dit plus de choses que la capitalisation&nbsp;:
            la <strong>marge brute de 48,6&nbsp;%</strong>. Une entreprise de logiciels tourne d'ordinaire entre 70
            et 80&nbsp;%&nbsp;: une fois le produit écrit, chaque licence vendue coûte presque rien.
            Anthropic est à 48,6&nbsp;%&nbsp;: <strong>un dollar de revenu sur deux part en calcul</strong>.
          </p>

          <p>
            Ce n'est pas un défaut de gestion, c'est la nature du métier&nbsp;: vendre des tokens, c'est vendre des
            GPU à l'heure en les revendant au token. Anthropic est une entreprise d'infrastructure déguisée en
            éditeur de logiciels. Conséquence directe pour l'analyse&nbsp;: sa rentabilité ne dépend pas d'un effet
            de levier logiciel, mais du <strong>prix du calcul</strong> et du <strong>prix de vente du token</strong>
            — deux courbes qui, pour l'instant, vont dans le bon sens (le coût baisse), mais qui peuvent se
            retourner.
          </p>

          <p>
            À la clôture, la capitalisation représente <strong>18,7 fois</strong> le chiffre d'affaires annualisé du
            troisième trimestre, et <strong>29 fois</strong> au plus haut de la séance. Ce n'est pas absurde pour une
            société qui croît de 1&nbsp;200&nbsp;% par an&nbsp;: c'est simplement le prix d'un pari sur la
            <em>poursuite</em> de la croissance, pas sur la rentabilité d'aujourd'hui.
          </p>
        </div>

        <div class="fade-in">
          <h2>🏢 Ce que ça change pour une PME des Hautes-Alpes</h2>

          <p>
            Soyons clairs sur notre périmètre&nbsp;: nous ne donnons pas de conseil boursier, et nous n'achetons pas
            l'action ANT. Ce qui nous concerne, c'est l'IA que nos clients installent dans leur activité — et cette
            introduction dit trois choses utiles.
          </p>

          <p>
            <strong>Le prix de l'action n'est pas le prix du service.</strong> Ce qui compte pour une entreprise,
            ce n'est ni la capitalisation de son fournisseur ni le tarif affiché du million de tokens&nbsp;: c'est
            le <strong>coût par tâche réellement rendue</strong> — un devis trié, un mail résumé, une facture
            rapprochée. Un modèle deux fois plus cher mais deux fois plus fiable est moins cher à l'usage.
          </p>

          <p>
            <strong>Un fournisseur unique est un risque de contrat, pas seulement un risque technique.</strong>
            Une société cotée doit croître&nbsp;: elle peut changer ses tarifs, ses quotas ou ses conditions sans
            vous demander votre avis. Nous gardons donc une couche d'abstraction entre nos outils et le fournisseur,
            et nous testons régulièrement deux modèles sur les mêmes tâches. Ce n'est pas de la défiance&nbsp;:
            c'est de la gestion de dépendance, la même que pour l'hébergement ou le nom de domaine.
          </p>

          <p>
            <strong>La réversibilité se prépare avant, pas après.</strong> Vos données doivent rester exportables,
            vos prompts versionnés, vos coûts mesurés. Le jour où le fournisseur change de politique ou de prix,
            la question n'est pas «&nbsp;quel modèle est le meilleur&nbsp;» mais «&nbsp;combien de jours pour
            basculer&nbsp;».
          </p>

          <p>
            Et une réserve, puisque nous en mettons systématiquement&nbsp;: <strong>personne ne sait si cette
            valorisation tient</strong>. Nous ne le savons pas non plus. Ce que nous savons, c'est qu'un système
            construit pour survivre à un changement de fournisseur survit aussi à une correction de marché — et
            qu'un système construit sur un seul fournisseur ne survit à rien.
          </p>
        </div>

        <div class="highlight-box">
          <h3>🔑 Ce qu'il faut retenir</h3>
          <ul>
            <li>Le 19 novembre 2026, Anthropic a levé <strong>81,3&nbsp;milliards de dollars</strong> et signé la
            plus grosse introduction en bourse de l'histoire&nbsp;; l'action a clôturé à 97,17&nbsp;$, soit
            +17,1&nbsp;% — après avoir ouvert à +34&nbsp;%.</li>
            <li>Capitalisation à la clôture&nbsp;: <strong>1&nbsp;270&nbsp;milliards de dollars</strong>, soit
            1,27&nbsp;billion en français, après un pic de séance au-dessus de 2&nbsp;000&nbsp;milliards (2&nbsp;billions).</li>
            <li>Cinq ans entre la création (2021) et le Nasdaq&nbsp;: c'est la <strong>taille</strong> au moment de
            l'introduction qui est inédite, pas la vitesse — Amazon était entré en bourse trois ans après sa création.</li>
            <li>Une capitalisation n'est pas un PIB&nbsp;: elle mesure une opinion sur des profits futurs, pas une
            production annuelle. Anthropic «&nbsp;vaut plus que la Suisse&nbsp;» sur le papier&nbsp;; elle encaisse
            vingt-deux fois moins par an que l'État français.</li>
            <li>Le vrai signal&nbsp;: <strong>81 milliards levés en un jour</strong>, l'équivalent de six années du
            budget annuel d'Horizon Europe. C'est cela qui change le rapport de force, pas le classement.</li>
          </ul>
        </div>

        <div class="cta-box">
          <h3>Vous intégrez de l'IA dans votre entreprise&nbsp;?</h3>
          <p>
            Nous mesurons ce que l'IA vous coûte réellement par tâche, ce qu'elle remplace, et ce qui se passerait
            le jour où votre fournisseur change de prix ou de conditions. Premier échange gratuit, sans engagement.
          </p>
          <a href="/contact.html" class="btn">Faire le point sur mon usage de l'IA →</a>
        </div>

        <p style="font-size:0.85rem;color:var(--text-light);font-style:italic">
          Sources&nbsp;:
          <a href="{ANT}" target="_blank" rel="noopener">Anthropic prices initial public offering</a>, communiqué
          d'Anthropic, 18 novembre 2026 (83,00&nbsp;$ par action, 980&nbsp;millions d'actions de classe A dont
          956&nbsp;351&nbsp;354 vendues par la société, option de surallocation de 147&nbsp;millions, cotation
          Nasdaq Global Select sous le symbole ANT) ·
          <a href="{REU}" target="_blank" rel="noopener">Wall Street ends sharply lower as Anthropic's debut fails
          to revive AI trade</a>, Reuters, 19 novembre 2026 (pic à 2 000&nbsp;milliards de capitalisation, clôture
          à +17,1&nbsp;%, plus grosse introduction de l'histoire) ·
          <a href="{CNBC}" target="_blank" rel="noopener">Anthropic IPO raises over $81 billion in largest offering
          on record</a>, CNBC, 19 novembre 2026 ·
          <a href="{FOOL}" target="_blank" rel="noopener">Anthropic Just Started Trading. Here's What You Need to
          Know.</a>, The Motley Fool, 19 novembre 2026 (ouverture à 111,50&nbsp;$, amplitude 92,72–115,10&nbsp;$,
          clôture 97,17&nbsp;$, capitalisation 1 270&nbsp;milliards, chiffre d'affaires, marge brute de
          48,6&nbsp;%, sursouscription six fois) ·
          <a href="{FMI}" target="_blank" rel="noopener">PIB nominal 2026 par pays</a>, FMI, World Economic Outlook
          d'octobre 2026 (via Worldometer) ·
          <a href="{YAH}" target="_blank" rel="noopener">Anthropic seeks $1.4 trillion valuation in highly
          anticipated IPO</a>, Yahoo Finance, novembre 2026 (valorisation de 965&nbsp;milliards en mai 2026,
          fourchette initiale de 70 à 78&nbsp;$ sur 825&nbsp;millions d'actions) ·
          Cours de change du 19 novembre 2026&nbsp;: 1&nbsp;USD = 0,9098&nbsp;EUR (Frankfurter, taux de référence BCE).
          <br>Calculs (flottant, multiples, comparaisons historiques) réalisés à partir de ces sources&nbsp;; les
          comparaisons avec Apple (1980) et Amazon (1997) portent sur des montants non corrigés de l'inflation.
          <br>Cet article a été rédigé avec <strong>Hermes</strong>, l'agent open source que nous déployons pour nos clients.
        </p>
      </div>
    </article>
"""

CARD = f"""          <div class="card fade-in" style="text-align:left">
            <span style="font-size:0.8rem;color:var(--clay);font-weight:600">{CAT}</span>
            <h3 style="margin:8px 0">{TITLE}</h3>
            <p style="font-size:0.85rem">81,3 milliards de dollars levés, 1 270 milliards de capitalisation, et un Nasdaq qui perd 2,3 % le même jour. Ce que valent vraiment ces 2 000 milliards, ce que le mot « billion » veut dire en français, et pourquoi une entreprise n'est pas un État — chiffres à l'appui.</p>
            <p style="font-size:0.78rem;color:var(--text-light);margin-top:12px">19 novembre 2026 · {READ}</p>
            <a href="/{SLUG}" style="display:inline-block;margin-top:10px;font-size:0.85rem;color:var(--clay);font-weight:600;text-decoration:none">Lire l'article →</a>
          </div>

"""

SITEMAP = f"""  <url>
    <loc>{URL}</loc>
    <lastmod>{DATE}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
"""


def main():
    src = SRC.read_text(encoding='utf-8')
    i = src.index('</nav>') + len('</nav>')
    prefix = src[:i]
    suffix = src[src.index('    <footer class="footer">'):]

    prefix2, n = re.subn(r'(?s)<title>.*?</script>', NEW_HEAD, prefix, count=1)
    assert n == 1, "bloc <head> introuvable dans l'article source"

    out = prefix2 + MOBILE_CSS + '\n\n' + BODY.strip('\n') + '\n' + suffix
    OUT.write_text(out, encoding='utf-8')

    for tag in ('div', 'article', 'p', 'ul', 'ol', 'li', 'h2', 'h3', 'h4', 'blockquote', 'a', 'strong', 'em',
                'table', 'thead', 'tbody', 'tr', 'td', 'th'):
        o = len(re.findall(r'<%s[\s>]' % tag, out))
        c = len(re.findall(r'</%s>' % tag, out))
        if tag in ('td', 'th'):
            c += len(re.findall(r'<%s[^>]*/>' % tag, out))
        assert o == c, f"balise déséquilibrée {tag}: {o} ouvertes / {c} fermées"
    assert out.rstrip().endswith('</html>'), "document non fermé"

    # carte du blog (idempotent)
    blog = ROOT / 'blog.html'
    bh = blog.read_text(encoding='utf-8')
    if SLUG not in bh:
        anchor = '        <div class="grid">\n'
        assert bh.count(anchor) == 1, "point d'insertion de la carte introuvable"
        bh = bh.replace(anchor, anchor + CARD, 1)
        blog.write_text(bh, encoding='utf-8')
        print("carte ajoutée à blog.html")
    else:
        print("carte déjà présente")

    # sitemap (idempotent)
    sm = ROOT / 'sitemap.xml'
    sh = sm.read_text(encoding='utf-8')
    if URL not in sh:
        sh = sh.replace('  <url>\n    <loc>https://alpesdata.com/blog-panne-outlook',
                        SITEMAP + '  <url>\n    <loc>https://alpesdata.com/blog-panne-outlook', 1)
        sm.write_text(sh, encoding='utf-8')
        print("entrée ajoutée au sitemap")
    else:
        print("sitemap déjà à jour")

    print(f"OK {OUT.name} — {len(out)} octets, balises équilibrées, document fermé")


if __name__ == '__main__':
    main()
