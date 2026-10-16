# Upgrade summary

## Implemented

- Existing identity, URLs, original layouts, service copy and honest proof placeholders preserved.
- All editorial collections and page/shared copy moved to JSON; named fields for services, case studies, articles, industry links, process, team, manifesto and engagement models. New records generate routes, cards, filters and sitemap without changing build.py.
- 28 pages: added free SEO/site health review, engagement models, Security and Accessibility. Manifesto on Home/About; contextual service/industry links; article-category filter.
- Self-hosted, OFL-licensed Fraunces display subset (20,780 bytes), refined dark/light palette, richer geometric art and reduced-motion-aware reveals/hover states.
- Configurable calendar with explicit click-to-load and direct-link fallback.
- Default-denied basic consent mode; optional analytics load only after opt-in; no measurement IDs shipped. Fixed event names; no form-field data in analytics.
- Live POST/loading/error/acceptance UI plus explicit preview download fallback. Optional Python server with strict validation, honeypot, persistent atomic rate limits, exact origin checks and SMTP STARTTLS. Live mode remains off.
- Verified-only Article/LocalBusiness schema configuration, with current Organization/Service/FAQ/Breadcrumb schemas retained.
- README authoring guides, backend deployment instructions, owner checklist and revised growth plan.

## Partially implemented / owner configuration required

- Live email delivery: server code and client flow exist, but the static Sites environment cannot execute Python. Hosting/proxy or Worker port, mail credentials, recipient, storage and real delivery verification are missing. Tests mock SMTP acceptance. Preview never reports delivery.
- CASL: optional unchecked checkbox and sender/withdrawal configuration gate exist. It remains disabled; working unsubscribe/consent operations and professional review are outstanding.
- Analytics and booking: configuration and consent/load gates are implemented. Real IDs, container audit and booking URL are absent. No provider-side conversion verification has occurred.
- Performance/accessibility: implementation supports these goals; no Lighthouse score, field CWV, independent audit or conformance certification has been obtained.

## Verification

- Python tests passed for field/type/length validation, honeypot, bad URL/email, header injection, invalid consent, rate limits/expiry, wrong Origin, missing configuration, oversized/non-JSON requests and mocked SMTP failure/acceptance.
- All 28 generated pages passed internal URL/anchor/asset checks, single-H1 and unique-ID checks, JSON-LD parsing, noindex protection and unresolved-template checks.
- JavaScript syntax checks passed. Mobile and desktop homepage layouts were inspected; no horizontal overflow was found at 320px or 1440px. Cookie dismissal and the review form’s explicit no-delivery download state were verified. Full screen-reader and cross-browser audits remain pending.
- Consent unit tests passed for default denial, opt-in loading, withdrawal/reload, GTM precedence, fixed event names and empty-ID behaviour.

## Blocked publication

The existing owner-private Site is still appgprj_6ad16ff8662481919cce1d6fe4fdb24a. The native source helper was started, but automatic approval rejected the hidden-stdin credential handoff because sandbox approval is disabled. No replacement Site was created; no deployment success is claimed. The deployable local output and GitHub source can still be delivered.
