# Hannie Consultants cc: company logo (redrawn)

The registered company logo, redrawn as a vector so it stays sharp at any
size. The design is unchanged: serif "H", HANNIE / CONSULTANTS, a navy inner
ring and a gold outer ring on cream. The HannieVerse trademark logo is
separate and is not covered here.

See `preview/compare-with-original.png` and `preview/versions.png`.

## What changed from the original

| | Original | Redrawn |
|---|---|---|
| File | 218 px image (blurs when enlarged) | Vector SVG, plus PNGs up to 2000 px |
| Navy | about `#172B44`, uneven | `#12294A` (the brand navy) |
| Gold | `#E6B262` | Two choices, see below |
| Cream | `#FCF9EF` | Same |
| "H" | Bold wedge serif | Merriweather Black, widened to match |
| HANNIE / CONSULTANTS | Bold sans | Montserrat Bold, both lines the same width |
| Versions | One | Badge, "H" only, wide, one colour, reversed |

## Choose a gold

- **original-gold** (`#E6B262`): keeps the lighter, warmer gold you have now.
- **site-gold** (`#C08A2E`): matches the website gold and the HannieVerse
  trademark logo, so the company and brand look related.

Once you choose, the other set of files can be deleted.

## Files

| File | Use |
|---|---|
| `svg/…-badge-*.svg`, `png/…-badge-*-2000.png` | Main logo: invoices, contracts, documents |
| `svg/…-lockup-*.svg`, `png/…-lockup-*-1600.png` | Wide version: letterhead, email signature, website footer |
| `svg/…-mark-*.svg`, `png/…-mark-*-512.png` | "H" only: social profile pictures, small spaces |
| `…-badge-navy-one-colour` | Stamps, black-and-white printing, embossing |
| `…-badge-white-reversed` | On navy or photo backgrounds |

All PNGs have transparent corners. For printers and designers, send the SVG.

## Rebuilding

`build.py` (with `glyphs.py` and the fonts in `fonts/`) regenerates the SVGs:
`pip install fonttools`, then `python3 build.py`, run from this folder.
Merriweather Black and Montserrat Bold are free fonts under the SIL Open Font License.
