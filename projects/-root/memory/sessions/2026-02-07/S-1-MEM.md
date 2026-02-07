# Session 1 - 2026-02-07 14:00

## Context
- **Working Directory:** /root
- **Primary Goal:** Deploy esme artist portfolio to itsupinthe.cloud domain with Cloudflare proxy
- **Duration:** ~45 minutes

## Goals Accomplished
- Repository deployed to /var/www/itsupinthe.cloud with proper ownership and permissions
- Nginx virtual host configured with security blocks and optimized caching policies
- Gzip compression enabled in nginx for text-based assets
- Direct IP access verified - site serves correctly via HTTP
- SSL/TLS handshake failure diagnosed and resolved via Cloudflare SSL mode change
- Production deployment verified at https://itsupinthe.cloud

## Bugs Fixed

### ERR_SSL_VERSION_OR_CIPHER_MISMATCH when accessing https://itsupinthe.cloud
**Root Cause:** Cloudflare SSL/TLS mode requires server-side HTTPS (Full or Full Strict mode) but nginx serves HTTP only

**Solution:** Change Cloudflare SSL/TLS encryption mode to Flexible (User→Cloudflare: HTTPS, Cloudflare→Server: HTTP)

**Prevention:** When deploying sites behind Cloudflare proxy without server-side SSL certificates, always use Flexible mode. Test HTTP before HTTPS to isolate SSL configuration issues.

## Patterns Discovered
- Cloudflare Flexible SSL pattern: VPS serves HTTP port 80, Cloudflare terminates HTTPS. User→Cloudflare encrypted, Cloudflare→Origin unencrypted. Appropriate for sites without server-side certificates.
- Image-heavy static site optimization: 520 MB asset portfolios benefit from 1-year cache headers with immutable flag to eliminate revalidation requests and reduce bandwidth
- Nginx security baseline: Production virtual hosts block .git directories, package.json, node_modules, and markdown documentation to prevent information disclosure
- DNS troubleshooting sequence: Check nameservers (dig NS) → verify A records → test HTTP → test HTTPS. Isolates SSL issues from routing issues.

## Problem Solutions

### How to serve static portfolio site with 520 MB of images efficiently
Nginx virtual host with differentiated cache policies: 1-year immutable for images, 7-day for CSS/JS, no-cache for HTML. Gzip enabled for text assets. Cloudflare CDN handles global distribution.

### Where to deploy git repository for persistent web serving
Clone to /var/www/domain-name (not /tmp). Enables git pull updates, follows web server conventions, persists across reboots. Set www-data ownership for nginx access.

## Future Avoidance
- Before deploying to Cloudflare proxy, verify SSL/TLS mode matches server capabilities (Flexible for HTTP-only origins, Full for self-signed certs, Full Strict for valid certificates)
- Test HTTP endpoint before configuring DNS/SSL to verify nginx configuration independently of TLS layer
- When setting gzip_types in nginx, omit text/html (included by default) to avoid duplicate MIME type warnings

## Notable Decisions

### Deploy repository to /var/www/itsupinthe.cloud instead of copying from /tmp/esme
**Rationale:** Git clone enables version control (git pull for updates), follows standard web directory conventions, matches existing bryanzane.com pattern, ensures persistence across reboots

**Trade-offs:** .git directory exposed (mitigated via nginx location block), slightly larger disk footprint vs plain copy

**Alternatives Rejected:** Copy from /tmp/esme (loses git history, manual updates), symlink to /tmp (not persistent)

### Separate cache policies by file type in nginx configuration
**Rationale:** Images in portfolio sites rarely change and are bandwidth-heavy (4 MB per file), HTML files contain embedded CSS/JS that may change frequently, CSS/JS files have moderate change frequency

**Trade-offs:** More complex nginx config vs single blanket cache policy, but significantly reduces bandwidth and improves performance for image-heavy sites

**Alternatives Rejected:** Single cache policy (either caches HTML too long or doesn't cache images enough), no caching (wastes bandwidth on 520 MB assets)

## Invisible Knowledge
- nginx 403 Forbidden on directory paths (e.g., /assets/images/) is expected behavior when autoindex is disabled - individual files still serve correctly with 200 OK
- esme repository requires no build step for production - static HTML/CSS/JS with embedded styles. Vite and node_modules are development-only dependencies.
- Cache-Control headers from nginx combine max-age and explicit flags - response shows both 'max-age=31536000' and 'public, immutable'
- Duplicate text/html in gzip_types produces warning but is harmless - nginx includes text/html by default in gzip compression

## References

### Files Modified
- /var/www/itsupinthe.cloud/
- /etc/nginx/sites-available/itsupinthe.cloud.conf
- /etc/nginx/sites-enabled/itsupinthe.cloud.conf
- /etc/nginx/nginx.conf

### External Links
- https://github.com/BryanZaneee/esme
- https://itsupinthe.cloud
