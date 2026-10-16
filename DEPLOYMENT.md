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
