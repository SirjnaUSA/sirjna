# Sirjna — Full Design, System & Implementation Handbook (v2025.11.07)

## 0. Overview
Sirjna (सिर्जना · “to create”) is an honest, engineering-first mentorship platform for Indian B.E./B.Tech./M.Tech. students targeting MS/MEng in the USA or Canada. Mentorship happens via the Frappe Portal, not phone calls—every issue documented, every reply reusable.

Flat-fee mentorship: Founder $349 (first 101) · Standard $499 · Advisory $25 (credited if joining). Referral: 10% reward visible +1 day, withdrawable +14 days. No agents, upsells, or visa filing. Long-term vision: Sirjna Labs incubator for alumni ideas/startups.

---

## 1. Mission & Extended Vision
Help engineers from first decision to first job and beyond. Build:
- **Pool of Wisdom:** issues → reusable guides.
- **Pool of Talent:** students → lifelong network.

When knowledge + talent meet → innovation. Future: **Sirjna Labs**, an incubator for alumni research/startup projects. Mentorship → Mastery → Creation.

> “First, we guide you. Then, we build with you.”

---

## 2. Phases
| Phase | Focus | Tagline |
|-------|--------|---------|
| Sankalp | profile/test planning | Dream clearly |
| Udaan | apply + pre-arrival | Launch fearlessly |
| Nirman | on-campus & first job | Build smart |
| Pragati | career growth | Grow endlessly |

Students may join any phase.

---

## 3. Philosophy
- All communication inside Portal. No random calls. Screenshot + note → mentor reply ≤24h.
- Replies are documented; issues become guides.
- Parents: read-only dashboards.
- Mentors: full-time engineers volunteering part-time.

---

## 4. Pricing Logic
Mentors earn $90–$150/hr in real life; firms bill $300–$500/hr. $499 is <1% of first-year salary—affordable, fair, sustainable. We charge for time, not hype.

---

## 5. Brand & Tone
Voice: honest · warm · direct · engineerly · playful · motivational.  
Website vibe: Tally.so—monochrome, dotted bg, one accent (#d4af37 gold), Inter/Poppins font.  
Structure: emotion → logic → hope.  
Formal tone only for legal. Short sentences. Conversational “you/we”.

---

## 6. Website (Public)
**Pages:** Home, How It Works, Pricing, Webinars, Advisory, Apply, FAQ, About, Terms, Privacy, Contact, Login.

**Layout:** hero → story → system → humans → math → founders → portal → voices → CTA.

**Header:** logo, nav (Home, How It Works, Pricing, FAQ, Login), CTAs (Webinar, 1-on-1, Apply).  
**Footer:** About, Webinars, Advisory, Apply, Privacy, Terms, Contact. Tagline: “$499 tax-included · educational mentorship only.”

### Sections
- **Home:** hero (“Built by engineers…”), 4-phase cards, why $499, Founder Cohort, Portal model, CTA.  
- **How It Works:** async support explained, portal screenshots, 24h SLA.  
- **Pricing:** table (Founder $349, Standard $499, 1-on-1 $25 credited), refund policy.  
- **Webinars:** list, register form, reminders.  
- **Advisory:** booking form, Stripe link.  
- **Apply:** form → Student Profile + Stripe checkout.  
- **FAQ:** honest answers.  
- **About:** origin story, mentor ethos, incubator hint.  
- **Terms/Privacy:** legal tone.

---

## 7. Portal UX
Grid: Left timeline | Center task | Right progress/resources.  
Help: “Report Issue” → upload screenshot + note → mentor reply ≤24h → documented.  
Parent: read-only. Mentor: queues (pending reviews, issues, new signups).  
Theme: white cards, black text, gold highlights, 40px targets.

---

## 8. DocTypes
Student Profile; Test Score; University; Program Deadline; Shortlist; Shortlist Entry; Mentorship Step; Student Progress; Webinar; Webinar Registration; Advisory Session; Payment Record; Resource Pack; Referral Link; Referral Credit; Payout Request; Sirjna Settings (Single).

---

## 9. Workflows
- **Mentorship Progress:** Step done → recompute % → auto-advance phase → email.  
- **Payments:** Stripe checkout ($25/$349/$499) → webhook → Payment Record Paid → create Student Profile → welcome.  
- **Referrals:** Paid + referral_code → Referral Credit (Pending→Available→Withdrawable after 14 days).  
- **Issues:** student posts screenshot → mentor reply → mark resolved → becomes guide.  
- **Webinars:** reminders T-24h.

---

## 10. Repo Layout
```
sirjna/
  api/
  doctype/
  public/css/sirjna.css
  templates/includes/
  www/
    index.html how-it-works.html pricing.html webinars.html advisory.html
    apply.html faq.html about.html terms.html privacy.html portal.html
requirements.txt MANIFEST.in
```

---

## 11. Optional Integrations
Drive, Insights, Wiki, CRM, Builder/Gameplan/Books — toggled in Sirjna Settings.

---

## 12. Operations
Daily: payments, issues (<24h), Zoom.  
Weekly: metrics (CPL, Lead→Paid, Refunds), backup, perms audit.  
Monthly: rotate keys, refresh content, test payment.  
Support ≤3 sentences, factual & kind.

---

## 13. Legal
Terms: educational only, refund pre-session, AZ law.  
Privacy: processed via Stripe/Zoom/email, no selling, GDPR/India compliant.

---

## 14. Content Tone Matrix
| Medium | Vibe | Goal |
| Website | playful + direct | excite + trust |
| Portal | clear + reassuring | progress clarity |
| Emails | short + personal | human touch |
| Social | conversational + smart | myth-busting |
| Webinars | educational + energetic | motivate |
| FAQ | human Q&A | honest info |
| Legal | formal | compliance |
| Internal | technical | accuracy |

---

## 15. Storytelling & Motivation
Use emotion→logic→hope rhythm. Real quotes: “Every expert was once an international student filling their first form.” Celebrate small wins. Engineering analogies. Dry humor ok.

---

## 16. Implementation via Frappe Desk

### Step 0 – Prep
- Set site, favicon/logo, email account, roles (Student, Parent, Mentor, Ops, Admin).

### Step 1 – Create DocTypes
Use Developer > DocType. Add fields & permissions: Students (self-only), Parent (read-only), Mentor (assigned).

### Step 2 – User Permissions
Bind Student→their Profile, Parent→child’s Profile.

### Step 3 – Sirjna Settings
Add keys, webhook secrets, toggles.

### Step 4 – Navigation
Add Top Bar Items (Home, How It Works, Pricing, FAQ, Login, CTAs). Add Portal Menu (Dashboard, Shortlist, Docs, Wallet).

### Step 5 – Static Pages
Create web pages for each URL. Upload sirjna.css. Add highlights/SVGs manually.

### Step 6 – Web Forms
- Apply form → Student Profile.  
- Webinar Registration form → Webinar.

### Step 7 – Mentorship Steps
Create steps per phase with order_index.

### Step 8 – Notifications
Set triggers (Payment Paid→Welcome; Progress Done→Phase Advance).

### Step 9 – Payments
Initially use Stripe Payment Links; replace later with Checkout Session webhook.

### Step 10 – Founder Logic
If <101 founders, set is_founder=1 and charge $349; else $499. Create report “Founder Cohort (<=101)” for visibility.

### Step 11 – Shortlist
Manually create 5/5/5 entries → mentor reviews → publish.

### Step 12 – Referrals
Create Referral Link per student. Manual creation of credits first. Add Wallet card to portal. Daily report for status flips.

### Step 13 – Support Issues
Enable attachments/comments; add “Report Issue” button on Student Progress. Saved Report “Issues last 24h”.

### Step 14 – Emails
Templates: Welcome, Phase Advance, Referral Credit Available, Webinar Reminders.

### Step 15 – Parent Portal
Portal Settings → new page pulling phase/%/next actions via Jinja.

### Step 16 – Mentor/Ops Console
Workspace “Sirjna Ops”: Payment Records not Paid, Issues 24h, Today’s Sessions, Founder count, Referral credits pending.

### Step 17 – Legal Pages
Create /terms and /privacy; paste finalized content.

### Step 18 – QA
Simulate Apply→Payment→Portal. Verify progress % auto, notifications, issue flow.

### Step 19 – Analytics (optional)
Add Frappe Insights dataset or simple visitor counter.

### Step 20 – Launch
Switch to Live Stripe keys, publish webinars, open Founder Cohort.

---

## 17. Ongoing Routine
Daily: respond <24h; process payments.  
Weekly: metrics & backups.  
Monthly: refresh + test.  

---

## 18. Core Quote
> **“Sirjna — Honest Mentorship for Engineers. Built in India. Guided in the USA. Designed for a lifetime of creation.”**
