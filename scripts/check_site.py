#!/usr/bin/env python3
"""Checks run on the built site (dist/) before every deployment.

1. Privacy: no phone numbers, no e-mail address other than the public one,
   nothing that looks like a token or secret.
2. Internal links: every local href/src resolves to a file in dist/.
3. External links (--external): every http(s) URL answers with a status
   below 400. DOI links are checked at doi.org (a redirect means the DOI is
   registered), so publisher bot-blocking does not cause false failures.

Exit status is non-zero when any check fails.
"""
import hashlib
import re
import sys
import time
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
PUBLIC_EMAIL = "mohammed.abdalsalam@pg.edu.pl"
SITE_PREFIX = "https://mohammed-abdalsalam-pg.github.io"

PRIVACY_PATTERNS = {
    "phone number": re.compile(r"(?:\+|\b00)\s?\d{2}[\s\-]?\d{3}[\s\-]?\d{3}[\s\-]?\d{3}\b"),
    "github token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}"),
    "generic secret": re.compile(r"(?i)(api[_-]?key|secret|password)\s*[:=]\s*['\"][^'\"]{8,}"),
}
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
ALLOWED_EMAILS = {PUBLIC_EMAIL}
# SHA-256 of the author's private phone digits: detects the number in any formatting
# without storing it in this public repository.
PRIVATE_PHONE_SHA256 = "9c5390f0f5ece954afba98d3e7f08c7a43f2651c1afac424ef0d73df18fdb8e0"
DIGIT_RUN = re.compile(r"\d[\d\s\-().]{7,16}\d")


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        for k, v in attrs:
            if k in ("href", "src") and v:
                self.urls.append(v)
            if k == "srcset" and v:
                self.urls += [part.strip().split()[0] for part in v.split(",")]


def check_privacy(files):
    errors = []
    for f in files:
        text = f.read_text(errors="ignore")
        for name, rx in PRIVACY_PATTERNS.items():
            for m in rx.finditer(text):
                errors.append(f"{f.relative_to(DIST)}: possible {name}: {m.group(0)[:30]!r}")
        for m in DIGIT_RUN.finditer(text):
            digits = re.sub(r"\D", "", m.group(0))
            for i in range(0, max(1, len(digits) - 8)):
                if hashlib.sha256(digits[i:i + 9].encode()).hexdigest() == PRIVATE_PHONE_SHA256:
                    errors.append(f"{f.relative_to(DIST)}: private phone number found")
        for m in EMAIL_RE.finditer(text):
            addr = m.group(0).rstrip(".")
            if addr not in ALLOWED_EMAILS and not addr.endswith("noreply.github.com"):
                errors.append(f"{f.relative_to(DIST)}: e-mail address not allowed: {addr}")
    return errors


def fetch_status(url):
    headers = {"User-Agent": "Mozilla/5.0 (compatible; academic-site-link-check)"}
    target = url
    if url.startswith("https://doi.org/"):
        req = urllib.request.Request(target, headers=headers, method="HEAD")
        opener = urllib.request.build_opener(NoRedirect)
        try:
            with opener.open(req, timeout=30) as r:
                return r.status
        except urllib.error.HTTPError as e:
            return e.code
    for method in ("HEAD", "GET"):
        req = urllib.request.Request(target, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.status
        except urllib.error.HTTPError as e:
            if method == "HEAD" and e.code in (403, 405, 404, 429):
                continue
            return e.code
        except Exception as e:  # noqa: BLE001
            if method == "GET":
                return f"error: {e.__class__.__name__}"
    return "unknown"


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


def main():
    external = "--external" in sys.argv
    html_files = sorted(DIST.rglob("*.html"))
    text_files = html_files + sorted(DIST.rglob("*.json")) + sorted(DIST.rglob("*.xml")) + sorted(DIST.rglob("*.txt"))
    errors = check_privacy(text_files)

    ext_urls = set()
    for f in html_files:
        p = Links()
        p.feed(f.read_text())
        for u in p.urls:
            if u.startswith(("mailto:", "#", "data:")):
                continue
            if u.startswith(SITE_PREFIX):
                u = "/" + u[len(SITE_PREFIX):].lstrip("/")
            elif u.startswith(("http://", "https://")):
                ext_urls.add(u.split("#")[0])
                continue
            if not u.startswith("/") and SITE_PREFIX in u:
                continue
            path = u.split("#")[0].split("?")[0]
            target = (DIST / path.lstrip("/")) if path.startswith("/") else (f.parent / path)
            if path.endswith("/") or target.is_dir():
                target = target / "index.html"
            if not target.exists():
                errors.append(f"{f.relative_to(DIST)}: broken internal link {u}")

    if external:
        for u in sorted(ext_urls):
            st = fetch_status(u)
            ok = isinstance(st, int) and (st < 400 or (u.startswith("https://doi.org/") and st in (301, 302, 303, 307, 308)))
            print(f"{'ok  ' if ok else 'FAIL'} {st} {u}")
            if not ok:
                errors.append(f"external link failed ({st}): {u}")
            time.sleep(0.3)

    for err in errors:
        print("ERROR", err)
    print(f"checked {len(html_files)} pages, {len(ext_urls)} external URLs; {len(errors)} problem(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
