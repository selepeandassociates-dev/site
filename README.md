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

The Home and Industries page pictures are designed for **2048 × 768 px** (about 8:3, JPG). Each slot tries your file first and falls back to a generated placeholder, so replacing is drop-in: save the file with the name below in `img/`.

| Save as | Where it appears | Composition tip |
|---|---|---|
| `img/hero.jpg` | Home hero background | Keep the left 45% calm and dark; the headline sits there. Subject on the right. |
| `img/boardroom.jpg` | Home page middle column beside "About Our Firm" and "Our Services" | **16:9**, about 1600 × 900 px. Keep the main subject in the centre; the sides crop slightly on some screens. |
| `img/skyline.jpg` | Home "Sectors We Serve" panel and the Industries page | Shown at roughly 16:9 on desktop, so keep the subject near the centre. |
| `img/thabo.jpg` | Portrait on the About and Leadership pages | Portrait-style crop, about 1200 × 1300 px (4 : 4.3). Head and shoulders, face in the upper half. |
| `img/thabo-sq.jpg` | Small round portrait in the Home "Why Choose Us" band | Square, 600 × 600 px, face centred. |

On phones the wide banners crop to a taller shape (3:2), so keep important subjects away from the far left and right edges.

`img/hero.jpg` (2048 × 768) and `img/boardroom.jpg` (16:9) are your supplied pictures, compressed to JPG (about 250-300 KB each). `img/skyline.jpg` is your supplied city skyline (about 2048 px wide). Keep new pictures under about 400 KB.

The logo (`img/logo.png`) was extracted from the company profile PDF. A vector or higher-resolution export would sharpen it. `img/thabo.jpg` and `img/thabo-sq.jpg` are currently cropped from the flyer, so replace them with proper portraits.

## Contact form

Set `FORM_ENDPOINT` at the top of `assets/site.js` to a Formspree, Laravel or other endpoint. While it is empty, the form opens the visitor's email app addressed to `info@selepe.co`. A honeypot field is already in place.

## Open items

- LinkedIn page, Legal Practice Council registration, Fidelity Fund Certificate, VAT and B-BBEE details are still `[to be inserted]` in the company profile, so they are **not** shown on the site. Add them to `src/build.py` (footer) and `leadership.html` when available.
- The mockup's stats ("250+ matters", "98% successful outcomes"), testimonial and "track record" section were replaced with verifiable facts from the company profile. Add real case studies or client endorsements later, and check the Legal Practice Council's rules on attorney advertising before publishing outcome statistics.
- Subscription prices are shown as published in the 2027 company profile. Update them in `subscriptions.html` if they change.
- Add Open Graph share image (`img/og.jpg`) and social links when ready.
