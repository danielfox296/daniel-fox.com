#!/usr/bin/env python3
"""One-off helper: turn each page's hero + CTA into a full-bleed photographic band.

Heroes are uniformly `<section class="hero">`, CTAs `<section class="section section-ink">`,
so a single exact-string swap per file is safe. Each becomes a .photo-section with a
.photo-bg layer (for the JS parallax) carrying a concept-matched cinematic image.
Idempotent: skips a file already converted. Also deletes the pass-1 inset photo files.
Delete this script once the band pass is settled.
"""
import pathlib

ROOT = pathlib.Path(__file__).parent
PAGES = ROOT / "_src" / "pages"


def bg(img):
    return f"  <div class=\"photo-bg\" style=\"background-image:url('img/photos/{img}.jpg')\"></div>"


# slug -> hero image (concept-matched). Excludes home (done by hand), about (keeps the
# portrait hero), and the utility pages (contact/thanks/video/redirects).
HERO = {
    "beliefs": "band-mountains-sunset",
    "demand-generation-for-high-ticket-businesses": "band-city-night",
    "do-i-need-a-cmo-for-my-small-business": "band-office-night",
    "do-i-need-a-fractional-cmo-or-an-agency": "boardroom-listening",
    "fractional-cmo-denver-boulder": "band-denver-night",
    "fractional-cmo-paid-advertising-strategy": "band-trading-dark",
    "fractional-cmo-struggling-marketing-strategy": "band-office-night",
    "fractional-cmo-vs-full-time-marketing-director": "boardroom-listening",
    "fractional-cmo-vs-marketing-agency": "boardroom-listening",
    "getting-found-by-ai-search": "band-ai-network",
    "how-do-i-know-if-my-market-is-saturated": "band-city-night",
    "how-much-does-a-fractional-cmo-cost": "band-trading-dark",
    "insights": "band-office-night",
    "is-a-fractional-cmo-worth-it": "band-trading-dark",
    "lead-generation-beyond-referrals": "band-city-night",
    "marketing-coordinator-vs-strategist": "boardroom-listening",
    "product-market-fit-has-a-ceiling": "band-mountains-sunset",
    "projective-empathy": "band-boutique",
    "seo-for-high-ticket-businesses": "band-ai-network",
    "should-i-rebrand-or-reposition": "band-office-night",
    "the-small-tweak-that-opens-the-next-market": "band-mountains-sunset",
    "what-to-ask-a-fractional-cmo-interview": "boardroom-listening",
    "what-we-run": "band-office-night",
    "who-its-for": "band-workshop",
    "why-arent-my-ads-converting-with-a-new-audience": "band-trading-dark",
    "why-is-my-roas-declining": "band-trading-dark",
    "your-answers-are-working-as-designed": "band-office-night",
    "your-dashboard-cant-tell-you-whats-wrong": "band-trading-dark",
}

# A consistent Denver-sunset close on every CTA (a deliberate brand signature). The local
# page closes on Boulder instead so it carries both cities.
CTA_DEFAULT = "band-denver-night"
CTA_OVERRIDE = {"fractional-cmo-denver-boulder": "band-boulder-sunset"}
# Pages whose CTA is the standard section-ink band (excludes seo's section-panel CTA + video).
CTA_PAGES = list(HERO.keys()) + ["about"]

HERO_OLD = '<section class="hero">'
CTA_OLD = '<section class="section section-ink">'


def first_section(slug):
    sec = PAGES / slug / "sections"
    files = sorted(sec.glob("*.html"))
    return files[0] if files else None


def cta_file(slug):
    sec = PAGES / slug / "sections"
    hits = sorted(sec.glob("*cta*.html"))
    return hits[0] if hits else None


def convert(path, old, new_open, img, label):
    txt = path.read_text(encoding="utf-8")
    if "photo-section" in txt.splitlines()[0]:
        print(f"  = already a band: {label}")
        return 0
    if old not in txt:
        print(f"  !! pattern not found in {label} ({path.name})")
        return 0
    txt = txt.replace(old, new_open + "\n" + bg(img), 1)
    path.write_text(txt, encoding="utf-8")
    print(f"  + {label} -> {img}")
    return 1


def main():
    removed = 0
    for f in PAGES.glob("*/sections/*-photo-*.html"):
        f.unlink()
        removed += 1
    old_gen = ROOT / "_gen_images.py"
    if old_gen.exists():
        old_gen.unlink()
    print(f"Removed {removed} pass-1 inset files + old generator.")

    n = 0
    for slug, img in HERO.items():
        hero = first_section(slug)
        if hero:
            n += convert(hero, HERO_OLD,
                         '<section class="hero photo-section photo-hero" data-parallax>',
                         img, f"{slug}/hero")
    for slug in CTA_PAGES:
        cf = cta_file(slug)
        if cf:
            img = CTA_OVERRIDE.get(slug, CTA_DEFAULT)
            n += convert(cf, CTA_OLD,
                         '<section class="section photo-section photo-center" data-parallax>',
                         img, f"{slug}/cta")
    print(f"Converted {n} sections.")


if __name__ == "__main__":
    main()
