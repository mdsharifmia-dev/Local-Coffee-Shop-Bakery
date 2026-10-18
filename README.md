# ☕ Local Coffee Shop & Bakery - Website

A modern, high-performance, responsive static website designed for an artisanal local coffee shop and bakery. Built with clean semantic HTML5, CSS3, and vanilla JavaScript.

---

## 📁 File Structure

```text
├── index.html       # Homepage (Hero, Highlights, Reviews, Hours)
├── about.html       # About Us (Story, Milestones, Craft Process, Values)
├── menu.html        # Menu & Online Ordering (Brews, Pastries, Order Modal)
├── gallery.html     # High-resolution Photo Gallery
├── contact.html     # Contact details, Inquiry Form & Google Maps
├── 404.html         # Custom branded 404 Not Found page
├── style.css        # Complete responsive design & Nordic Specialty theme
├── script.js        # Mobile hamburger, Menu filters, WhatsApp Ordering
├── favicon.svg      # Crisp vector coffee cup favicon
├── robots.txt       # Search engine crawler directives
└── sitemap.xml      # Search engine indexing map
```

---

## 🚀 How to Host & Go Live (Free in 2 Minutes)

### Option 1: Netlify Drop (Easiest - Drag & Drop)
1. Visit **[app.netlify.com/drop](https://app.netlify.com/drop)**.
2. Drag and drop this entire project folder into the browser.
3. Your website goes live with a free custom SSL (`https://...netlify.app`) immediately!

### Option 2: GitHub Pages (Free forever)
1. Create a repository on GitHub.
2. Push or upload these files to the repository.
3. Go to **Settings** > **Pages** > Select `main` branch > **Save**.
4. Your site will be live at `https://<your-username>.github.io/<repo-name>/`.

### Option 3: Vercel or Cloudflare Pages
- Import repository or deploy using the `vercel` CLI.

---

## ⚙️ Customization Guide

1. **WhatsApp Ordering Phone Number**:
   - Open `script.js`.
   - On line 8, set `const COFFEE_SHOP_WHATSAPP_NUMBER = "8801XXXXXXXXX";` (with country code, no `+` or spaces).
   - Orders placed from the menu will instantly open a pre-filled WhatsApp message to your phone!

2. **Operating Hours**:
   - Update hours in `index.html` and `contact.html` under the `<section class="hours-section">`.

3. **Menu Items & Pricing**:
   - Open `menu.html` to add, edit, or adjust prices and descriptions.

---

## 🛡️ Security & Performance Standards
- Zero external build dependencies (100% lightweight & fast).
- Safe from DOM XSS (`textContent` + `encodeURIComponent`).
- Tabnabbing secured with `rel="noopener noreferrer"`.
- Mobile-first responsive with responsive media queries.
- SEO-ready with OpenGraph metadata, `robots.txt`, and `sitemap.xml`.
