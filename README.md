# GridHU-Web

A GridHU egyszerű, statikus webes otthona. Elsődleges célja a GridHU Android-alkalmazás publikus adatvédelmi tájékoztatójának kiszolgálása.

## Technológia

- statikus HTML és CSS;
- nincs build toolchain, JavaScript, külső font, cookie, analytics vagy tracker;
- GitHub Pagesen fut.

## Helyi megnyitás

A `index.html` fájl közvetlenül megnyitható böngészőben. Egyszerű helyi HTTP-kiszolgálóhoz például a repository gyökerében futtatható:

```text
python -m http.server 8000
```

Ezután nyisd meg a `http://localhost:8000/` címet.

## Oldalak

- Kezdőlap: <https://kosikbkosik-ux.github.io/GridHU-Web/>
- Adatvédelem: <https://kosikbkosik-ux.github.io/GridHU-Web/privacy/>
- Kapcsolat: <https://kosikbkosik-ux.github.io/GridHU-Web/contact/>

Az adatvédelmi tájékoztató a [privacy/index.html](privacy/index.html) fájlban módosítható.

## GitHub Pages deployment

A [deploy-pages.yml](.github/workflows/deploy-pages.yml) workflow minden `main` ágra történő push után a hivatalos GitHub Pages actionökkel publikálja a teljes statikus site-ot. Nincs szükség secretre vagy build-lépésre.

A belső linkek relatívak, ezért a site GitHub project Pages base path alatt (`/GridHU-Web/`) is működik.

## Adatvédelem

A site nem tölt be külső fontot, analitikát, cookie-t, trackert vagy hirdetési kódot.
