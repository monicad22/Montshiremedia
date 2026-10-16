# Website maintenance

The live website has not yet been deployed. GitHub remains the source of truth. Production update automation is not enabled.

1. Edit the relevant content/*.json collection or public configuration in content.json on a separate branch.
2. Run the build and checks in DEPLOYMENT.md. Preview all changed pages and test the affected interactions.
3. Review changes before merging. A merge currently does not imply a GoDaddy release.
4. Use the verified deployment method once configured; record the source commit and a private backup before replacement.

Keep credentials out of Git, public content and dist/. Store future automated deployment credentials in GitHub Secrets with minimum permissions. Rotate access after revocation or suspected exposure. Keep backups outside publicly served files.

After launch, periodically check HTTPS expiry and renewal, root/www redirects, key routes, form inbox delivery, GoDaddy account notices and backup restoration. Treat mail-provider acceptance and inbox receipt as separate checks. Re-test consent when analytics tags change. Verify policy and business content before removing preview protection.

Outstanding priorities: finish hosting verification; resolve draft content and launch decisions; configure mail delivery; back up and approve publication; verify DNS/SSL and public functionality; implement an approved update process.
