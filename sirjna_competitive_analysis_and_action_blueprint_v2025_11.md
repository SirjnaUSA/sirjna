
# Sirjna Competitive Analysis & Action Blueprint (v2025.11)

## 1. Executive Summary
Sirjna’s niche — Indian BE/BTech/MTech students targeting MS/MEng in USA/Canada — is underserved by both traditional agents and AI-first startups. The key differentiators are: flat pricing, documentation-first mentorship, and lifecycle support (Sankalp→Udaan→Nirman→Pragati).

Competitors (Zyra, Ambitio, Kollegio, LeapScholar, IvyWise, GeeBee, Edwise, AECC, KC Overseas, LeverageEdu, PassionPrep) either focus only on pre-admission or broad, generic study-abroad services. None combine human mentorship, structured phases, and engineering-specific career support.

---

## 2. Strategic Positioning

| Axis | Sirjna | Competitors |
|------|---------|--------------|
| Focus | Engineering MS/MEng USA/Canada | Broad disciplines |
| Lifecycle | Full (pre → job) | Mostly pre-admission |
| Delivery | Asynchronous portal + human mentors | Calls/emails |
| Pricing | Flat USD fee + referral | Variable or % based |
| Ethos | No ghostwriting, no commissions | Mixed practices |
| Brand | Honest, engineerly, warm | Agent / academic / AI |
| Goal | Build creators & mentors | Sell admissions |

---

## 3. Strengths

1. **Niche clarity** — single clear audience, easier SEO & message targeting.
2. **Lifecycle coverage** — first job & career growth phases are unique.
3. **Portal-first workflow** — 24h SLA, reusable documentation.
4. **Transparent pricing** — builds trust immediately.
5. **Engineering mentors** — practical credibility.
6. **Referral system** — low-CAC virality.

---

## 4. Weaknesses & Remedies

| Weakness | Fix | Frappe Implementation |
|-----------|-----|------------------------|
| Low social proof | Create “Results/Voices” page with real stories. | Static web page `/www/voices.html`; Doctype `Student Result`; query data to render quotes/cards. |
| Top-of-funnel reach | Weekly webinars and $25 advisory CTA. | `Webinar` Doctype + Scheduler for reminders; add CTA on every web page using `frappe.ui.form.on` snippet. |
| Perceived rigor | Add Roundtable Review (peer + mentor). | `Review Round` Doctype linked to `Student Progress`. Workflow: Submitted→Reviewed→Published. |
| AI convenience gap | Build in-portal Copilot (FAQ autocomplete, checklist suggestions). | Custom Script API endpoint `/api/method/sirjna.api.copilot`; restrict to internal dataset using LlamaIndex or pre-uploaded Markdown. |
| Scholarship info thin | Build “Funding Playbook” resource pack. | New `Resource Pack` entry tagged “Funding”; render markdown via `frappe.render_template`. |
| University data freshness | Program Deadline monitor + scrape. | Script in `/doctype/program_deadline/cron.py`; schedule hourly/daily update; flag `last_verified_on`. |
| Career outcomes articulation | Publish Nirman→Pragati ladders. | Portal section `/www/career-tracks.html`; fetch content from `Resource Pack`. |

---

## 5. Feature Build Roadmap (Frappe v15)

### P0 (Now → 2 weeks)
1. **Mentorship Steps v1.0**
   - Define 10–14 steps for Sankalp & Udaan.
   - Doctype `Mentorship Step` → Field `order_index`, `phase`, `title`, `rubric` (HTML).

2. **Shortlist 5/5/5 Generator**
   - Create Python method to auto-pick Safe/Target/Reach universities.
   - Use `University` + `Program Deadline` Doctypes; add mentor review status.

3. **SOP/LOR Originality Policy**
   - Upload to `Resource Pack`; add checkbox “Acknowledged” before submission.

4. **Voices Page**
   - `/www/voices.html` with Jinja template fetching `Student Result` entries.

5. **Webinar Factory**
   - Reuse `Webinar` + `Webinar Registration` Doctypes.
   - Daily scheduler sends T-24h reminder via `frappe.sendmail()`.

---

### P1 (3–6 weeks)
1. **Portal Copilot**
   - Backend: Python endpoint `/api/method/sirjna.api.copilot.ask`.
   - Frontend: Custom Desk widget or Chat bubble.
   - Trained on markdown from `/sirjna/docs/guides/` using FAISS or simple Q/A JSON.

2. **Funding Playbook**
   - Single `Resource Pack` entry with Markdown.
   - Web CTA: “Download Free Funding Playbook” → creates `Lead`.

3. **Roundtable Review Workflow**
   - Add Doctype `Review Round`.
   - Link mentors → reviewers → comments.
   - Hook: `on_submit` → notify primary mentor.

4. **Nirman Playbooks**
   - Create guides for resume, research assistantship, on-campus jobs.
   - Host under `/www/resources/nirman.html`.

---

### P2 (6–12 weeks)
1. **Deadline Verifier**
   - Cron job in `hooks.py`: `daily_at("02:00")` to update `Program Deadline`.
   - Add color-coded “verified” tags in portal view.

2. **Referral Wallet UI**
   - Web page `/portal/referral` pulling `Referral Credit` entries.
   - Enable payout request submission.

3. **Pragati Track (Career Growth)**
   - Add Mentorship Steps for career licensing (PE, EIT).
   - Create template docs + checklists.

---

## 6. Growth Tactics

1. **Founder Cohort Campaign**
   - Add live counter in `/www/pricing.html` using Frappe REST call: count `Student Profile` where `is_founder=1`.
   - Trigger confetti animation via JS once count <101.

2. **University Landing Pages**
   - Auto-generate `/www/university/<slug>.html` using Program data.
   - Include: deadlines, GRE requirement, SOP hints, faculty tags.

3. **Webinar + Advisory Funnel**
   - Scheduler runs weekly; email sequence: register → join → post-webinar CTA to $25 Advisory.

4. **YouTube & Blog Integration**
   - Use Frappe Blog module; each video = new Blog Post with embedded iframe.

---

## 7. Operational Quality Framework

| Metric | Target | Implementation |
|---------|---------|----------------|
| Mentor first response time | ≤24h | Compute delta in `Student Progress.after_insert`; log in `Response Log` Doctype. |
| Resolution time | ≤72h | Auto flag to Ops via Notification Rule. |
| SLA visibility | Show timers in portal UI (Jinja template logic). |
| Originality | 100% adherence | Add pre-submit warning + AI check endpoint (optional). |

---

## 8. Content Strategy

### Web
- Add “Results”, “Funding”, “Career Tracks” pages.
- Tally-style structure: Hero → Story → System → Humans → Math → Founder → Portal → Voices → CTA.

### Portal
- Gold accent, dotted background, 3-column layout.
- Dynamic progress bar from `Student Progress.progress_pct`.
- “Report Issue” button triggers form → saves `Support Issue` Doctype.

### Social
- Weekly myth-busting post (visa, SOP originality, scholarship myths).
- Share micro-wins of students (“First admit from Chandigarh!”, “First RA offer from Purdue!”).

---

## 9. Infrastructure Tips for Frappe v15

- Keep each phase’s logic modular: create `sirjna.utils.progress.py` for progress auto-calculations.
- Use **single DocType for Settings** (`Sirjna Settings`) to store keys & feature toggles (Zoom, Stripe, AI Copilot).
- Write **idempotent webhooks** for Stripe; ensure Payment Record is updated via `on_update` handler.
- Use **Scheduler Events** for:
  - Webinar reminders.
  - Referral status updates.
  - Deadline verifier.
- Prefer **Jinja + server templates** for static pages (simpler than JS SPAs).
- Commit fixtures regularly (`bench export-fixtures`).
- Test via Frappe’s unit tests (`frappe.tests.utils.FrappeTestCase`).

---

## 10. Message to Team
> “While others stop at admission, we mentor till your first job.”  
> That’s the moat. Own it, prove it, document it.
