# Sirjna Handbook — Unified Design, Product & Vision Guide
*(Build: Frappe v15 · Hosted on Frappe Cloud)*

## 0. Mission & Ethos
Sirjna (सिर्जना · “to create”) is an honest, engineering-first mentorship platform for Indian B.E./B.Tech./M.Tech. students targeting MS/MEng in the U.S. or top-tier Canada.

> **One flat fee. No upsells. No agents. No visa/legal filing. No fake promises.**

### Core Principles
- Engineering-grade honesty: precision, transparency, and integrity.
- Student + parent clarity: no jargon, no hidden terms.
- Educational mentorship only: never legal or immigration services.
- Tax-included flat pricing: Founders $349; Standard $499; Advisory $25 creditable.
- Everything documented: guidance happens inside the **Sirjna Portal**, not on endless calls.

---

## 1. The Extended Vision — From Mentorship to Creation
Sirjna starts with guidance but grows into a lifetime network of engineers.

- We mentor students from first decision to first job.
- We build a **pool of wisdom** (every solved issue becomes a guide).
- We build a **pool of talent** (every mentored student joins our professional network).

When knowledge and talent meet, ideas emerge — and we’ll nurture them.

> **Sirjna Labs (future)**  
> The incubator for alumni who want to build.  
> - Mentorship for research and startup ideas  
> - Access to domain experts and early resources  
> - A collaborative ecosystem across engineering disciplines

**Long-term aim:** turn students into professionals, professionals into innovators, and innovators into mentors.

> “First, we guide you. Then, we build with you.”

---

## 2. Mentorship Model
| Phase | Focus | Tagline |
|-------|--------|---------|
| **Sankalp** | Clarity, profile building, test planning | *Dream clearly.* |
| **Udaan** | Application & pre-departure | *Launch fearlessly.* |
| **Nirman** | On-campus success & first job | *Build smart.* |
| **Pragati** | Career growth & leadership | *Grow endlessly.* |

Students can join any phase individually or complete all four.

**How it works**
- All interactions happen via the **Portal**.
- Students post screenshots/issues; mentors reply within **24 hours**.
- Each answer is written, stored, and re-usable — your learning record grows automatically.
- Mentorship steps unlock sequentially; each phase advances at 100 % completion.
- Parents can view progress; mentors manage assigned students.

> “Real engineers don’t repeat errors — they document fixes.”

---

## 3. Brand & Tone

### 3.1 Voice
| Attribute | Description | Example |
|------------|--------------|----------|
| **Honest** | Tell the truth, even if it’s simple. | “We’re not agents. We’re engineers.” |
| **Warm** | Sound human, not corporate. | “Hey, we’ve been there — the 2 a.m. form confusion.” |
| **Direct** | Short sentences. Active voice. | “No hidden costs. No fake urgency.” |
| **Engineerly** | Logical, precise, factual. | “$499 flat — tax included.” |
| **Playful** | Small human touches, humor, or doodles. | “Yes, we like gold accents — engineers need style too.” |
| **Motivational** | Inspire without exaggeration. | “Your next experiment is your next step forward.” |

Formal tone only for Terms, Privacy, and legal pages.

### 3.2 Copy Principles
- Use “you”, “we”, and conversational transitions.
- One idea per paragraph.
- Alternate rhythm: serious → hopeful → factual → punchline.
- Always end with a **call or curiosity hook**.
- Avoid hype words: empower, premium, transform, guarantee.

### 3.3 Visual Personality
- Base palette: black / white; soft dotted background.
- Accent: gold (#d4af37) or electric blue for hand-drawn highlights.
- Font: Inter + Poppins (system-UI fallbacks).
- Interaction: subtle hover, hand-scribble SVG animations.
- Layout rhythm: wide margins, 1.6–1.8 line-height, max 80 ch width.

---

## 4. Web Experience — Public Site
**Tally-style flow:**
1. Hero → Built by engineers who’ve done it — for engineers who will. CTA buttons.
2. The Spark → story of late-night confusion → idea of Sirjna.
3. The System → 4-phase cards.
4. The Humans → mentors’ hourly worth.
5. The Honest Math → Why $499.
6. Founder Cohort → $349 offer + refund + referrals.
7. Portal Explained → “No calls · 24 h response · Everything documented.”
8. Stories → quotes & testimonials.
9. CTA Footer → “Ready to build your story?”

---

## 5. Portal Design
| Role | View | Key Elements |
|------|------|---------------|
| **Student** | 3-column grid | Left – timeline; Center – active task; Right – progress + resources. |
| **Parent** | Read-only summary | Phase · % · Next actions · FAQ link. |
| **Mentor** | Queue dashboard | Pending reviews · Today’s sessions · New students. |

**UI Traits**
- White cards, black text, gold active markers.
- 40 px touch targets.
- Focus outlines kept for accessibility.
- Task cards show status chips (Pending · In Progress · Done).

---

## 6. Pricing, Founder Cohort & Referral
| Plan | Fee (USD) | Notes |
|------|------------|-------|
| **Founder Cohort (101)** | $349 | 1 refund winner · 10 % referrals |
| **Standard Mentorship** | $499 | All phases included |
| **1-on-1 Advisory** | $25 | Credited if you join |

**Referral Program**
- 10 % reward → visible + 1 day · withdrawable + 14 days.
- Redeem via gift card / credit / UPI (capped $600 yr).
- One-level · no MLM · fraud guard.

---

## 7. Backend Architecture (Frappe v15)
- App: `sirjna`
- Repo: `SirjnaUSA/sirjna`
- Hosting: Frappe Cloud
- Stack: Python + JS + MariaDB
- Integrations: Stripe · Zoom · Google OAuth

**DocTypes:** Student Profile, Test Score, University, Program Deadline, Shortlist, Shortlist Entry, Mentorship Step, Student Progress, Webinar, Webinar Registration, Advisory Session, Payment Record, Resource Pack, Referral Link, Referral Credit, Payout Request, Sirjna Settings.

**Automation:** progress recalculation, phase auto-advance, Stripe webhook, referral update, webinar reminders.

**Guards:** graceful disable for missing keys.

---

## 8. Optional Integrations
Drive · Insights · Wiki · CRM · Builder/Gameplan/Books — all toggleable.

---

## 9. Operations & SOP
**Daily:** check payments, reply < 24 h, verify Zoom.
**Weekly:** metrics, backup, permissions.
**Monthly:** rotate keys, refresh content, test flow.

Support = factual + kind + concise.

---

## 10. Legal
**Terms:** educational only, refund before first session, AZ law.
**Privacy:** data = profile + payments + logs, no selling, legal retention, cross-border disclosure.

---

## 11. Content & Vibe Guidelines
| Medium | Vibe | Goal |
|--------|------|------|
| Website | Playful + direct | Excite + build trust |
| Portal UI | Clear + reassuring | “You’re on Step 3 of 10.” |
| Emails | Short + personal | “Hi Ananya – your portal is live.” |
| Social | Conversational + smart | Myth-busting, real stories |
| Webinars | Educational + energetic | Inspire with data + honesty |
| FAQ | Human Q&A | Real answers |
| Legal | Formal + neutral | Compliance |
| Internal Docs | Technical + precise | Mentor & ops clarity |

---

## 12. Motivation & Storytelling
- Emotion → Logic → Hope.
- Celebrate small wins.
- Engineering analogies.
- Motivational quotes and alumni snippets.
- Smart humor, cultural respect.

---

## 13. References
tally.so · frappe.io · ambitio.club · yocket.com · ncees.org

---

## 14. Repo Layout
```
sirjna/
  sirjna/
    api/
    doctype/
    public/css/sirjna.css
    templates/includes/
    www/
      index.html
      how-it-works.html
      pricing.html
      webinars.html
      advisory.html
      apply.html
      faq.html
      about.html
      terms.html
      privacy.html
      portal.html
requirements.txt
MANIFEST.in
```

---

## 15. Closing Line
> **Sirjna — Honest Mentorship for Engineers.**  
> Built in India. Guided in the USA. Designed for a lifetime of creation.
