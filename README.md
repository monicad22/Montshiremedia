# Montshire Media

An upgrade of the existing site: 28 pre-rendered pages, editable content collections, self-hosted Fraunces display typography, geometric art, light/dark themes and progressive JavaScript. The original Sites identity is preserved locally in `.openai/hosting.json`. It remains excluded from the public GitHub repository.

## Build, preview and verify

Python 3.9+ is sufficient; no build dependencies are needed. From the project folder:

```sh
python3 build.py
python3 tests/check_site.py
python3 -m unittest discover -s tests -v
python3 -m http.server 4173 --bind 127.0.0.1 --directory dist
```

Open http://127.0.0.1:4173/. `dist/` contains the deployable static site. CSS and JavaScript are maintained there; HTML, config.js, sitemap and robots are generated. Preserve assets when rebuilding. `server/leads.py` is an optional WSGI endpoint, separate from static hosting; see server/README.md.

## Content model

- `content.json`: public configuration—origin, preview flag, analytics IDs, lead enablement/endpoint, marketing sender details, booking URL and verified business fields. Never put credentials here.
- `content/services.json`: service descriptions, deliverables, tools, KPIs and FAQs.
- `content/case-studies.json`: title, industry/service labels, placeholder status, sections and quote.
- `content/articles.json`: categories, bylines, reading time, sections, draft/published status and verification fields.
- `content/industries.json`: unique industry narratives and service-slug links. These generate contextual links on existing pages, not thin landing pages.
- `content/process.json`, `team.json`, `engagements.json`, `manifesto.json`: their named collections.
- `content/pages.json`: page metadata and editable `body_html` content layouts, preserving the original sections. Markers such as `{{service_cards}}` insert collection components. These are trusted owner-authored HTML—not a public input field. Do not paste unreviewed scripts or markup.
- `content/shared.json`: shared editorial copy, navigation/footer HTML, CTA copy, form labels/options and status messages.

Text in collection records is escaped by the renderer. Slugs must be unique lowercase letters/numbers separated by single hyphens. The build checks required references and prevents duplicate routes. Route generation, filtering, listings, sitemap and internal links derive from the collections.

### Add a case study without changing build.py

1. Copy one object in `content/case-studies.json` and give it a unique slug, title, description, industry and service label.
2. Edit the `sections` array (`heading`, `text`) and `quote`. Keep `placeholder: true` until all claims and client permissions are verified. When approved, set false. Include baseline, time period and attribution in results.
3. Run `python3 build.py`. The detail page, listing card and filter options are generated automatically. Preview and run the checks. The current fixture check expects 28 pages; update that count after intentionally adding/removing pages.

### Add an article without changing build.py

1. Copy an object in `content/articles.json`; set a unique slug, title, description, category, author, reading_time and sections.
2. Use `status: "draft"`, `verified: false`, `date_published: null` while editing. The outline disclosure remains visible.
3. Only after author/date/content approval, set `status: "published"`, `verified: true` and `date_published` to an ISO date. Article schema is emitted only with those verified details. This does not remove the site's preview/noindex protection.
4. Rebuild. The article page, listing, categories, related links and sitemap update automatically.

## Forms and booking: exact current state

Both Contact and Free SEO & site health review have forms. `lead.enabled` is false: submissions create a browser-local text download, and the page explicitly says nothing was sent or stored. The client also supports live POST, loading, failure and acceptance states. The optional server implements strict validation, length/body limits, an atomic SQLite-backed rate limit, honeypot, origin checks and SMTP STARTTLS notifications. Unit tests mock email acceptance; **real delivery has not been tested**.

**Missing:** a supported live server deployment, production origin/proxy routing, persistent rate-limit storage/secret, a verified SMTP account/sender and owner-approved notification recipient. Python WSGI cannot run in the existing static Sites deployment. Provision a separate same-origin endpoint or port this handler to a Sites Worker with durable storage and an HTTP email provider. Setup and launch tests are in `server/README.md`. Keep live mode off until successful inbox delivery and failure paths are verified.

Marketing consent is unchecked, optional and disabled until live delivery, sender identity, postal address, contact email and unsubscribe URL are configured. No newsletter subscription occurs automatically. A working withdrawal process and professional CASL/privacy review are still required; the implementation alone is not a compliance claim.

Set `booking_url` to an approved HTTPS embed URL. The calendar loads only after a visitor explicitly clicks Load booking calendar; a direct link is also provided. Confirm provider terms, privacy and accessibility before enabling.

## Analytics and consent

`dist/consent.js` queues default-denied consent before any Google tags. Analytics scripts load only after opt-in and only if a valid ID exists. Choose `analytics.gtm_id` OR `analytics.ga4_id`; GTM takes precedence to avoid loading both. Advertising storage, ad user data and personalization remain denied. Essential-only withdraws consent and reloads without analytics scripts.

The implementation emits `cta_click`, `booking_click` (only an actual calendar action), and `form_submit` (only confirmed server acceptance). It never passes enquiry fields. Direct GA4 uses a clean page URL without query/hash and a blank referrer. If using GTM, configure GA4 tags to use similarly clean URLs and disable automatic/enhanced form capture, user-provided data and any tag that collects PII. Audit the actual container; code cannot guarantee the behaviour of arbitrary tags the owner adds. Decide cookie cleanup/retention and document it in the final policy. No IDs are configured and no live analytics has been verified.

## Design and performance

The original green/ink/off-white direction and layouts are retained. Fraunces is self-hosted with `font-display: swap`; its Latin subset is 20,780 bytes. Source: https://github.com/google/fonts/tree/main/ofl/fraunces, SIL Open Font License bundled at `dist/fonts/OFL.txt`. The font was instanced at weight 450, optical size 72, softness 35, wonk 1 and subset to Latin/punctuation. Body type uses system sans-serif. There are no external font requests. Motion respects reduced-motion and content is visible if JavaScript fails.

No Lighthouse score, field Core Web Vitals, WCAG certification, security certification or independent audit is claimed. Tests and manual verification are recorded in CHANGE-SUMMARY.md.

## Publish the existing Site

Use the Sites source workflow with the preserved ID; never create a replacement Site. Get the existing Site/access, mint a short-lived source credential, open/sync with the helper, package `dist/` with the manifest, then save/deploy to its existing owner-private audience. Credentials stay in memory and go through hidden stdin only. Do not copy credentials into GitHub.

Current limitation: the source helper's credential stdin handoff was rejected by the session approval policy, so this upgrade has not been published through Sites. GitHub source updates and the local deployable files are separate from a verified Sites deployment.

## Before public launch

Follow every item in PLACEHOLDERS.md. Keep `preview: true` and noindex until the owner confirms placeholders are resolved. Legal pages remain drafts. After approval, configure the final domain/origin, update schema with verified business details, resolve redirects, validate social cards and structured data, verify DNS/HTTPS and production headers, configure Search Console, and measure real performance/accessibility. Follow GROWTH-PLAN.md after those launch gates pass.
