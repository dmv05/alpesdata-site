#!/usr/bin/env python3
"""Correctif mobile des articles de blog alpesdata.com (idempotent).

Deux défauts du gabarit, mesurés à 390 px :
 1. .article-page .stats-grid passe en `1fr 1fr` sous 768 px → cartes de 163 px sur
    mobile, texte étranglé. On force une colonne sous 560 px et on réduit les paddings.
 2. Les titres d'encadré écrits en <h4> dans .cta-box / .highlight-box ne sont pas
    stylés par le gabarit (seuls h2/h3 le sont) → passage en <h3>.

Usage : python3 tools/mobile-fix-blog.py [fichier.html ...]
Sans argument : tous les blog-*.html de la racine du dépôt.
"""
import glob
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
MARK = '<!-- mobile-fix-blog -->'
CSS = MARK + '''
    <style>
@media(max-width:560px){
  .article-page{padding:36px 16px}
  .article-page .stats-grid{grid-template-columns:1fr}
  .article-page .stat-card{padding:18px}
  .article-page .stat-card .number{font-size:1.6rem}
  .article-page .cta-box,.article-page .highlight-box,.article-page .tech-box{padding:22px}
  .article-page blockquote{padding:20px}
}
    </style>'''

H4_BOX = re.compile(r'(<div class="(?:cta-box|highlight-box)"[^>]*>\s*)<h4>(.*?)</h4>', re.S)
MARK_FALLBACK = '<!-- mobile-fix-fallback -->'
FALLBACK = MARK_FALLBACK + """<style>
/* Filet de sécurité : un bloc .fade-in plus haut que 10x l'écran ne franchit jamais le
   seuil 0.1 d'IntersectionObserver sur téléphone, et le corps de l'article reste invisible.
   Ici le contenu devient visible seul au bout de 2,5 s, même si l'observer ne se déclenche pas. */
@keyframes fade-in-fallback{to{opacity:1;transform:none}}
.article-page .fade-in{animation:fade-in-fallback .01s linear 2.5s forwards}
</style>"""

TAGS = ('div', 'article', 'p', 'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'blockquote', 'a',
        'strong', 'em', 'table', 'thead', 'tbody', 'tr', 'td', 'th')


def check(t, name):
    for tag in TAGS:
        o = len(re.findall(r'<%s[\s>]' % tag, t))
        c = len(re.findall(r'</%s>' % tag, t))
        if tag in ('td', 'th'):
            c += len(re.findall(r'<%s[^>]*/>' % tag, t))
        assert o == c, f"{name}: balise déséquilibrée {tag}: {o}/{c}"
    assert t.rstrip().endswith('</html>'), f"{name}: document non fermé"


def fix(path):
    p = pathlib.Path(path)
    t = p.read_text(encoding='utf-8')
    notes = []

    if 'max-width:560px' not in t:
        assert t.count('</nav>') >= 1, f"{p.name}: pas de </nav>"
        t = t.replace('</nav>', '</nav>' + CSS, 1)
        notes.append('CSS mobile')
    else:
        notes.append('CSS déjà présent')

    if 'fade-in-fallback' not in t:
        t = t.replace('</head>', FALLBACK + '\n</head>', 1)
        notes.append('filet anti-page-vide')

    t2, n = H4_BOX.subn(r'\1<h3>\2</h3>', t)
    if n:
        t = t2
        notes.append(f'{n} h4→h3')

    check(t, p.name)
    if all(x in ('CSS déjà présent',) for x in notes) and not n and 'filet anti-page-vide' not in notes:
        print(f"  {p.name:46s} inchangé")
        return False
    p.write_text(t, encoding='utf-8')
    print(f"  {p.name:46s} " + ', '.join(notes))
    return True


def main():
    args = sys.argv[1:]
    files = args if args else sorted(glob.glob(str(ROOT / 'blog-*.html')))
    changed = 0
    print("Correctif mobile des articles :")
    for f in files:
        changed += bool(fix(f))
    print(f"\n{changed} fichier(s) modifié(s)")


if __name__ == '__main__':
    main()
