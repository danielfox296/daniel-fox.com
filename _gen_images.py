#!/usr/bin/env python3
"""One-off helper: drop clean full-color photo-band section files into pages.

Each insert becomes its own `<section>` section file whose sort-key slots it
between existing sections (e.g. 015-* renders after 01-* and before 02-*).
Non-destructive: never edits existing copy. Re-runnable: clears prior *-photo-*
files first. Delete this script after the image pass is done.
"""
import pathlib

ROOT = pathlib.Path(__file__).parent
PAGES = ROOT / "_src" / "pages"
PHOTOS = "img/photos"

# image name -> alt text (descriptive, for a11y + SEO)
ALT = {
    "denver-skyline-mountains": "The Denver skyline with the Rocky Mountains rising behind it",
    "denver-aerial": "Aerial view of downtown Denver, Colorado",
    "denver-union-station": "Denver's historic Union Station",
    "denver-downtown-dusk": "A downtown Denver street at dusk",
    "boulder-foothills": "The Flatirons rising above the open foothills west of Boulder, Colorado",
    "colorado-mountains": "A Colorado mountain range under a clear blue sky",
    "strategy-whiteboard": "A marketing strategy mapped out in diagrams on a glass whiteboard",
    "strategy-planning-team": "Two people planning a strategy together at a whiteboard",
    "sticky-notes-planning": "A planning board crowded with sticky notes",
    "analytics-laptop": "Performance-marketing analytics graphs on a laptop screen",
    "dashboard-data": "A dashboard screen full of marketing data",
    "analytics-tablet": "Reviewing performance data on a tablet",
    "team-meeting": "A leader running a working session with a team and laptops",
    "boardroom-listening": "A team listening in a board meeting",
    "team-collaboration": "A team collaborating in a bright room",
    "growth-chart-laptop": "An upward growth chart on a laptop screen",
    "growth-analysis": "Analyzing growth charts and graphs on a laptop",
    "craftsman-woodwork": "A craftsman building a chair by hand in a workshop",
    "artisan-hands": "An artisan working a piece of wood by hand",
    "workshop-tools": "Hands using a power tool in a maker's workshop",
    "custom-home-luxury": "A modern luxury home with stone accents at sunset",
    "home-construction-framing": "A custom home under construction with wooden framing",
    "luxury-home": "A large custom home on a grassy hillside",
    "search-magnifying-laptop": "A magnifying glass beside a laptop, suggesting search",
    "laptop-search": "A person working on a laptop at a clean white desk",
    "ai-circuit-brain": "A circuit board shaped like a brain, suggesting AI search",
    "ai-abstract": "An abstract sphere of dots and lines suggesting an AI model",
    "compass-direction": "A compass in shallow focus, suggesting direction",
    "compass-hand": "A hand holding a compass, pointing the way",
    "calculator-finance": "Working through numbers on a calculator at a desk",
    "calculator-money": "A calculator, pen, and money on a table",
    "audience-crowd": "A large group of people standing together",
    "market-gathering": "An aerial view of a large crowd gathering",
    "boutique-retail": "A customer browsing inside a considered, premium retail space",
    "retail-store": "A shopper at a clothing rack in a boutique",
    "paint-swatches": "Paint and color swatches, suggesting a rebrand",
    "color-swatches-fan": "A fan of color swatches on a white surface",
    "handshake-deal": "Two people shaking hands on an agreement",
    "partners-handshake": "Business partners shaking hands in agreement",
    "mountain-trail": "A trail winding through a valley between mountains",
    "trail-uphill": "A path climbing a grassy hill toward distant mountains",
    "archery-target": "Arrows grouped tightly in a shooting target",
    "arrow-aim": "An arrow in sharp focus, suggesting aim",
    "interview-two-people": "Two people in conversation across a table",
}


def band(img, cap=None, cls="fig-wide"):
    return {"kind": "band", "img": img, "cap": cap, "cls": cls}


def hero(img, cap=None):
    return {"kind": "band", "img": img, "cap": cap, "cls": "fig-hero"}


def row(imgs, caps):
    return {"kind": "row", "imgs": imgs, "caps": caps}


# slug -> { sortkey: insert }
PLAN = {
    "about": {
        "025": band("craftsman-woodwork", "Before the fractional work: I founded, built, and sold Skreened, a ~$16M custom-apparel company."),
        "035": band("denver-skyline-mountains", "Based in the Denver and Boulder area, working with companies nationwide."),
    },
    "beliefs": {
        "015": band("compass-direction", "A few positions I'll defend."),
        "025": band("strategy-whiteboard"),
    },
    "demand-generation-for-high-ticket-businesses": {
        "015": band("growth-analysis", "Demand you can see, size, and repeat — not referral roulette."),
        "045": band("analytics-laptop"),
        "075": band("team-meeting"),
    },
    "do-i-need-a-cmo-for-my-small-business": {
        "015": band("team-meeting"),
        "045": band("strategy-whiteboard"),
    },
    "do-i-need-a-fractional-cmo-or-an-agency": {
        "015": band("partners-handshake"),
        "035": band("analytics-laptop"),
    },
    "fractional-cmo-denver-boulder": {
        "015": hero("denver-skyline-mountains", "Downtown Denver, the Front Range rising behind it."),
        "025": row(["boulder-foothills", "denver-union-station"],
                   ["The Flatirons above Boulder.", "Denver's Union Station."]),
        "035": band("colorado-mountains"),
    },
    "fractional-cmo-paid-advertising-strategy": {
        "015": band("analytics-laptop", "Paid is only as good as the measurement behind it."),
        "045": band("dashboard-data"),
    },
    "fractional-cmo-struggling-marketing-strategy": {
        "015": band("sticky-notes-planning", "A lot of activity is not the same as a strategy."),
        "045": band("compass-direction"),
    },
    "fractional-cmo-vs-full-time-marketing-director": {
        "015": band("team-meeting"),
        "035": band("calculator-finance"),
    },
    "fractional-cmo-vs-marketing-agency": {
        "015": band("partners-handshake"),
        "045": band("strategy-whiteboard"),
        "065": band("analytics-laptop"),
    },
    "getting-found-by-ai-search": {
        "015": band("ai-circuit-brain", "Buyers now ask an AI before they ask around."),
        "035": band("search-magnifying-laptop"),
    },
    "how-do-i-know-if-my-market-is-saturated": {
        "015": band("market-gathering", "A crowded market and a saturated one are not the same thing."),
        "035": band("audience-crowd"),
    },
    "how-much-does-a-fractional-cmo-cost": {
        "015": band("calculator-finance", "The fee is the easy part. The return is the real question."),
        "035": band("calculator-money"),
    },
    "insights": {
        "015": band("strategy-whiteboard"),
    },
    "is-a-fractional-cmo-worth-it": {
        "015": band("growth-chart-laptop", "“Worth it” is only knowable once the contribution is fenced."),
        "055": band("calculator-finance"),
    },
    "lead-generation-beyond-referrals": {
        "015": band("handshake-deal", "Referrals are a great start and a fragile foundation."),
        "035": band("audience-crowd"),
        "055": band("analytics-laptop"),
    },
    "marketing-coordinator-vs-strategist": {
        "015": band("strategy-whiteboard"),
        "035": band("archery-target"),
    },
    "product-market-fit-has-a-ceiling": {
        "015": band("trail-uphill", "Fit isn't a finish line. It's a cohort with an edge."),
        "045": band("mountain-trail"),
    },
    "projective-empathy": {
        "015": band("boutique-retail", "Seeing the purchase through the buyer's eyes, not your own."),
        "025": band("interview-two-people"),
    },
    "seo-for-high-ticket-businesses": {
        "015": band("search-magnifying-laptop"),
        "025": band("laptop-search"),
    },
    "should-i-rebrand-or-reposition": {
        "015": band("paint-swatches", "Most “rebrands” are repositioning in disguise."),
        "035": band("color-swatches-fan"),
    },
    "the-small-tweak-that-opens-the-next-market": {
        "015": band("trail-uphill", "The next market is usually one cohort over."),
        "045": band("compass-hand"),
    },
    "what-to-ask-a-fractional-cmo-interview": {
        "015": band("interview-two-people", "The questions that separate an operator from a vendor."),
        "045": band("strategy-whiteboard"),
    },
    "what-we-run": {
        "015": band("strategy-whiteboard"),
        "035": band("analytics-laptop"),
        "045": band("team-meeting"),
    },
    "who-its-for": {
        "015": hero("custom-home-luxury", "Considered, high-ticket purchases — chosen after the research."),
        "025": row(["boutique-retail", "craftsman-woodwork"],
                   ["Premium consumer retail.", "Makers of considered goods."]),
    },
    "why-arent-my-ads-converting-with-a-new-audience": {
        "015": band("archery-target", "A new audience is a new target, not the same aim."),
        "035": band("audience-crowd"),
    },
    "why-is-my-roas-declining": {
        "015": band("analytics-laptop", "A declining ROAS is a symptom. The cause is upstream."),
        "035": band("dashboard-data"),
    },
    "your-answers-are-working-as-designed": {
        "015": band("strategy-whiteboard"),
        "045": band("boutique-retail"),
    },
    "your-dashboard-cant-tell-you-whats-wrong": {
        "015": band("dashboard-data", "The dashboard tells you what happened, not why."),
        "045": band("analytics-tablet"),
    },
    "contact": {
        "005": band("partners-handshake"),
    },
    "thanks": {
        "015": band("colorado-mountains", "Talk soon."),
    },
}


def fig_html(img, cap, cls):
    alt = ALT[img]
    cap_html = f"\n      <figcaption>{cap}</figcaption>" if cap else ""
    return (
        f'    <figure class="fig {cls}">\n'
        f'      <img src="{PHOTOS}/{img}.jpg" alt="{alt}" loading="lazy" decoding="async">{cap_html}\n'
        f'    </figure>'
    )


def render(insert):
    if insert["kind"] == "band":
        inner = fig_html(insert["img"], insert["cap"], insert["cls"])
    else:  # row
        figs = []
        for img, cap in zip(insert["imgs"], insert["caps"]):
            alt = ALT[img]
            cap_html = f"\n        <figcaption>{cap}</figcaption>" if cap else ""
            figs.append(
                f'      <figure class="fig">\n'
                f'        <img src="{PHOTOS}/{img}.jpg" alt="{alt}" loading="lazy" decoding="async">{cap_html}\n'
                f'      </figure>'
            )
        inner = '    <div class="fig-row">\n' + "\n".join(figs) + "\n    </div>"
    return (
        '<section class="section-tight">\n'
        '  <div class="container">\n'
        f"{inner}\n"
        "  </div>\n"
        "</section>\n"
    )


def main():
    # clean any prior generated files so the script is idempotent
    removed = 0
    for f in PAGES.glob("*/sections/*-photo-*.html"):
        f.unlink()
        removed += 1
    written = 0
    for slug, inserts in PLAN.items():
        sec = PAGES / slug / "sections"
        if not sec.exists():
            print(f"  !! missing sections dir for {slug}")
            continue
        for key, insert in inserts.items():
            out = sec / f"{key}-photo-{slug[:10]}.html"
            out.write_text(render(insert), encoding="utf-8")
            written += 1
    print(f"Removed {removed} old, wrote {written} photo section files.")


if __name__ == "__main__":
    main()
