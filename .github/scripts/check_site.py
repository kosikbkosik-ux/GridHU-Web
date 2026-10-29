"""Dependency-free static site checks. No external requests or production writes."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote
import json
import sys
import xml.etree.ElementTree as ET

BASE = 'https://kosikbkosik-ux.github.io/GridHU-Web/'
ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[2]
EXPECTED = {'', 'privacy/', 'contact/', 'aramtermeles/', 'paks/', 'import-export/'}

class Document(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.tags=[]; self.ids=set(); self.refs=[]; self.metas={}; self.canon=[]
        self.titles=[]; self.jsons=[]; self.capture=None; self.buffer=''
        self.errors=[]; self.source=source
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        a=dict(attrs); self.tags.append((tag,a))
        if 'id' in a:
            if a['id'] in self.ids: self.errors.append('duplicate ID '+a['id'])
            self.ids.add(a['id'])
        if tag=='html' and a.get('lang')!='hu': self.errors.append('lang must be hu')
        if tag=='meta': self.metas[a.get('name',a.get('property'))]=a.get('content','')
        if tag=='link' and a.get('rel')=='canonical': self.canon.append(a.get('href'))
        if tag in ('a','link') and a.get('href'): self.refs.append(a['href'])
        if tag in ('img','source') and a.get('src'): self.refs.append(a['src'])
        if tag=='img' and (not a.get('alt') or not a.get('width') or not a.get('height')):
            self.errors.append('image needs alt and explicit dimensions')
        if tag=='title': self.capture='title'; self.buffer=''
        if tag=='script':
            if a.get('type')!='application/ld+json' or 'src' in a:
                self.errors.append('unexpected executable or external script')
            self.capture='json';self.buffer=''
        for key in a:
            if key.startswith('on'): self.errors.append('inline event handler')

    def handle_data(self,data):
        if self.capture: self.buffer+=data

    def handle_endtag(self,tag):
        if tag=='title' and self.capture=='title': self.titles.append(self.buffer.strip());self.capture=None
        if tag=='script' and self.capture=='json':
            try: self.jsons.append(json.loads(self.buffer))
            except ValueError: self.errors.append('invalid JSON-LD')
            self.capture=None

errors=[]; docs={};titles=[];descriptions=[]
def check(ok,message):
    if not ok: errors.append(message)

for f in sorted(ROOT.rglob('*.html')):
    if any(p.startswith('.') or p=='_site' for p in f.relative_to(ROOT).parts): continue
    rel=f.relative_to(ROOT).as_posix()
    d=Document(f.read_text(encoding='utf-8')); docs[rel]=d
    for e in d.errors: errors.append(rel+': '+e)
    check(sum(t=='h1' for t,a in d.tags)==1,rel+': exactly one H1 required')
    check(sum(t=='main' for t,a in d.tags)==1,rel+': exactly one main required')
    check(len(d.titles)==1 and d.titles[0],rel+': title required')
    check(bool(d.metas.get('description')),rel+': description required')
    check('viewport' in d.metas,rel+': viewport required')
    if rel=='404.html':
        check(d.metas.get('robots')=='noindex','404 must not be indexed')
        continue
    path=rel.removesuffix('index.html')
    check(path in EXPECTED,rel+': unexpected indexable HTML')
    check(d.canon==[BASE+path],rel+': wrong canonical')
    check('noindex' not in d.metas.get('robots','').lower(),rel+': accidental noindex')
    check(d.metas.get('og:url')==BASE+path,rel+': OG URL mismatch')
    check(d.metas.get('og:image')==BASE+'assets/social-card.png',rel+': OG image mismatch')
    titles+=d.titles;descriptions.append(d.metas.get('description'))
    for item in d.jsons:
        check(item.get('@context')=='https://schema.org',rel+': invalid schema context')
        check(item.get('@type') in ('WebSite','WebPage'),rel+': unexpected schema type')
        check(item.get('url')==BASE+path and item.get('inLanguage')=='hu',rel+': schema identity mismatch')
        check(not any(k in json.dumps(item) for k in ('aggregateRating','reviewCount','offers','softwareVersion')),rel+': unsupported app facts')

check(len(titles)==len(set(titles)),'duplicate page titles')
check(len(descriptions)==len(set(descriptions)),'duplicate descriptions')
for rel,d in docs.items():
    url=BASE+rel
    for ref in d.refs:
        target=urlsplit(urljoin(url,ref))
        if target.scheme in ('mailto','tel'): continue
        if target.netloc!=urlsplit(BASE).netloc: continue
        check(target.path.startswith('/GridHU-Web/'),f'{rel}: escaped project path {ref}')
        name=unquote(target.path.removeprefix('/GridHU-Web/'))
        if name.endswith('/') or not name: name+='index.html'
        check((ROOT/name).is_file(),f'{rel}: missing local target {ref}')
        if target.fragment and name in docs:
            check(unquote(target.fragment) in docs[name].ids,f'{rel}: missing fragment {ref}')

ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
sitemap=ET.parse(ROOT/'sitemap.xml')
locations=[e.text for e in sitemap.findall('s:url/s:loc',ns)]
check(set(locations)=={BASE+p for p in EXPECTED} and len(locations)==len(EXPECTED),'sitemap URL set mismatch')
check((ROOT/'assets/social-card.png').is_file(),'missing sharing image')
check(not (ROOT/'robots.txt').exists(),'project robots file would not control host root')
css=(ROOT/'assets/styles.css').read_text(encoding='utf-8')
check('@import' not in css and 'url(' not in css,'unexpected external CSS dependency')
if errors:
    print('\n'.join('FAIL '+e for e in errors));sys.exit(1)
print(f'PASS: {len(docs)} HTML documents; {len(locations)} sitemap URLs; local links/fragments, metadata, JSON-LD, assets, project path and static-only checks')
