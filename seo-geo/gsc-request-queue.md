# GSC request-indexing queue — daniel-fox.com

Worked by the scheduled task `gsc-request-indexing-daniel-fox` (every 2 days,
~10/day quota — quota is per-property, separate from danielchristopherfox.com).
Property: **Domain** `sc-domain:daniel-fox.com` in Search Console
(account danielchristopherfox@gmail.com). Console URL:
https://search.google.com/search-console?resource_id=sc-domain%3Adaniel-fox.com

Per URL: inspect first. If "URL is on Google" → mark `[i]` indexed (no request).
If not indexed → REQUEST INDEXING → mark `[x]` with date. On "Quota Exceeded"
stop the run and leave the rest for next time. When every line is `[x]` or `[i]`,
disable the scheduled task and note completion here.

Baseline 2026-07-22 (Page indexing report, last update 7/9/26): 4 indexed,
29 not indexed — 26 "Discovered - currently not indexed" (never crawled),
1 "Crawled - currently not indexed", 2 "Page with redirect" (www/http variants,
harmless), 0 errors. Sitemap (32 URLs) submitted and clean; robots.txt clean.
All 32 sitemap URLs are queued below — inspection sorts out the already-indexed
ones for free (marking `[i]` costs no quota).

## Pending (priority order — money pages first)

- [x] 2026-07-22 https://daniel-fox.com/how-much-does-a-fractional-cmo-cost.html
- [x] 2026-07-22 https://daniel-fox.com/is-a-fractional-cmo-worth-it.html
- [x] 2026-07-22 https://daniel-fox.com/fractional-cmo-vs-marketing-agency.html
- [i] https://daniel-fox.com/fractional-cmo-vs-full-time-marketing-director.html
- [x] 2026-07-22 https://daniel-fox.com/do-i-need-a-fractional-cmo-or-an-agency.html
- [i] https://daniel-fox.com/do-i-need-a-cmo-for-my-small-business.html
- [x] 2026-07-22 https://daniel-fox.com/what-to-ask-a-fractional-cmo-interview.html
- [x] 2026-07-22 https://daniel-fox.com/fractional-cmo-denver-boulder.html
- [x] 2026-07-22 https://daniel-fox.com/fractional-b2c-cmo.html (was "URL is unknown to Google")
- [ ] https://daniel-fox.com/what-we-run.html
- [ ] https://daniel-fox.com/who-its-for.html
- [ ] https://daniel-fox.com/about.html
- [ ] https://daniel-fox.com/contact.html
- [ ] https://daniel-fox.com/insights.html
- [ ] https://daniel-fox.com/beliefs.html
- [ ] https://daniel-fox.com/fractional-cmo-paid-advertising-strategy.html
- [ ] https://daniel-fox.com/fractional-cmo-struggling-marketing-strategy.html
- [ ] https://daniel-fox.com/seo-for-high-ticket-businesses.html
- [ ] https://daniel-fox.com/demand-generation-for-high-ticket-businesses.html
- [ ] https://daniel-fox.com/getting-found-by-ai-search.html
- [ ] https://daniel-fox.com/lead-generation-beyond-referrals.html
- [ ] https://daniel-fox.com/how-do-i-know-if-my-market-is-saturated.html
- [ ] https://daniel-fox.com/should-i-rebrand-or-reposition.html
- [ ] https://daniel-fox.com/why-is-my-roas-declining.html
- [ ] https://daniel-fox.com/why-arent-my-ads-converting-with-a-new-audience.html
- [ ] https://daniel-fox.com/marketing-coordinator-vs-strategist.html
- [ ] https://daniel-fox.com/product-market-fit-has-a-ceiling.html
- [ ] https://daniel-fox.com/the-small-tweak-that-opens-the-next-market.html
- [ ] https://daniel-fox.com/projective-empathy.html
- [ ] https://daniel-fox.com/your-answers-are-working-as-designed.html
- [ ] https://daniel-fox.com/your-dashboard-cant-tell-you-whats-wrong.html

## Verify-only (likely already indexed; inspect and mark [i])

- [ ] https://daniel-fox.com/

## Run log

- 2026-07-22: queue created from Page indexing report + sitemap.xml (32 URLs).
- 2026-07-22 (live session): 7 requested, 2 found already indexed and marked [i]
  (fractional-cmo-vs-full-time-marketing-director, do-i-need-a-cmo-for-my-small-business).
  8th request click (what-we-run.html) hit "Quota Exceeded" — cap was 7 today, not 10;
  that URL was NOT submitted, left unchecked. Note: fractional-b2c-cmo.html inspected
  as "URL is unknown to Google / no referring sitemaps" despite being in sitemap.xml —
  GSC's sitemap state may be stale; consider resubmitting sitemap.xml in the Sitemaps
  report if more URLs show this.
