# Website maintenance

The live website has not yet been deployed. GitHub remains the source of truth. Production update automation is not enabled.

1. Edit the relevant content/*.json collection or public configuration in content.json on a separate branch.
2. Run the build and checks in DEPLOYMENT.md. Preview all changed pages and test the affected interactions.
3. Review changes before merging. A merge currently does not imply a GoDaddy release.
4. Use the verified deployment method once configured; record the source commit and a private backup before replacement.

Keep credentials out of Git, public content and dist/. Store future automated deployment credentials in GitHub Secrets with minimum permissions. Rotate access after revocation or suspected exposure. Keep backups outside publicly served files.

After launch, periodically check HTTPS expiry and renewal, root/www redirects, key routes, form inbox delivery, GoDaddy account notices and backup restoration. Treat mail-provider acceptance and inbox receipt as separate checks. Re-test consent when analytics tags change. Verify policy and business content before removing preview protection.

Outstanding priorities: finish hosting verification; resolve draft content and launch decisions; configure mail delivery; back up and approve publication; verify DNS/SSL and public functionality; implement an approved update process.

Temporary preview is now published at https://a9x.f47.mytemp.website/ using the documented File Manager release process. This is a manually deployed preview; GitHub changes still do not deploy automatically. Starter backup and restoration limitations are recorded in DEPLOYMENT.md. Before connecting montshiremedia.ca, resolve the HTTP redirect, host-injected monitoring, content/origin settings and live form delivery decisions.

The custom-domain preview is now configured at https://montshiremedia.ca/. Allow existing DNS caches to expire before treating local browser errors as hosting failure. The custom-domain release adds .htaccess; rollback must restore that file as well as HTML, robots and sitemap. Previous static preview release remains privately stored in account home. Root/www SSL is configured for AutoSSL renewal; monitor renewal and test it before expiry. Forms and indexing remain disabled until their launch gates are complete.
