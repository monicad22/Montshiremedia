# Optional lead delivery endpoint

This Python WSGI module is implemented and unit-tested, but **not deployed by the current static Sites configuration**. Sites hosts Cloudflare Workers rather than Python WSGI. A live endpoint needs either a separately provisioned Python host with same-origin reverse proxy routing, or a port to a Sites-supported Worker with durable rate-limit storage and an HTTP email service. No such service or email account is provisioned in this workspace. Do not enable live mode until delivery is tested.

Required environment configuration on that server (never browser config or Git):

- `SITE_ORIGIN`: exact HTTPS site origin; no trailing slash.
- `SMTP_HOST`, `SMTP_PORT` (default 587), `SMTP_USER`, `SMTP_PASSWORD`: a verified provider supporting STARTTLS.
- `SMTP_FROM`: verified sender address.
- `LEAD_TO`: owner-approved notification recipient.
- `RATE_LIMIT_SECRET`: a random secret of at least 32 bytes.
- `RATE_LIMIT_DB`: path to a persistent SQLite database outside publicly served files, writable only by the service.

Use a production WSGI runner and HTTPS proxy with request/body/read-time limits. Serve `dist/` at the root and route only POST `/api/leads` to `server.leads:application`. Set `REMOTE_ADDR` from a trusted proxy configuration; the application intentionally ignores forwarded headers from requests. With multiple servers, replace SQLite with a shared transactional limiter. Limits are five requests per client per 15 minutes, applied before field validation. The limit table prunes expired rows on each request; schedule expiry cleanup if retention must be enforced while idle.

Then set `lead.enabled=true` in content.json on both the server and frontend, keep `lead.endpoint=/api/leads`, rebuild, restart the WSGI process and test. The configuration is loaded at process startup. Static preview mode must stay disabled until the endpoint is actually available. The frontend displays success only after HTTP 200 and `accepted:true`. This means SMTP accepted the message; it does not prove inbox delivery. Errors preserve the entered values. A timeout can be ambiguous; check the recipient inbox before resubmitting to avoid duplicates.

The server validates strict keys/types/lengths, required fields, email and HTTP(S) website formats, known service/budget values, marketing eligibility and a honeypot. It sends plain-text mail using fixed subject lines and refuses header control characters. No URL fetching is performed. No enquiry contents are logged by the module or stored in SQLite. Configure the web server, proxy and mail provider not to log bodies, and decide email retention. Keep database files and secrets outside dist and out of Git.

Marketing is optional and unchecked. Keep it disabled until sender identity, postal address, contact email, consent wording, withdrawal URL and a tested unsubscribe process are approved. The email records consent selection, wording version and time; this does not enroll anyone in a marketing platform or itself establish CASL compliance. Obtain professional review.

Before enabling: test missing configuration, malformed inputs, honeypot, request limits, wrong origin, provider rejection, outage, successful provider acceptance and received inbox mail. Confirm privacy text and provider/cross-border retention details. Add production security headers and verify them on the real origin. No certifications or penetration tests are claimed.
