# Deployment

Preparation status — not deployed. Source audited at 0d9dccc696df8b5440f36162ce4127b1051fc348.

## Verified build

Python 3.9+ standard library; no installation step or third-party dependencies.

```sh
python3 build.py
python3 tests/check_site.py
python3 -m unittest discover -s tests -v
node tests/test-consent.cjs
```

All four checks passed during preparation. The site has 28 pre-rendered pages. Deployable output is dist/ only. CSS, JavaScript, favicon and font are maintained in dist/; do not clean that directory before building. The Python mail backend in server/ is a separate deployment.

## Launch gates

- Verify cPanel document root, existing files, runtime support and SSL eligibility.
- Back up the destination outside the public web root and record the backup path.
- Resolve owner decisions in PLACEHOLDERS.md. Current preview=true deliberately emits noindex and robots Disallow.
- Set content.json origin to the approved HTTPS production origin and rebuild. Never expose server secrets there.
- Establish a supported /api/leads service and verify real inbox delivery before enabling forms.
- Request explicit approval for the exact file publication and DNS changes.
- Deploy only the release output, retaining required host configuration. Verify routes and assets over HTTPS.

## Rollback

Before publication, record the deployed source SHA, release checksum and private backup location. Restore the previous web-root snapshot using the verified hosting method. Restore DNS only from the recorded before-state and with owner approval. No production snapshot exists yet.

## Future automation

Automatic deployment is not enabled. Select SSH/SFTP or a hosting-supported Git method only after checking account capabilities. A future workflow must build and test a fixed commit, deploy only dist/, use GitHub Secrets, serialize production deployments and require an approved production environment. Confirm approval before enabling automatic publication.

## Approved temporary deployment completed

Temporary preview: https://a9x.f47.mytemp.website/
Website source deployed: 0d9dccc696df8b5440f36162ce4127b1051fc348. Release ZIP SHA-256: 7035e0e913a9fb6c3440c7979506d96e15b1f408d00ce89bb3db6aab51f1f0fc.

Owner approved backup and temporary preview upload. The release archive was uploaded to the private account home and extracted into /home/nkmtbwey0o8o/public_html. Existing host files and .well-known were preserved. DNS and automatic publishing were not changed.

Backup: /home/nkmtbwey0o8o/montshire-starter-backup-20261016.zip. Verified archive results include .well-known/acme-challenge, cgi-bin, home.html, 404.shtml and layout-styles.css. Both backup and release ZIP URLs return 404 on the public site. To restore the starter, first privately preserve the current website, move newly added release files out of public_html, and extract the starter archive into public_html. The starter archive does not contain the new Montshire pages, so extracting alone will not remove them. Do not delete .well-known or unrelated hosting files.

Testing: HTTPS returned 200 for all 28 pages and 9 assets. All assets match the release byte-for-byte. All HTML matches after removing one GoDaddy-injected monitoring block. Missing-route probe returned 404. Browser checks passed for services menu, mobile menu and draft enquiry confirmation. Homepage layouts inspected at 1440, 768, 390 and 412 pixel widths; no horizontal overflow observed. These are browser viewport checks, not physical-device tests. Homepage/contact console inspection found no errors at the time checked.

Launch failures/pending: HTTP returns 200 without HTTPS redirect; custom domain is unconnected; canonical/sitemap origin still uses the prior Sites URL; noindex remains intentional; no live email delivery, booking or analytics integration is enabled. GoDaddy injects img1.wsimg.com/traffic-assets/js/tccl.min.js independently of the site's consent code; its data handling/opt-out needs resolution. Security headers and complete accessibility/performance audits are not verified. The temporary preview is not final launch approval.
