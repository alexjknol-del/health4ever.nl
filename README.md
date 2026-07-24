# Health4Ever

Statische website voor de gezondheidsgids **health4ever.nl**. Gehost op Cloudflare Pages.

## Structuur

- `public/` — de kant-en-klare website (dit is de map die Cloudflare Pages publiceert)
- `build.py` — sitegenerator die `public/` opbouwt
- `content_articles.py` — de artikelcontent
- `assets_src/` — bronbestanden voor CSS en illustraties

## Bouwen

```bash
python3 build.py
```

De output verschijnt in `public/`.

## Cloudflare Pages

- Build command: *(leeg)*
- Build output directory: `public`
- Framework preset: None

De site bevat geen build-stap op Cloudflare: de HTML in `public/` wordt rechtstreeks geserveerd.
