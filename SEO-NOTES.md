# Revenger: content and local SEO handover

Updated 23 October 2026. Research is a qualitative review of public websites, not a search-volume, backlink or ranking audit. No ranking outcome is promised.

## Competitor observations

| Reference | Observed approach | Revenger implementation |
| --- | --- | --- |
| [Bisleri](https://www.bisleri.com/bisleri-water-bottles/bisleri.html) | Product formats, quality information and a broad beverage portfolio | Clear water/soda/jeera/lemon categories and enquiry routes. No competitor quality-test numbers or certifications copied. |
| [Bisleri contact](https://www.bisleri.com/contact-us) | Named locations and direct business contacts | Separate head and registered office details, telephone, email and address-search links. |
| [AquaZal](https://aquazal.com/) | Packaged water and jars with Prayagraj references | Explicit Prayagraj coverage and a retailer enquiry path. No unsupported jar formats added. |
| [SaryuNeer](https://saryuneer.com/) | UP city coverage alongside brand and product content | One useful service-area page listing only the client's ten confirmed cities/districts. |
| [A3 Distributors](https://www.a3distributor.com/) | Mumbai business supply positioning and beverage categories | Retailer/distributor language paired with city and product enquiry prefills. |

These are content observations and design/SEO recommendations, not claims that a competitor ranks first or that Revenger is superior. Revenger copy is original and based on the supplied business brief.

## Search-intent map

| Page | Target topics and phrases used naturally |
| --- | --- |
| Home | Revenger water brand, packaged drinking water and beverages, Maharashtra, Uttar Pradesh |
| Company | GangaShree Roots Private Limited, Revenger company, Subir Banerjee, Rakesh Salve |
| Products | Revenger packaged drinking water, soda, jeera soda, lemon soda |
| Values | Revenger quality commitment, trust, responsible manufacturing and growth |
| Service areas | packaged drinking water brand in Prayagraj; water and beverage retail enquiries in Mumbai, Thane, Palghar; coverage in Jaunpur, Varanasi, Pratapgarh, Sultanpur, Ayodhya, Chitrakoot |
| Contact | Revenger contact number; Vasai West head office; Prayagraj registered office |

No search-volume or competition metrics were available, so these are intent-based keyword targets. Do not describe every service area as a factory or office. The client has not identified the factory address.

## Implemented

- Six server-rendered pages with unique titles and descriptions in `content.py`.
- One H1 per page, descriptive headings, internal links and readable URLs.
- Absolute self-canonical URLs; Open Graph and Twitter preview metadata.
- Organization, Brand, Person references, WebSite, WebPage and BreadcrumbList JSON-LD with client-supplied facts.
- Both offices and the ten service areas represented without fake branches, ratings, opening hours or credentials.
- `sitemap.xml`, `robots.txt`, genuine 404 responses; public content available without JavaScript.
- Responsive local fonts, deferred small interaction script, no heavy Three.js or GSAP loading on the portfolio.
- Direct call/email actions; email draft composer makes no database submission claim.

Google ignores meta-keywords; target terms belong in useful visible copy, titles and descriptions: https://developers.google.com/search/docs/crawling-indexing/special-tags

## What remains outside the code

1. Finalize a brand-owned domain. Set `SITE_URL=https://your-domain` in Vercel and redeploy; it controls all canonical, share, schema and sitemap URLs. Redirect the old domain to the final one.
2. Verify ownership in Google Search Console, submit `/sitemap.xml`, inspect the six URLs and request indexing where appropriate. Indexing is not automatic or guaranteed.
3. Create/complete eligible Google Business Profiles with consistent company name, real address, phone, categories and genuine business hours. Confirm whether customers can visit each office before publishing visiting hours or a storefront claim.
4. Add original leadership, plant and actual product/label photography when provided. Current bottle artwork is the earlier site asset, not a verified label/specification photo. The newly supplied chat bottle and product-range images need local files before replacing that asset. No portraits were supplied; client approved text leadership profiles.
5. Confirm actual sizes, pack quantities, specifications, factory address and credentials before adding them. Avoid unsupported mineral-water, purity-test, spring-source or health claims.
6. Maintain business listings, earn authentic customer reviews and track city-level organic enquiries in Search Console. Do not buy reviews or publish duplicate city pages with swapped place names.

Google explains local visibility in terms of relevance, distance and prominence, not title tags alone:
https://support.google.com/business/answer/7091

Structured data guidance:
https://developers.google.com/search/docs/appearance/structured-data/organization
https://developers.google.com/search/docs/appearance/structured-data/local-business

## Asset / contact notes

Official contact from client: +91 8169456633, GangaShreeroots@gmail.com. The WhatsApp message sender number is not used as the company contact. No WhatsApp capability is assumed for the official number.
The company currently has text leadership profiles, as authorized. No stock face is presented as a real executive. Product flavour graphics are decorative type compositions, not packaging photographs.
