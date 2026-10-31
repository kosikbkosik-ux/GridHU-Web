# GridHU-Web

A GridHU statikus webes otthona: Android-alkalmazásbemutató, három adatértelmező útmutató, kapcsolat és adatvédelem.

## Technológia

- statikus HTML és CSS;
- nincs frontend build toolchain, futtatható JavaScript, külső font, cookie, analytics vagy tracker;
- a JSON-LD kizárólag valós WebSite/WebPage metaadat; nincs kitalált értékelés vagy rich result ígéret;
- GitHub Pagesen fut.

## Helyi megnyitás

A gyökérhez kötött erőforrások miatt HTTP-previewt használj. A repository gyökerében, Python 3.9+ verzióval:

```text
python .github/scripts/serve_site.py
```

Ezután nyisd meg a `http://127.0.0.1:8000/` címet. A preview a saját domain `/` gyökerét modellezi. Csak a loopback interfészen, a publikus fájllistát szolgálja ki GET és HEAD kérésre is; nincs API-hívás vagy adatgyűjtés. Leállítás: Ctrl+C.

## Oldalak

- Kezdőlap: <https://gridhu.hu/>
- Adatvédelem: <https://gridhu.hu/privacy/>
- Kapcsolat: <https://gridhu.hu/contact/>
- Áramtermelés és mix: <https://gridhu.hu/aramtermeles/>
- Paks adatainak értelmezése: <https://gridhu.hu/paks/>
- Import–export: <https://gridhu.hu/import-export/>
- Sitemap: <https://gridhu.hu/sitemap.xml>
- Robots: <https://gridhu.hu/robots.txt>

Az adatvédelmi tájékoztató a [privacy/index.html](privacy/index.html) fájlban módosítható.

## GitHub Pages deployment

A [deploy-pages.yml](.github/workflows/deploy-pages.yml) workflow `main` pushra vagy kézi indításra publikál. A PR ellenőrző workflow nem deployol. A deployment előtt a Python-ellenőrző lefut, majd az explicit publikus fájllistából friss `_site` staging mappa készül. Kizárólag ez kerül a Pages artifactba; README, tesztek és belső jegyzetek nem. Nincs új szolgáltatás vagy frontend buildfüggőség.

A canonical, Open Graph, Twitter-kép, JSON-LD és sitemap címek a `https://gridhu.hu/` célcímre mutatnak; az `index.html` változat canonicalja a perjeles oldal. A belső navigáció és az erőforrások a saját domain `/` gyökerét használják. A `robots.txt` így a host gyökerében szolgálható ki; engedi a feltérképezést és megadja az új sitemap címét. A 404-oldal `noindex` jelölése megmarad, és nem szerepel a sitemapben.

Az explicit publikus allowlist **15 fájlt** tartalmaz a robots fájllal együtt. A régi projektútvonalhoz nem készül második, duplikált oldalfa. A régi GitHub Pages URL-ek átirányítását, a saját domain beállítását, a DNS-t és a HTTPS-t az éles kiadáskor külön kell igazolni: ezeket a kódbeli átvezetés és a helyi teszt nem bizonyítja.

A saját domain a GitHub Pages repository-beállításában adható meg. [Egyéni GitHub Actions publikálásnál nincs szükség `CNAME` fájlra](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site); meglévő ilyen fájlt a GitHub figyelmen kívül hagy. A workflow és a staging ezért nem hoz létre `CNAME` fájlt. Sitemap-beküldés és Search Console-igazolás megfelelő hozzáféréssel, az éles új URL-ek ellenőrzése után végezhető. A [Google robots útmutatója](https://developers.google.com/search/docs/crawling-indexing/robots/create-robots-txt) szerint a robots fájl a host gyökerébe tartozik. Dokumentációellenőrzés: 2026-10-31.

## Ellenőrzés

```text
python .github/scripts/check_site.py
python .github/scripts/prepare_site.py
python .github/scripts/check_site.py _site
```

A staging üres, új célmappát igényel. A teszt ellenőrzi a belső URL-eket és fragmentumokat, a saját domain gyökerét, a régi projektcím hiányát, a címek egyediségét, canonicalt, megosztási metaadatokat, sitemapet, JSON-LD-t, robots szabályokat és a véletlen indexelési tiltást. Külső oldalak elérhetőségét, éles domainbeállítást, Google-indexelést, Lighthouse-eredményt vagy fizikai Android-működést nem bizonyít.

## Alkalmazásképek és bolti hivatkozás

A kezdőlap a [nyilvános magyar Google Play-adatlapra](https://play.google.com/store/apps/details?id=com.kosikbotond.gridhu&hl=hu) mutat; a telepíthetőséget a Play dönti el. Az `assets/app-*.png` képek az adatlap valódi alkalmazásképernyői, ellenőrizve 2026-10-29-én. A rögzített értékek bemutatók; a képeket nem szabad aktuális mérésként értelmezni. A `social-card.png` saját statikus megosztási grafika, nem appképernyő.

A webes bemutató nem helyettesíti a Google Play leírását vagy az elsődleges adatforrást. A szakmai oldalak forrásjegyzéke és ellenőrzési dátuma az oldalak alján található. A meglévő adatvédelmi nyilatkozat törzse nem marketingtartalom.

## Adatvédelem

A site nem tölt be külső fontot, analitikát, cookie-t, trackert vagy hirdetési kódot.
