#!/usr/bin/env python3
"""Liftwright static site generator.

Mirrors the Bowie (entuned.co) / danielchristopherfox.com SSG idiom: edit `_src/`,
run `python3 build.py`, built HTML lands at the repo root. NEVER edit root *.html by hand.

Pure Python stdlib — no dependencies, no npm, no bundler.
"""
import html
import json
import pathlib

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "_src"
PAGES = SRC / "pages"
PARTIALS = SRC / "partials"
LAYOUTS = SRC / "layouts"

SITE_URL = "https://liftwright.co"
OG_IMAGE = f"{SITE_URL}/img/og-default.png"

# Nav keys for active-state highlighting. A page's config.json sets "nav" to one of these
# to mark the matching header link as the current page. Insights cluster (index + pillar +
# spokes) all use "insights" so the section stays lit while reading any piece of it.
NAV_KEYS = ["what-we-run", "who-its-for", "about", "insights", "contact"]

# Liftwright GA4 property "Liftwright" (web stream "Liftwright Web", stream id 15028666922),
# created 2026-06-08 under the existing "Daniel Fox" Analytics account (acct 121066079).
# Empty string => no analytics tag is emitted (we never ship a broken/half-wired tag).
GA_MEASUREMENT_ID = "G-FGSHJ5C5ZT"

# Liftwright is firewalled from the Daniel Fox / Music Behaviorist person entity and from
# Entuned. The default org schema is neutral — no Person, no personal-brand binding.
SCHEMA_ORG = {
    "@type": "Organization",
    "name": "Liftwright",
    "url": SITE_URL,
    "description": (
        "Fractional marketing leadership for established, profitable, under-led businesses "
        "with considered, high-ticket purchases. Strategy through pipeline, run as one team."
    ),
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

    replacements = {
        "{{title}}": html.escape(cfg["title"]),
        "{{meta_description}}": html.escape(cfg.get("meta_description", ""), quote=True),
        "{{canonical}}": canonical_for(output),
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
        urls.append(f"  <url><loc>{html.escape(loc)}</loc></url>")
    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )
    (ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")


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
    print(f"Done. {len(built)} pages + sitemap.xml")


if __name__ == "__main__":
    main()
