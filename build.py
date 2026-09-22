#!/usr/bin/env python3
"""daniel-fox.com static site generator.

Mirrors the Bowie (entuned.co) / danielchristopherfox.com SSG idiom: edit `_src/`,
run `python3 build.py`, built HTML lands at the repo root. NEVER edit root *.html by hand.

Pure Python stdlib — no dependencies, no npm, no bundler.
"""
import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "_src"
PAGES = SRC / "pages"
PARTIALS = SRC / "partials"
LAYOUTS = SRC / "layouts"

SITE_URL = "https://daniel-fox.com"
OG_IMAGE = f"{SITE_URL}/img/og-default.png"

# Nav keys for active-state highlighting. A page's config.json sets "nav" to one of these
# to mark the matching header link as the current page. Insights cluster (index + pillar +
# spokes) all use "insights" so the section stays lit while reading any piece of it.
NAV_KEYS = ["what-we-run", "who-its-for", "about", "insights", "contact"]

# Eyebrow kickers (small uppercase tracked labels above a headline) are off under the
# 2026-08-04 Cinema design — "headlines carry the sections". They are STRIPPED here at
# build time rather than hidden with CSS: `display:none` left ~475 words of real copy
# sitting in the HTML as hidden text, which search engines discount and which reads as
# a (mild) cloaking signal at that volume. The copy itself stays untouched in _src, so
# flipping this back to True restores every one of them.
SHOW_EYEBROWS = False
EYEBROW_RE = re.compile(r'[ \t]*<p class="eyebrow">.*?</p>\n?', re.DOTALL)

# GA4 property under the "Daniel Fox" Analytics account (acct 121066079), measurement id
# carried over unchanged when the site moved from liftwright.co to daniel-fox.com.
# Empty string => no analytics tag is emitted (never ship a broken/half-wired tag).
GA_MEASUREMENT_ID = "G-FGSHJ5C5ZT"

# This is Daniel Fox's own-name site. The default schema is the Person entity behind the
# fractional-CMO offering. Article pages override `schema` in their config.json.
# Disambiguation matters: a different, prominent "Dr. Daniel Fox" (mental-health/BPD author)
# shares the name. Occupation, alma mater, prior company, and topic coverage pin THIS entity
# down for engines. sameAs carries Daniel's confirmed LinkedIn profile (provided 2026-06-12);
# add further verified profile URLs here as they're confirmed — never assert one we can't stand behind.
SCHEMA_ORG = {
    "@type": "Person",
    "name": "Daniel Fox",
    "url": SITE_URL,
    "image": f"{SITE_URL}/img/daniel-fox.jpg",
    "sameAs": ["https://www.linkedin.com/in/danielcfox/"],
    "jobTitle": "Fractional B2C CMO",
    "address": {
        "@type": "PostalAddress",
        "addressLocality": "Denver",
        "addressRegion": "CO",
        "addressCountry": "US",
    },
    "areaServed": "US",
    "description": (
        "Fractional B2C CMO and marketing leadership for established, profitable consumer businesses "
        "with considered, high-ticket purchases. I run the whole marketing function, "
        "strategy through pipeline, and answer for the number."
    ),
    "alumniOf": {"@type": "CollegeOrUniversity", "name": "The Ohio State University"},
    "knowsAbout": [
        "Fractional CMO services",
        "B2C and consumer-brand marketing",
        "Marketing leadership",
        "Demand generation",
        "Positioning",
        "Go-to-market strategy",
        "High-ticket and considered-purchase marketing",
    ],
}


def read(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")


def partial(name: str) -> str:
    return read(PARTIALS / f"{name}.html")


def canonical_for(output: str) -> str:
    # index.html canonicalises to the bare directory URL to avoid /index.html duplication.
    if output == "index.html":
        return f"{SITE_URL}/"
    return f"{SITE_URL}/{output}"


def build_schema(cfg: dict) -> str:
    schema = cfg.get("schema", SCHEMA_ORG)
    if not schema:
        return ""
    payload = {"@context": "https://schema.org", **schema}
    return (
        '<script type="application/ld+json">'
        + json.dumps(payload, ensure_ascii=False)
        + "</script>"
    )


def build_ga() -> str:
    if not GA_MEASUREMENT_ID:
        return ""
    gid = GA_MEASUREMENT_ID
    return (
        f'<script defer src="https://www.googletagmanager.com/gtag/js?id={gid}"></script>'
        '<script>window.dataLayer=window.dataLayer||[];'
        "function gtag(){dataLayer.push(arguments);}gtag('js',new Date());"
        f"gtag('config','{gid}');</script>"
    )


def emit_redirect(cfg: dict, output: str) -> None:
    target = html.escape(cfg["redirect_to"], quote=True)
    stub = (
        "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        '<meta name="robots" content="noindex">'
        f'<meta http-equiv="refresh" content="0;url={target}">'
        f'<link rel="canonical" href="{target}">'
        f'<title>Redirecting…</title></head><body>'
        f'<a href="{target}">Continue</a></body></html>'
    )
    (ROOT / output).write_text(stub, encoding="utf-8")


def build_page(page_dir: pathlib.Path) -> dict | None:
    cfg = json.loads(read(page_dir / "config.json"))
    output = cfg["output"]

    if cfg.get("redirect_to"):
        emit_redirect(cfg, output)
        return None  # keep redirects out of the sitemap

    nav_prefix = "../" * output.count("/")

    section_dir = page_dir / "sections"
    sections = sorted(section_dir.glob("*.html")) if section_dir.exists() else []
    content = "\n".join(read(s) for s in sections)
    if not SHOW_EYEBROWS:
        content = EYEBROW_RE.sub("", content)

    page_css = ""
    css_file = page_dir / "style.css"
    if css_file.exists():
        page_css = f"<style>\n{read(css_file)}\n</style>"

    base = read(LAYOUTS / "base.html")
    header = partial("header").replace("{{nav_prefix}}", nav_prefix)
    footer = partial("footer").replace("{{nav_prefix}}", nav_prefix)

    # Active-nav state: a page's config can set "nav" to one of NAV_KEYS; the matching
    # header link gets aria-current="page" (styled in styles.css), the rest are cleared.
    active = cfg.get("nav", "")
    for key in NAV_KEYS:
        marker = 'aria-current="page"' if key == active else ""
        header = header.replace("{{nav_" + key + "}}", marker)

    # Optional per-page <body> class (e.g. "article", "blog-index") for layout variants.
    bc = cfg.get("body_class", "")
    body_attr = f' class="{html.escape(bc, quote=True)}"' if bc else ""

    replacements = {
        "{{body_attr}}": body_attr,
        "{{title}}": html.escape(cfg["title"]),
        "{{meta_description}}": html.escape(cfg.get("meta_description", ""), quote=True),
        "{{canonical}}": canonical_for(output),
        "{{og_type}}": cfg.get("og_type", "website"),
        "{{og_image}}": OG_IMAGE,
        "{{robots}}": cfg.get("robots", "index, follow"),
        "{{schema}}": build_schema(cfg),
        "{{ga}}": build_ga(),
        "{{page_css}}": page_css,
        "{{nav_prefix}}": nav_prefix,
        "{{header}}": header,
        "{{content}}": content,
        "{{footer}}": footer,
    }
    out_html = base
    for token, value in replacements.items():
        out_html = out_html.replace(token, value)

    out_path = ROOT / output
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(out_html, encoding="utf-8")
    return {"output": output, "cfg": cfg}


def write_sitemap(pages: list[dict]) -> None:
    urls = []
    for page in pages:
        if page["cfg"].get("robots", "").startswith("noindex"):
            continue
        loc = canonical_for(page["output"])
        # Optional lastmod from the page's own dates (same idiom as the
        # danielchristopherfox.com builder). Stable hand-set dates — never
        # build-time stamps — so the changed-only IndexNow diff stays honest.
        lastmod = page["cfg"].get("date_modified") or page["cfg"].get("date_published")
        tail = f"<lastmod>{lastmod}</lastmod>" if lastmod else ""
        urls.append(f"  <url><loc>{html.escape(loc)}</loc>{tail}</url>")
    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )
    (ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")


def write_llms(pages: list[dict]) -> None:
    """llms.txt from _src/llms.json (curated grouping + per-page title/desc)
    joined against the pages that actually built. An entry's title/desc may be
    null to derive from the page's config (title / meta_description). Warns on
    drift both ways — a listed page that didn't build, or an indexable page
    missing from llms.json — so the file can never silently rot again."""
    spec = json.loads(read(SRC / "llms.json"))
    by_output = {p["output"]: p["cfg"] for p in pages}
    lines = ["# Daniel Fox", "", f"> {spec['intro']}"]
    listed = set()
    for section in spec["sections"]:
        lines += ["", f"## {section['title']}", ""]
        for entry in section["pages"]:
            output = entry["page"]
            cfg = by_output.get(output)
            if cfg is None:
                print(f"  ! llms.json lists {output} but no such page built")
                continue
            listed.add(output)
            # Derived titles drop the shared " | Daniel Fox" suffix so they
            # read like the curated ones; explicit entry titles win as-is.
            title = entry.get("title") or cfg["title"].removesuffix(" | Daniel Fox").strip()
            desc = entry.get("desc") or cfg.get("meta_description", "")
            lines.append(f"- [{title}]({canonical_for(output)}): {desc}")
    for page in pages:
        if page["output"] in listed:
            continue
        if page["cfg"].get("robots", "").startswith("noindex"):
            continue
        print(f"  ! {page['output']} is indexable but missing from _src/llms.json — add it")
    (ROOT / "llms.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    built = []
    for page_dir in sorted(PAGES.iterdir()):
        if not page_dir.is_dir():
            continue
        if not (page_dir / "config.json").exists():
            continue
        result = build_page(page_dir)
        if result:
            built.append(result)
            print(f"  built {result['output']}")
        else:
            print(f"  redirect {page_dir.name}")
    write_sitemap(built)
    write_llms(built)
    print(f"Done. {len(built)} pages + sitemap.xml + llms.txt")


if __name__ == "__main__":
    main()
