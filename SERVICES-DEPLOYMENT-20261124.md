# Services expansion — November 24, 2026

Published destination: https://montshiremedia.ca/services/ on the existing GoDaddy account. The native Sites project remains unpublished; the separate source-workflow credential handoff was rejected by automatic approval review. No alternative public Sites audience or new hosting project was created.

The catalogue contains 13 services, retaining the original six detail URLs and adding seven: strategy/training, organic social, email campaigns/automation, photography/video/podcasts, PR/creator campaigns, hosting/care and promotional merchandise. Existing SEO, paid media, web, branding and analytics scopes were expanded in place. SERVICE-CATALOGUE-REVIEW.md records references and overlap decisions.

## Release and rollback

Release: `montshire-services-20261124-r2.zip`, SHA-256 `f6b8a65439743752e559ae861ba3fd245c005ad1746b650bbc9d66446f3f4eda`. The archive contains 35 HTML pages, style.css and sitemap.xml. The first archive used restrictive file permissions and briefly caused 403 responses; the corrected r2 archive stores regular files with mode 0644. Do not use the first `montshire-services-20261124.zip` archive.

Private rollback backup: `/home/nkmtbwey0o8o/montshire-before-services-20261124.zip`, created from the complete public_html before this change. Both rollback and release archives are outside public_html. Existing .htaccess, api/leads/.htaccess, .well-known, JavaScript/configuration, fonts and robots.txt were excluded from the release. Extracting the rollback restores the prior public_html content; newly added service directories must be moved aside separately when reverting. Preserve host files and unrelated later changes.

## Verification

- All 37 changed public files returned HTTPS 200 and matched the local release after stripping only the previously documented GoDaddy monitoring block from HTML.
- Existing config.js and robots.txt matched the private before-state; both private archive URL probes returned 404.
- The catalogue contains 13 unique service links. The services navigation contains the all-services link plus those 13 entries.
- All 35 generated pages pass route, anchor, asset, metadata and structured-data checks. Six backend tests and the existing consent checks pass.
- Desktop and a 390px-wide embedded mobile viewport were visually inspected. Mobile content width was 390px with no horizontal overflow. These checks are not physical-device, independent accessibility or performance audits.

## Editing

Edit `content/services.json` for service copy, deliverables, scope notes and group assignments. Edit the `/services/` entry in `content/pages.json` for the overview. `service_catalogue.py` renders the directory groups and direct-email service CTA. Keep each slug unique and assign it to exactly one group. Preserve existing URLs and expand related deliverables instead of adding duplicate pages.

Rebuild with `python3 build.py`, then run `python3 tests/check_site.py`, `python3 -m unittest discover -s tests -v`, and `node tests/test-consent.cjs`. Build output remains `dist/`. Preserve its assets when rebuilding.

## Marketing readiness

The pre-launch/noindex state, unfinished editorial/legal content and preview enquiry forms were preserved. Services pages offer direct mailto links to the previously created info@montshiremedia.ca mailbox. This update did not verify inbox deliverability, enable tracking, change DNS or purchase services. Resolve launch content and live enquiry delivery before sending paid traffic.
