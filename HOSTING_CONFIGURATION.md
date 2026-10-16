# Hosting configuration

Confirmed in the authenticated GoDaddy dashboard:

- Domain: montshiremedia.ca
- Plan: Web Hosting Deluxe with cPanel.
- New account initially required activation. North America was the selected data center; WordPress was skipped because this is a static site. Skipping WordPress immediately began provisioning.
- Server IP, document root, deployed files, runtime versions, SSH/SFTP eligibility, SSL eligibility and renewal: not yet verified.

## DNS before provisioning

| Type | Name | Data | TTL |
| --- | --- | --- | --- |
| A | @ | Parked | 600 |
| NS | @ | ns35.domaincontrol.com. | 3600 |
| NS | @ | ns36.domaincontrol.com. | 3600 |
| CNAME | www | montshiremedia.ca. | 3600 |
| CNAME | _domainconnect | _domainconnect.gd.domaincontrol.com. | 3600 |
| SOA | @ | Primary nameserver ns35.domaincontrol.com. (full SOA not displayed) | 3600 |
| TXT | _dmarc | v=DMARC1; p=quarantine; adkim=r; aspf=r; rua=mailto:dmarc_rua@onsecureserver.net; | 3600 |

Seven records were listed with no filter applied. No MX, AAAA, SPF or DKIM records were listed; this is not a claim that no mail service exists. Preserve DMARC and Domain Connect records. No DNS edits have been requested by the agent. Recheck the zone after account provisioning for any GoDaddy changes. A nameserver change is not presently justified.

## Backend requirements

Static pages need directory index serving. Optional server/leads.py needs production WSGI routing, private persistent SQLite rate-limit storage and SMTP STARTTLS. Account support remains unverified. Required server environment names are documented in server/README.md; values belong in private server configuration, never Git or browser files.

## Verified after activation and preview deployment

- Shared server IP: 107.180.113.184.
- Temporary primary domain: a9x.f47.mytemp.website.
- Verified document root: /home/nkmtbwey0o8o/public_html.
- cPanel displayed active SSL for the temporary domain; HTTPS requests validated successfully. Custom-domain SSL has not been provisioned or verified.
- File Manager upload/extraction verified. Archive files kept outside the public root.
- Python app creation form offers Python 3.11.16 and 3.10.21, WSGI startup/callable configuration, application URL/path, private app root, log path and environment variables. No app was created; application execution and SMTP delivery remain untested. Avoid the default Python 2.7 choice.
- FTP, SSH Access and Git Version Control tools are present, but credential-based connections and unattended deployment have not been established.
- No domain or DNS edits performed by the agent. Recheck the authoritative zone before any future change.
