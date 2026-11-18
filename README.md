# Selepe & Associates Inc – website

Static, multi-page site built with **Tailwind CSS 3**. The finished pages and compiled CSS are already in this folder, so you can upload it to any web host as-is (open `index.html` to preview).

## Pages

| File | Purpose |
|---|---|
| `index.html` | Home (Van der Merwe layout, Selepe content) |
| `about.html` | Who we are, vision, mission, values, founder's message |
| `services.html` | The nine areas of legal service |
| `subscriptions.html` | Legal-as-a-Service plans with category tabs |
| `corporate.html` | CLS, Managed Legal Ops, EOPS, correspondent services, performance-based recoveries |
| `industries.html` | Client groups and sectors |
| `how-we-work.html` | Engagement process, partnership journey, Legal Interact, why choose us |
| `academy.html` | LEAP Academy |
| `leadership.html` | Thabo's profile, governance and compliance |
| `contact.html` | Enquiry form, WhatsApp, address |

## Editing

Page content lives in `src/pages/*.html` (the `<main>` content only). `src/build.py` wraps each page in the shared head, header and footer and writes the finished HTML to the site root. Contact details, nav links and the footer are defined once in `src/build.py`.

```bash
npm install          # once
npm run build        # rebuild pages + compile Tailwind
npm run watch:css    # recompile CSS while you edit
```

Brand tokens (navy, gold, silver, cream, fonts) are in `tailwind.config.js`. Reusable component classes (`.btn-gold`, `.card`, `.eyebrow`, `.tile`, `.field`, …) are in `src/input.css`.

## Replacing placeholder images

Each image slot tries a real photo first and falls back to a generated placeholder, so replacing is drop-in. Save your file with the name below in `img/` and it takes over.

| Save as | Used for | Suggested size |
|---|---|---|
| `img/hero.jpg` | Home hero background (right side is visible; keep the left calm) | 2400 × 1200 |
| `img/boardroom.jpg` | Home "About" panel | 1000 × 1100 |
| `img/skyline.jpg` | Home sectors panel, Industries page | 1600 × 900 |
| `img/thabo.jpg`, `img/thabo-sq.jpg` | Founder portrait (currently cropped from the flyer; replace with a proper studio photo) | 1200 × 1300 / 600 × 600 |

The logo (`img/logo.png`) was extracted from the company profile PDF. A vector or higher-resolution export would sharpen it.

## Contact form

Set `FORM_ENDPOINT` at the top of `assets/site.js` to a Formspree, Laravel or other endpoint. While it is empty, the form opens the visitor's email app addressed to `info@selepe.co`. A honeypot field is already in place.

## Open items

- LinkedIn page, Legal Practice Council registration, Fidelity Fund Certificate, VAT and B-BBEE details are still `[to be inserted]` in the company profile, so they are **not** shown on the site. Add them to `src/build.py` (footer) and `leadership.html` when available.
- The mockup's stats ("250+ matters", "98% successful outcomes"), testimonial and "track record" section were replaced with verifiable facts from the company profile. Add real case studies or client endorsements later, and check the Legal Practice Council's rules on attorney advertising before publishing outcome statistics.
- Subscription prices are shown as published in the 2027 company profile. Update them in `subscriptions.html` if they change.
- Add Open Graph share image (`img/og.jpg`) and social links when ready.
