import frappe

PHASES = ["Sankalp", "Udaan", "Nirman", "Pragati"]

@frappe.whitelist()
def recompute_progress_pct(doc=None, method=None, student: str | None = None):
    try:
        student_name = student or (getattr(doc, "student", None) if doc else None)
        if not student_name:
            return
        sp = frappe.get_doc("Student Profile", student_name)
        phase = sp.status_phase or "Sankalp"
        steps = frappe.get_all("Mentorship Step", filters={"phase": phase}, pluck="name")
        total = len(steps)
        if not total:
            sp.db_set("progress_pct", 0)
            return
        done = frappe.db.count("Student Progress", {"student": sp.name, "status": "Done", "step": ("in", steps)})
        pct = round((done / total) * 100, 1)
        sp.db_set("progress_pct", pct)
        if pct >= 100:
            advance_phase(sp.name)
    except Exception:
        pass

@frappe.whitelist()
def advance_phase(student: str):
    try:
        sp = frappe.get_doc("Student Profile", student)
        if (sp.status_phase or "") not in PHASES:
            sp.db_set("status_phase", "Sankalp"); return
        idx = PHASES.index(sp.status_phase)
        if idx + 1 >= len(PHASES):
            return
        nxt = PHASES[idx+1]
        sp.db_set("status_phase", nxt)
        sp.db_set("progress_pct", 0)
        _seed_progress_for_phase(sp.name, nxt)
        if sp.email:
            frappe.sendmail(recipients=[sp.email],
                            subject=f"Sirjna: Welcome to {nxt}",
                            message=f"Hi {sp.full_name}, new steps are unlocked in your portal.")
    except Exception:
        pass

def _seed_progress_for_phase(student: str, phase: str):
    try:
        step_names = frappe.get_all("Mentorship Step", filters={"phase": phase}, pluck="name")
        for s in step_names:
            if not frappe.db.exists("Student Progress", {"student": student, "step": s}):
                doc = frappe.new_doc("Student Progress")
                doc.student = student
                doc.step = s
                doc.status = "Pending"
                doc.insert(ignore_permissions=True)
    except Exception:
        pass
