#!/usr/bin/env python3
"""Génère blog-panne-outlook-microsoft-365.html à partir du dernier article publié.

Assemblage par découpe (skill alpesdata-client-sites, references/blog-articles.md §1) :
head/CSS/nav/footer identiques, seul le <head> SEO et le corps changent.
Corriger ICI, puis relancer : python3 tools/build-blog-panne-outlook.py
"""
import re
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / 'blog-rea-mcp-ingenierie-inverse.html'
OUT = ROOT / 'blog-panne-outlook-microsoft-365.html'

SLUG = 'blog-panne-outlook-microsoft-365.html'
URL = 'https://alpesdata.com/' + SLUG
TITLE = "Panne mondiale Outlook : ce qu'un jour sans Microsoft 365 dit de votre entreprise"
DESC = ("Depuis le 12 novembre au soir, Outlook, Teams et Copilot sont perturbés dans 74 pays. "
        "Ce que la panne révèle — et le point de fragilité qu'elle vous oblige à regarder en face.")

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
  "datePublished": "2026-11-13",
  "dateModified": "2026-11-13",
  "author": {{"@type": "Person", "name": "Didier Moranval-Vincent", "url": "https://alpesdata.com/"}},
  "publisher": {{"@type": "Organization", "name": "Alpesdata", "url": "https://alpesdata.com",
    "logo": {{"@type": "ImageObject", "url": "https://alpesdata.com/favicon-192.png"}}}}
}}
  </script>"""

FI = ("https://www.franceinfo.fr/internet/microsoft/"
      "une-panne-mondiale-touche-la-messagerie-outlook-de-microsoft-les-mesures-pour-la-resoudre-"
      "ne-fonctionnent-pas-comme-prevu_8280422.html")
NUM = ("https://www.numerama.com/tech/2373565-panne-de-microsoft-365-relancer-outlook-toutes-les-"
       "5-minutes-ne-sert-a-rien-ou-suivre-letat-du-service-en-temps-reel.html")

BODY = f"""
    <article class="article-page">
      <div class="article-container">
        <a href="/blog.html" class="back-link">← Retour au blog</a>

        <header class="article-header fade-in">
          <span class="article-category">☁️ Cloud &amp; Continuité d'activité</span>
          <h1>{TITLE}</h1>
          <div class="article-meta">
            <span>13 novembre 2026</span>
            <span>9 min de lecture</span>
            <span>#Outlook #Microsoft365 #Panne #Continuité #PME</span>
          </div>
          <p style="font-size:1.1rem;color:var(--text-light);line-height:1.7">
            Depuis le jeudi 12 novembre au soir, des dizaines de milliers d'utilisateurs n'ont plus accès à leur
            boîte Outlook, et Microsoft reconnaît ce vendredi que les mesures engagées <strong>«&nbsp;ne fonctionnent
            pas comme prévu&nbsp;»</strong>. Au-delà du désagrément, la panne pose une question très concrète à
            n'importe quelle entreprise, du cabinet médical à la PME de dix personnes&nbsp;: <strong>que reste-t-il de
            votre activité quand votre messagerie ne répond plus&nbsp;?</strong> Voici ce qui s'est passé, ce qu'il
            faut faire ce week-end, et ce que nous en tirons chez Alpesdata.
            (<a href="{FI}" target="_blank" rel="noopener">franceinfo avec AFP</a>)
          </p>
        </header>

        <div class="fade-in">
          <h2>📌 Les faits, sans jargon</h2>

          <p>
            La panne a commencé <strong>le 12 novembre en soirée</strong>. Elle touche Outlook, Teams et Copilot, et
            plus largement tout ce qui vient chercher du courrier ou de l'agenda chez Microsoft. Jeudi, le groupe
            assurait travailler «&nbsp;sans relâche&nbsp;»&nbsp;; vendredi, il indiquait sur X que ses correctifs ne
            produisaient pas l'effet attendu et qu'il cherchait des <strong>solutions alternatives</strong>.
          </p>

          <blockquote>
            «&nbsp;Nous avons confirmé que le problème pouvait toucher la connexion au service Microsoft&nbsp;365 pour
            tous les utilisateurs, dans n'importe quelle région du monde.&nbsp;»
            <br><strong>— Microsoft</strong>, cité par franceinfo le 12 novembre 2026.
          </blockquote>

          <p>
            Un dirigeant du groupe a ajouté sur le même réseau qu'<strong>«&nbsp;aucun signe d'action malveillante ou
            de cyberattaque&nbsp;»</strong> n'avait été détecté à ce stade. Autrement dit&nbsp;: ce n'est pas une
            attaque, c'est de l'ingénierie qui lâche — ce qui, pour la suite, est plutôt une bonne nouvelle.
          </p>

          <p>
            L'ampleur, maintenant. Selon Downdetector, les produits Microsoft ont été signalés en panne dans
            <strong>74 pays et territoires</strong>&nbsp;: Amériques, Europe, Asie, Afrique. Numerama relève environ
            <strong>150&nbsp;000 signalements</strong> pour Outlook aux États-Unis au pic de la panne. Le détail qui
            compte pour un dirigeant&nbsp;: la panne ne s'arrête pas à la boîte mail. Elle a aussi perturbé les
            <strong>assistants d'intelligence artificielle branchés sur un compte Microsoft</strong> pour lire les
            e-mails ou consulter l'agenda.
          </p>

          <p>
            Côté services publics, le réseau hospitalier de l'université de l'Iowa, privé de messagerie électronique
            <em>et</em> vocale, a demandé à ses patients de passer par son portail en ligne. Les compagnies IndiGo et
            CemAir ont signalé des perturbations de leurs services de messagerie&nbsp;; aucun transporteur n'a
            annoncé de vol affecté. Et franceinfo, qui sollicite ses lecteurs pour raconter leur journée, leur
            demande d'écrire à une adresse <strong>Gmail</strong> — en précisant, avec honnêteté, que la rédaction est
            elle aussi touchée.
          </p>

          <p>
            C'est la meilleure image de la journée&nbsp;: un média national qui bascule sur une boîte grand public
            pour continuer à recevoir du courrier. Ce n'est pas un aveu de faiblesse&nbsp;: c'est exactement ce que
            fait une organisation qui a <em>déjà</em> un plan de secours.
          </p>
        </div>

        <div class="fade-in">
          <h2>🔧 Pourquoi ça ne se répare pas d'un clic</h2>

          <p>
            Derrière Outlook, il y a un moteur&nbsp;: <strong>Exchange Online</strong>. C'est lui qui stocke les
            boîtes, répond aux clients de messagerie, alimente les agendas partagés — et sert de socle à Teams comme
            à Copilot. Quand ce socle vacille, tout ce qui s'y appuie vacille en même temps, dans le même ordre de
            grandeur de temps.
          </p>

          <p>
            Une panne de cette taille ne se répare pas comme un routeur qu'on débranche. Les serveurs sont remis en
            service <strong>par grappes</strong>&nbsp;: toutes les régions ne reviennent donc pas au même moment, et
            un utilisateur peut rester bloqué alors que son voisin est déjà rétabli. C'est aussi pour cela qu'un
            tableau de bord au vert ne garantit pas que votre boîte répond.
          </p>

          <div class="tech-box">
            <h4>La panne en une phrase</h4>
            <p>
              Des serveurs d'Exchange Online sont devenus brusquement indisponibles et les contrôles de santé
              échouent sur ces machines&nbsp;; la charge se reporte sur les serveurs restants et la remise en service
              se fait par vagues, région par région. Aucun correctif client — vider un cache, réinstaller Outlook,
              changer de mot de passe — n'y change quoi que ce soit.
              <br><em>Sources d'état à suivre&nbsp;: <a href="https://status.cloud.microsoft" target="_blank" rel="noopener">status.cloud.microsoft</a>
              et le compte <a href="https://x.com/MSFT365Status" target="_blank" rel="noopener">@MSFT365Status</a>.</em>
            </p>
          </div>

          <p>
            Numerama rappelle le seul réflexe utile&nbsp;: relancer Outlook toutes les cinq minutes ne sert à rien.
            Microsoft publie lui-même l'état de ses services, et le centre d'administration Microsoft&nbsp;365
            (rubrique «&nbsp;Service health&nbsp;») donne aux administrateurs un suivi plus fin encore.
          </p>

          <div class="stats-grid">
            <div class="stat-card">
              <span class="number">74</span>
              <span class="label">pays et territoires touchés<br>selon Downdetector (franceinfo, 13/11/2026)</span>
            </div>
            <div class="stat-card">
              <span class="number">≈ 150 000</span>
              <span class="label">signalements Outlook aux États-Unis<br>au pic de la panne (Downdetector via Numerama)</span>
            </div>
            <div class="stat-card">
              <span class="number">2<sup>e</sup> jour</span>
              <span class="label">sans rétablissement complet,<br>depuis le 12/11 au soir</span>
            </div>
            <div class="stat-card">
              <span class="number">6 / 6</span>
              <span class="label">sites que nous hébergeons en HTTP&nbsp;200<br>le 13/11/2026 à 11h28</span>
            </div>
          </div>
        </div>

        <div class="fade-in">
          <h2>⚠️ Le vrai sujet&nbsp;: votre messagerie tient tout le reste</h2>

          <p>
            Une boîte mail n'est pas un service parmi d'autres. C'est la <strong>clé passe-partout</strong> de votre
            système d'information. Le jour où elle tombe, voilà ce qui tombe avec elle, sans que personne ne l'ait
            décidé&nbsp;:
          </p>

          <ul>
            <li><strong>Les mots de passe.</strong> «&nbsp;Mot de passe oublié&nbsp;» envoie un lien par mail. Plus de
            mail, plus de réinitialisation.</li>
            <li><strong>La double authentification.</strong> Une grande partie des codes de sécurité arrivent encore
            par e-mail, parfois sur la boîte même dont on essaie de se connecter.</li>
            <li><strong>L'agenda et les rendez-vous.</strong> Outlook et Teams partagent le même socle&nbsp;: les
            créneaux et les invitations tombent en même temps que les mails.</li>
            <li><strong>Les pièces jointes qui font tourner l'entreprise.</strong> Factures fournisseurs, bons de
            commande, devis signés, relevés — tout ce qui arrive par mail et qu'on ne retrouve plus nulle part
            ailleurs.</li>
            <li><strong>Les automatisations et l'IA.</strong> Les assistants branchés sur la boîte pour trier, résumer
            ou lire l'agenda se sont tus en même temps qu'elle, comme l'a relevé franceinfo.</li>
          </ul>

          <p>
            Le problème n'est pas Microsoft, et ce n'est pas non plus le cloud. C'est la <strong>concentration</strong>&nbsp;:
            un seul compte qui tient le courrier, l'agenda, la visioconférence, les fichiers et désormais l'IA. Quand
            la brique du milieu casse, tout le reste s'arrête à la même seconde, et personne ne sait plus par quel
            bout reprendre.
          </p>

          <blockquote>
            <strong>Ce n'est pas la panne qui coûte cher. C'est le nombre de choses dont on découvre, ce jour-là,
            qu'elles en dépendaient.</strong>
          </blockquote>
        </div>

        <div class="fade-in">
          <h2>✅ Ce qu'il faut faire maintenant</h2>

          <p>
            Cinq gestes, dans l'ordre. Les quatre premiers tiennent dans la journée&nbsp;; le cinquième est un
            rendez-vous à prendre avec soi-même.
          </p>

          <ol>
            <li><strong>Arrêtez de relancer Outlook toutes les cinq minutes.</strong> Suivez
            <a href="https://status.cloud.microsoft" target="_blank" rel="noopener">status.cloud.microsoft</a> et
            @MSFT365Status&nbsp;: vous saurez où en est la reprise, région par région, au lieu de le deviner.</li>
            <li><strong>Essayez les autres portes.</strong> Le web (outlook.com ou outlook.office.com), l'application
            mobile, un autre appareil&nbsp;: il est fréquent qu'un client de bureau reste bloqué alors que la version
            web répond déjà. Un accès qui marche, c'est un mail urgent qui part.</li>
            <li><strong>Sortez la liste de vos accès critiques.</strong> Vingt minutes et une feuille&nbsp;: quels
            comptes se réinitialisent par mail, quelles doubles authentifications passent par la boîte, quels
            prestataires vous écrivent uniquement là. C'est votre vraie carte de dépendance.</li>
            <li><strong>Ouvrez — et testez — un canal de secours.</strong> Une adresse chez un autre fournisseur que
            Microsoft, une règle de transfert pour les urgences, les numéros de téléphone des cinq personnes qui
            comptent. Envoyez-vous un mail de test <em>aujourd'hui</em>&nbsp;: un plan de secours non testé n'est
            pas un plan de secours, c'est une intention.</li>
            <li><strong>Gardez une copie locale de vos mails.</strong> Un export mensuel de la boîte (PST/OST côté
            Outlook, archive .eml ou .mbox ailleurs) sur un disque ou dans un Nextcloud. «&nbsp;Mes mails sont chez
            Microsoft&nbsp;» veut dire, littéralement&nbsp;: «&nbsp;mes mails sont chez quelqu'un d'autre&nbsp;».</li>
          </ol>

          <p>
            Si vous ne faites qu'une seule chose aujourd'hui&nbsp;: ouvrez votre boîte de secours et envoyez-vous un
            mail. C'est cinq minutes, et c'est le seul point de cette liste que la panne ne peut pas vous empêcher de
            faire.
          </p>
        </div>

        <div class="fade-in">
          <h2>🏢 Ce qu'Alpesdata fait — et ce qu'elle ne promet pas</h2>

          <p>
            <strong>Mesure, pas promesse.</strong> Le vendredi 13 novembre 2026 à 11h28, nous avons sondé les sites
            que nous concevons et hébergeons&nbsp;: alpesdata.com, massagepro.fr, ma-therapie.fr, foundation.immo,
            alice.moranval.com et hautes-alpes-immo.com. <strong>Six sur six ont répondu HTTP&nbsp;200</strong>, en 27
            à 180&nbsp;millisecondes, servis par nginx. Aucun d'eux n'a besoin de Microsoft&nbsp;365 pour s'afficher.
          </p>

          <p>
            La raison est architecturale, pas magique. Ce sont des sites <strong>statiques</strong>&nbsp;:
            HTML, CSS et JavaScript, <strong>zéro fichier PHP</strong> dans nos dépôts, pas de session, pas de base de
            données interrogée côté visiteur, rien à exécuter. Une panne de messagerie ne peut pas éteindre une page
            qui ne parle pas à une messagerie. Et notre propre courrier ne passe pas par Exchange Online&nbsp;: les
            enregistrements MX de nos domaines pointent ailleurs — la panne Outlook ne nous coupe donc pas le mail,
            ce qui n'était pas acquis d'avance.
          </p>

          <p>
            Maintenant les limites, parce qu'elles viennent avant les promesses. <strong>Nous ne dirons jamais
            «&nbsp;zéro dépendance&nbsp;»&nbsp;: c'est faux.</strong> Nos sites dépendent du registrar qui tient le
            nom de domaine, de notre hébergeur, du DNS, du certificat TLS, et de services tiers pour l'affichage des
            polices ou la mesure d'audience. Une panne chez l'un d'eux nous toucherait aussi, et nous ne prétendrons
            pas le contraire. Ce que nous promettons est plus petit et plus utile&nbsp;: une dépendance
            <strong>connue, courte et documentée</strong> — la liste écrite noir sur blanc, une copie du site quelque
            part, et une procédure de bascule que l'on a déjà exécutée une fois.
          </p>

          <p>
            Et une position, puisque la question nous est posée à chaque incident de ce genre&nbsp;: <strong>cette
            panne ne nous réjouit pas</strong>. Les outils de Microsoft sont bons, nous les utilisons quand ils sont
            le meilleur choix pour un client. Ce que nous refusons, c'est de laisser un même fournisseur tenir, sans
            le dire, le courrier, l'agenda, les fichiers et l'IA d'une même entreprise. Le cloud des autres est
            excellent — jusqu'au jour où il tombe, et ce jour-là, ce qui compte est ce que vous aviez prévu.
          </p>
        </div>

        <div class="highlight-box">
          <h3>🔑 Ce qu'il faut retenir</h3>
          <ul>
            <li>Depuis le 12 novembre au soir, Outlook, Teams et Copilot sont perturbés&nbsp;; Microsoft reconnaît
            vendredi que ses mesures «&nbsp;ne fonctionnent pas comme prévu&nbsp;».</li>
            <li>Aucun signe d'action malveillante ou de cyberattaque n'a été détecté à ce stade, selon Microsoft.</li>
            <li>Le risque réel n'est pas la panne&nbsp;: c'est la concentration — une boîte qui tient les mots de
            passe, la double authentification, l'agenda et l'IA.</li>
            <li>Un canal de secours testé aujourd'hui vaut mieux qu'un plan de continuité dans un tiroir.</li>
            <li>Nos six sites répondaient en HTTP&nbsp;200 le 13/11 à 11h28, sans dépendance à
            Microsoft&nbsp;365&nbsp;: c'est une mesure datée, pas un slogan.</li>
          </ul>
        </div>

        <div class="cta-box">
          <h3>Votre entreprise tiendrait-elle debout sans sa messagerie&nbsp;?</h3>
          <p>
            Nous listons vos dépendances réelles — nom de domaine, hébergement, mail, sauvegardes — et ce qu'il
            faudrait pour continuer à travailler le jour où l'une d'elles tombe. Premier échange gratuit, sans
            engagement.
          </p>
          <a href="/contact.html" class="btn">Faire le point sur mes dépendances →</a>
        </div>

        <p style="font-size:0.85rem;color:var(--text-light);font-style:italic">
          Sources&nbsp;:
          <a href="{FI}" target="_blank" rel="noopener">Une panne mondiale touche la messagerie Outlook de Microsoft,
          « aucun signe d'action malveillante ou de cyberattaque » n'a été détecté à ce stade</a>, franceinfo avec AFP,
          13 novembre 2026 (périmètre Microsoft&nbsp;365, 74 pays selon Downdetector, Iowa, IndiGo, CemAir, assistance
          IA) ·
          <a href="{NUM}" target="_blank" rel="noopener">Panne de Microsoft&nbsp;365&nbsp;: relancer Outlook toutes les
          5 minutes ne sert à rien</a>, Numerama, 13 novembre 2026 à 09h55 (signalements Downdetector, reprise par
          grappes, status.cloud.microsoft et @MSFT365Status) ·
          <a href="https://status.cloud.microsoft" target="_blank" rel="noopener">status.cloud.microsoft</a>, tableau de
          bord officiel de Microsoft (état publié, dernière consultation le 13/11/2026) ·
          Mesures Alpesdata du 13/11/2026 à 11h28&nbsp;: requêtes HTTP sur six domaines (codes 200, 27–180&nbsp;ms,
          serveur nginx) et absence de fichier PHP dans nos dépôts.
          <br>Cet article a été rédigé avec <strong>Hermes</strong>, l'agent open source que nous déployons pour nos clients.
        </p>
      </div>
    </article>
"""


def main():
    src = SRC.read_text(encoding='utf-8')
    i = src.index('</nav>') + len('</nav>')
    prefix = src[:i]
    suffix = src[src.index('    <footer class="footer">'):]

    prefix2, n = re.subn(r'(?s)<title>.*?</script>', NEW_HEAD, prefix, count=1)
    assert n == 1, "bloc <head> introuvable dans l'article source"

    out = prefix2 + '\n\n' + BODY.strip('\n') + '\n' + suffix
    OUT.write_text(out, encoding='utf-8')

    # contrôles d'équilibre
    for tag in ('div', 'article', 'p', 'ul', 'ol', 'li', 'h2', 'h3', 'h4', 'blockquote', 'a', 'strong', 'em'):
        o = len(re.findall(r'<%s[\s>]' % tag, out))
        c = len(re.findall(r'</%s>' % tag, out))
        assert o == c, f"balise déséquilibrée {tag}: {o} ouvertes / {c} fermées"
    assert out.rstrip().endswith('</html>'), "document non fermé"
    print(f"OK {OUT.name} — {len(out)} octets, balises équilibrées, document fermé")


if __name__ == '__main__':
    main()
