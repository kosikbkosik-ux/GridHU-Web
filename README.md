# GridHU-Web

A GridHU statikus webes otthona: Android-alkalmazásbemutató, három adatértelmező útmutató, kapcsolat és adatvédelem.

## Technológia

- statikus HTML és CSS;
- nincs frontend build toolchain, futtatható JavaScript, külső font, cookie, analytics vagy tracker;
- a JSON-LD kizárólag valós WebSite/WebPage metaadat; nincs kitalált értékelés vagy rich result ígéret;
- GitHub Pagesen fut.

## Helyi megnyitás

A projektútvonalhoz kötött erőforrások miatt HTTP-previewt használj. A repository gyökerében, Python 3.9+ verzióval:

```text
python .github/scripts/serve_site.py
```

Ezután nyisd meg a `http://127.0.0.1:8000/GridHU-Web/` címet. Csak a loopback interfészen, a publikus fájllistát szolgálja ki; nincs API-hívás vagy adatgyűjtés. Leállítás: Ctrl+C.

## Oldalak

- Kezdőlap: <https://kosikbkosik-ux.github.io/GridHU-Web/>
- Adatvédelem: <https://kosikbkosik-ux.github.io/GridHU-Web/privacy/>
- Kapcsolat: <https://kosikbkosik-ux.github.io/GridHU-Web/contact/>
- Áramtermelés és mix: <https://kosikbkosik-ux.github.io/GridHU-Web/aramtermeles/>
- Paks adatainak értelmezése: <https://kosikbkosik-ux.github.io/GridHU-Web/paks/>
- Import–export: <https://kosikbkosik-ux.github.io/GridHU-Web/import-export/>
- Sitemap: <https://kosikbkosik-ux.github.io/GridHU-Web/sitemap.xml>

Az adatvédelmi tájékoztató a [privacy/index.html](privacy/index.html) fájlban módosítható.

## GitHub Pages deployment

A [deploy-pages.yml](.github/workflows/deploy-pages.yml) workflow `main` pushra vagy kézi indításra publikál. A PR ellenőrző workflow nem deployol. A deployment előtt a Python-ellenőrző lefut, majd az explicit publikus fájllistából friss `_site` staging mappa készül. Kizárólag ez kerül a Pages artifactba; README, tesztek és belső jegyzetek nem. Nincs új szolgáltatás vagy frontend buildfüggőség.

A canonical és sitemap címek a jelenlegi HTTPS projektcímre mutatnak; az `index.html` változat canonicalja a perjeles oldal. A navigáció és erőforrások a `/GridHU-Web/` projektútvonalat használják. Domainváltáskor mindkettőt tudatosan át kell vezetni. Nincs projekt alatti `robots.txt`: az a host gyökerének szabályait nem helyettesítené. Sitemap-beküldés és Search Console-igazolás külön hozzáféréssel és élesítés után végezhető.

## Ellenőrzés

```text
python .github/scripts/check_site.py
python .github/scripts/prepare_site.py
python .github/scripts/check_site.py _site
```

A staging üres, új célmappát igényel. A teszt ellenőrzi a belső URL-eket és fragmentumokat, a projektútvonalat, a címek egyediségét, canonicalt, sitemapet, JSON-LD-t és a véletlen indexelési tiltást. Külső oldalak elérhetőségét, Google-indexelést, Lighthouse-eredményt vagy fizikai Android-működést nem bizonyít.

## Alkalmazásképek és bolti hivatkozás

A kezdőlap a [nyilvános magyar Google Play-adatlapra](https://play.google.com/store/apps/details?id=com.kosikbotond.gridhu&hl=hu) mutat; a telepíthetőséget a Play dönti el. Az `assets/app-*.png` képek az adatlap valódi alkalmazásképernyői, ellenőrizve 2026-10-29-én. A rögzített értékek bemutatók; a képeket nem szabad aktuális mérésként értelmezni. A `social-card.png` saját statikus megosztási grafika, nem appképernyő.

A webes bemutató nem helyettesíti a Google Play leírását vagy az elsődleges adatforrást. A szakmai oldalak forrásjegyzéke és ellenőrzési dátuma az oldalak alján található. A meglévő adatvédelmi nyilatkozat törzse nem marketingtartalom.

## Adatvédelem

A site nem tölt be külső fontot, analitikát, cookie-t, trackert vagy hirdetési kódot.
