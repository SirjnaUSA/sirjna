# Sirjna Frappe Desk Setup — Steps 0 to 2

This document records every configuration and DocType setup done in Frappe v15 Desk for the Sirjna mentorship platform.

---

## 0) Prereqs (once)

### Roles & Access
- Role: **System Manager** (+ Developer role if required).
- Path: Desk → Developer → DocType must be visible.
- Module: **Sirjna**
- Naming Rule Default: `By script`
- Autoname Format: `format:CODE-{####}`

### Basic Setup
1. **Website Settings**: Title “Sirjna”, logo + favicon uploaded.
2. **Email Account**: contact@sirjna.com via smtp.hostinger.com (SSL 465).
3. **Roles**: Student, Parent, Mentor, Ops, Admin.
4. **User Permissions**: Students see only their own data; parents read-only linked child.

---

## 1) Creation Order

Child Tables:
1. Test Score
2. Program Deadline
3. Shortlist Entry

Masters & Transactions:
4. Student Profile
5. University
6. Shortlist
7. Mentorship Step
8. Student Progress
9. Webinar
10. Webinar Registration
11. Advisory Session
12. Payment Record
13. Resource Pack
14. Referral Link
15. Referral Credit
16. Payout Request
17. Sirjna Settings (Single)

---

## A) Child Tables

### Test Score
- Is Child Table ✅, Editable Grid ✅, Autoname: `hash`
- Fields:
  - Type (Select → GRE, IELTS, TOEFL, None)
  - Date Taken (Date)
  - Score Total (Data or Int)

### Program Deadline
- Is Child Table ✅, Autoname: `hash`
- Fields:
  - Term (Select → Fall, Spring)
  - Deadline Type (Select → Priority, Final, Scholarship)
  - Deadline Date (Date)

### Shortlist Entry
- Is Child Table ✅, Autoname: `hash`
- Fields:
  - University (Link → University)
  - Tier (Select → Safe, Target, Reach)
  - Rationale (Small Text)

---

## B) Core DocTypes

### Student Profile
- Autoname: `format:SP-{####}`
- Is Submittable ❌, Track Changes ✅
- Title Field: full_name
- Fields:
  - User (Link → User)
  - Full Name, Email, Phone (Data)
  - Degree Level (Select → BE, BTech, MTech)
  - Discipline (Data)
  - GPA Scale, GPA Value (Float)
  - Tests (Table → Test Score)
  - Status Phase (Select → Sankalp, Udaan, Nirman, Pragati)
  - Progress % (Percent, Read Only, Default 0)
  - Country Target (Select → US, Canada)
  - Intake Term (Select → Fall, Spring)
  - Intake Year (Int)
  - Is Founder (Check)
  - Notes (Private) (Small Text)
- Permissions:
  - Student: Read/Write (If Owner ✅)
  - Parent: Read
  - Mentor/Ops: Read/Write
  - Admin: All

### University
- Autoname: `format:UNI-{####}`
- Title Field: university_name
- Fields: name, country, department, program, rank_band, deadlines (Program Deadline), est_fees_usd, notes, category_default (Safe/Target/Reach)

### Shortlist
- Autoname: `format:SL-{####}`
- Fields: student (Link → Student Profile), entries (Table → Shortlist Entry), generated_by (Manual/Rule/AI), confidence_notes (Small Text)

### Mentorship Step
- Autoname: `format:STEP-{####}`
- Fields: phase (Sankalp/Udaan/Nirman/Pragati), title (Data), desc_md (Text Editor), requires_upload (Check), help_video_url (Data), order_index (Int)

### Student Progress
- Autoname: `format:PROG-{####}`
- Fields: student (Link → Student Profile), step (Link → Mentorship Step), status (Pending/In-Progress/Done), uploaded_doc (Attach), completed_on (Datetime), issue_thread (Long Text)

### Webinar
- Autoname: `format:WEB-{####}`
- Fields: title (Data), start_at (Datetime), duration_min (Int), zoom_meeting_id, zoom_join_url, zoom_start_url

### Webinar Registration
- Autoname: `format:WR-{####}`
- Fields: webinar (Link → Webinar), student_email (Data), user (Link → User), status (Registered/Attended/No-show)

### Advisory Session
- Autoname: `format:ADV-{####}`
- Fields: student, slot_start, slot_end, is_paid, stripe_session_id, zoom_meeting_id, status (Booked/Completed/No-show), credit_applied (Check)

### Payment Record
- Autoname: `format:PAY-{####}`
- Fields: student (Link → Student Profile), purpose (Advisory_25/Mentorship_349/Mentorship_499), amount_usd (Currency), stripe_payment_intent (Data), status (Created/Paid/Refunded/Failed), invoice_url, referral_code_used, referrer_user (Link → User)

### Resource Pack
- Autoname: `format:RES-{####}`
- Fields: scope (University/City/Phase), scope_ref (Dynamic Link), phase (Sankalp/Nirman/Pragati), content_md (Text Editor)

### Referral Link
- Autoname: `format:REFL-{####}`
- Fields: owner_user (Link → User), code (Data Unique), url (Data Read Only), total_credited, total_paid_out (Currency), is_active (Check)

### Referral Credit
- Autoname: `format:REFC-{####}`
- Fields: referrer_user (Link → User), referred_student (Link → Student Profile), payment_record (Link → Payment Record), amount_usd (Currency), status (Pending/Available/Locked/Paid), visible_on, withdrawable_on (Datetime), notes (Small Text)

### Payout Request
- Autoname: `format:PAYO-{####}`
- Fields: requester_user (Link → User), method (Select → Visa Gift Card, Amazon Gift Card, UPI, Account Credit), amount_usd (Currency), kyc_status (Not Required/Pending/Verified/Rejected), status (Created/Approved/Sent/Failed), evidence_url (Data)

### Sirjna Settings (Single)
- Is Single ✅
- Fields:
  - Mode (Select → Test/Live)
  - Stripe keys (Publishable/Secret/Webhook for Test + Live)
  - Zoom credentials (Account ID, Client ID, Client Secret)
  - Enable toggles (Referrals, Drive, Insights, Wiki, CRM)
  - Payout Min USD (Int default 25)
  - Payout Methods (Code JSON)

---

## C) Permissions Templates
| DocType | Permissions |
|----------|-------------|
| Student Profile / Student Progress / Shortlist | Student: Read/Write (If Owner ✅), Parent: Read, Mentor/Ops: Read/Write, Admin: All |
| University / Mentorship Step | Student/Parent: Read, Mentor/Ops/Admin: Read/Write |
| Payment Record / Referral Credit / Payout Request | Student: Read (If Owner), Ops/Admin: Read/Write, Mentor: Read |
| Sirjna Settings | Admin only |

---

## D) Layout & View Guidelines
- Title Field set for every master.
- Logical Sections: Personal Info, Academics, Program Details, Flags.
- List View: include columns Student, Status, Completed On.
- Dashboard Links: Student Profile → Student Progress, Shortlist, Payment Record.

---

## E) Sanity Checks
1. Create sample Student Profile with Test Scores.
2. Add Mentorship Steps per phase.
3. Create Student Progress (Pending → Done).
4. Create University with Program Deadlines.
5. Create Shortlist and Shortlist Entries.
6. Add a Payment Record (Paid).
7. Add Referral Link and Credit.
8. Verify Sirjna Settings toggle enable_referrals ✅.

---

✅ Status: Sirjna DocType structure and permissions fully configured.
Ready for Step 3 — Portal, Payment automation, and referral logic.
