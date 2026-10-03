# Handoff: hannieverse.com website work

Branch: `claude/upbeat-faraday-sjwbci` (repo `pyhannie-ops/Honour-Diagnostic`). Everything below lives in `qa/`.

## Context
Website for Hannie Consultants cc (HannieVerse Enterprise™). The Honour™ Diagnostic launches **14 October 2026**; Flow™ and SoftPower™ follow. The HFS Arc (Honour™, Flow™, SoftPower™) is the business model. The owner edits the site in Wix herself, so the work is page mock-ups, copy and assets she can apply there. The owner is not a coder: give plain steps, not code.

## What exists
| File / folder | What it is |
|---|---|
| `Website-Fix-and-Improve-List.docx` | Printable fix and improve checklist, plus approved FAQ copy and session copy. Built by `make_fix_checklist.py`. |
| `Website-Check-Hannieverse.docx` | One-page manual QA checklist (laptop and phone). Built by `make_checklist.py`. |
| `honour-page-mockup.html` | Honour page mock-up (hero, how it works, sample report, pricing, "Before you decide" FAQ). |
| `homepage-mockup.html` | Homepage mock-up (Why Us slideshow, 10 s per slide, pause/play). |
| `sample-report/` | Rewritten sample Honour Report (docx, pdf, previews). Built by `make_sample_report.py`. |
| `infographic/` | One-page report infographic. `report-infographic-v4-*.png` is the final one (older versions can be deleted). |
| `logo/` | Circular HannieVerse emblem (original artwork) and lockups with wordmark. |
| `site-qa.js`, `README.md` | Optional Playwright QA script (not needed by the owner). |

## Decisions to keep
- **Voice:** "we" and "you". No first-person "I" on the site.
- **Honour™ facts:**
  - Three online sessions of 90 minutes: Tuesday, Friday, the following Wednesday.
  - Two private reflections of about 15 minutes, sent by email link after Sessions 1 and 2, due the day before the next session.
  - 5 to 9 participants. From $441 per participant (9 people) to $705 (5 people); $3,525 to $3,969 total. USD base; GBP, EUR, ZAR available. 50% deposit, 50% on report delivery.
  - Report within **5 business days** (the Brief still says 3: needs updating).
  - Gifts of Clarity for every participant; individual reports for participants; anonymised sponsor report.
  - Sponsor attends sessions only if participants agree.
  - Honour™ **recommends, it does not implement.** The word to use is "recommendations".
- **Anonymity:** no names, functions or roles attached to any finding. A theme is included only if at least three participants raised it (proposed rule: confirm with the owner).
- **Style:** teal `#095656`, gold `#C4A032` / `#C08A2E`, navy `#12294A`, off-white `#F5F1E8`, cream `#FDF1E0`. Site font Poppins. Documents: Aptos 10 pt, 1.15 spacing, no em-dashes, avoid the word "actually".
- **Layout choices:** header with menu and "Book a call" is frozen, so no repeated closing "Book" strips. FAQ uses Wix Collapsible Text Boxes. "WTF?" card: rename (suggested "Willing To Flip?").
- **Honest framing:** Honour™ is new, so no invented testimonials or track record. Use founding-cohort pricing, a sample report and transparency instead.

## Known open items
1. Test all booking flows (Discovery Call, Honour™ request, Facilitator Package) and both forms (homepage and Technical Writing) end to end. Not tested.
2. Fix About Us credential links that point to LinkedIn edit pages.
3. Update the Brief: 5 business days, "recommendations" wording, minimum of 5 participants, sponsor rule, Reflect email timing.
4. Confirm a Facilitator Package price or "on the call".
5. Confirm Flow™ and SoftPower™ one-line promises (placeholders on the homepage mock-up) and a waitlist form.
6. Add the founding-cohort date to the site.
7. Send an uncropped emblem if the crescent top (cut by the source image) matters.

## Next pages to mock up
Our Philosophy, HFS Arc, About Us, Technical Writing, Connections, Book Online. Do one page at a time; the owner applies each in Wix before moving on.

## Environment notes
- The sandbox cannot reach `static.wixstatic.com` or run a normal browser against hannieverse.com without extra network access. The owner can send image files directly.
- To render mock-ups to PNG, use Playwright with `/opt/pw-browsers/chromium` (see the `shot.js`-style scripts used earlier) and `file://` URLs.
