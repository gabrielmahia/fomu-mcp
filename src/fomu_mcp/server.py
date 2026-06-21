"""FomuMCP — Kenya Civic Form Agent (6 tools). DEMO data.

Source: Engineer's Schematic — Form Agent type:
'Turns messy user answers into applications, checklists, letters.'

Fomu (Swahili for 'form') handles Kenya's most common citizen-facing documents.
"""
from __future__ import annotations
from typing import Optional
from fastmcp import FastMCP
from pydantic import Field
mcp = FastMCP(name="fomu-mcp", instructions="Kenya civic form agent — generates checklists, guidance, and draft applications for common government processes. DEMO.")

# ── Form Definitions ──────────────────────────────────────────────────────────
FORMS = {
    "business_registration": {
        "name": "Business Name/Company Registration",
        "authority": "Business Registration Service (BRS) via eCitizen",
        "portal": "ecitizen.go.ke",
        "cost_kes": {"sole_proprietorship": 950, "partnership": 1000, "limited_company": 10650},
        "processing_days": 3,
        "fields": ["Proposed business name (3 alternatives)", "Business type", "Business address",
                   "Director/owner names and IDs", "Nature of business", "KRA PIN (each director)"],
        "documents": ["National ID or Passport (all directors)", "KRA PIN certificate",
                      "Passport photos (2 each)", "Proof of business address",
                      "Memorandum & Articles of Association (limited company only)"],
        "steps": ["Search name availability on eCitizen", "Fill online form", "Pay via M-PESA/card",
                  "Await SMS confirmation (1-3 days)", "Download Certificate from eCitizen"],
    },
    "business_permit": {
        "name": "Single Business Permit",
        "authority": "County Government",
        "portal": "County eCitizen portal or county offices",
        "cost_kes": {"kiosk": 2000, "retail_shop": 5000, "medium_business": 15000, "large_business": 30000},
        "processing_days": 7,
        "fields": ["Business name and registration number", "Business location (county, ward)",
                   "Type of business activity", "Annual turnover estimate",
                   "Number of employees", "Premises ownership (own/rent)"],
        "documents": ["Business registration certificate", "KRA PIN certificate",
                      "National ID", "Lease agreement (if renting)",
                      "Previous year permit (renewal)", "Fire safety certificate (food businesses)"],
        "steps": ["Apply at county offices or county eCitizen portal", "Pay county permit fees",
                  "Await inspection (food/health businesses)", "Collect permit"],
    },
    "kra_pin": {
        "name": "KRA Personal Identification Number (PIN)",
        "authority": "Kenya Revenue Authority",
        "portal": "itax.kra.go.ke",
        "cost_kes": 0,
        "processing_days": 1,
        "fields": ["Full legal name (as on ID)", "Date of birth", "ID/Passport number",
                   "Physical address", "Email address", "Phone number",
                   "Tax obligation type (employee, business, rental, etc.)"],
        "documents": ["National ID or Passport", "Birth certificate (if different from ID name)"],
        "steps": ["Visit itax.kra.go.ke", "Click 'New PIN Registration'",
                  "Fill individual taxpayer details", "Upload ID scan",
                  "Submit — PIN generated immediately", "Download PIN certificate"],
    },
    "nhif_registration": {
        "name": "NHIF/SHA Registration",
        "authority": "Social Health Authority (SHA)",
        "portal": "sha.go.ke or NHIF offices",
        "cost_kes": {"employed": 500, "self_employed": 500, "voluntary": 500},
        "processing_days": 7,
        "fields": ["Full name", "ID number", "Phone number", "Employer name (if employed)",
                   "Dependants (spouse, children under 21)", "Bank account (optional)"],
        "documents": ["National ID", "Passport photo", "Payslip (if employed)",
                      "Marriage certificate (for spouse)", "Birth certificates (for children)"],
        "steps": ["Visit sha.go.ke or nearest NHIF office", "Fill SHA Form 1",
                  "Submit with documents", "Receive SHA number by SMS (7 days)",
                  "Set up monthly contribution (M-PESA Paybill 200222)"],
    },
    "land_title_search": {
        "name": "Land Title Search",
        "authority": "Ministry of Lands — eCitizen",
        "portal": "ecitizen.go.ke/lands",
        "cost_kes": 500,
        "processing_days": 3,
        "fields": ["Title number (LR or IR number)", "County", "Applicant name and ID"],
        "documents": ["National ID of applicant"],
        "steps": ["Log into eCitizen", "Select 'Lands — Search'", "Enter title number",
                  "Pay KES 500 via M-PESA", "Download search certificate (3 days)"],
        "note": "Also verify for: charges, caveats, restrictions, ownership history",
    },
    "police_clearance": {
        "name": "Certificate of Good Conduct",
        "authority": "Directorate of Criminal Investigations (DCI)",
        "portal": "ecitizen.go.ke → DCI Services",
        "cost_kes": 1050,
        "processing_days": 30,
        "fields": ["Full name", "ID/Passport number", "Date of birth", "Purpose of certificate"],
        "documents": ["National ID or Passport", "Fingerprinting at DCI offices or Huduma Centres"],
        "steps": ["Apply on eCitizen → DCI → Certificate of Good Conduct",
                  "Pay KES 1,050", "Book fingerprinting appointment",
                  "Attend fingerprinting at DCI/Huduma Centre",
                  "Certificate ready in 30 days — download from eCitizen"],
    },
}

@mcp.tool(name="form_checklist", description="Generate a checklist for a Kenya government form or application. DEMO.")
def form_checklist(form_type: str = Field(..., description="Government form or process e.g. 'business_registration', 'kra_pin', 'nhif_registration', 'land_title_search', 'police_clearance', 'passport'"), applicant_type: Optional[str] = Field("individual", description="Applicant category: 'individual', 'company', 'ngo'. Affects required documents.")) -> dict:
    f = form_type.lower().replace(" ", "_").replace("-", "_")
    form = FORMS.get(f)
    if not form:
        available = list(FORMS.keys())
        return {"source": "DEMO", "error": f"Form type '{form_type}' not in database",
                "available_forms": available, "tip": "Try: business_registration, business_permit, kra_pin, nhif_registration, land_title_search, police_clearance"}
    cost = form.get("cost_kes", {})
    if isinstance(cost, dict):
        cost_display = {k: f"KES {v:,}" for k, v in cost.items()}
    else:
        cost_display = f"KES {cost:,}"
    return {"source": f"DEMO — {form['authority']}", "form": form_type,
            "applicant_type": applicant_type, "authority": form["authority"],
            "portal": form["portal"], "cost": cost_display,
            "processing_days": form["processing_days"],
            "required_fields": form["fields"], "required_documents": form["documents"],
            "steps": form["steps"], "note": form.get("note", ""),
            "disclaimer": "Requirements may change. Verify at the official portal before applying."}

@mcp.tool(name="form_draft_letter", description="Generate a draft formal letter for common Kenya civic requests. DEMO.")
def form_draft_letter(letter_type: str = Field(..., description="Letter category e.g. 'introduction', 'complaint', 'appeal', 'request_extension'"), applicant_name: str = Field(..., description="Full name of the applicant for the letter salutation and signature"), details: Optional[str] = Field(None, description="Additional context to personalise the letter e.g. reference number, specific department, date of original application")) -> dict:
    TEMPLATES = {
        "introduction_letter": {
            "title": "Letter of Introduction",
            "body": f"""To Whom It May Concern,

I, {applicant_name}, hereby introduce myself as a bona fide resident/citizen seeking assistance with [PURPOSE].

I hold National ID Number: _______________

I kindly request your office to assist me with this matter.

Yours faithfully,
{applicant_name}
Date: _______________
Contact: _______________""",
            "use_cases": "Bank account opening, school applications, welfare assistance, community verification",
        },
        "reference_letter": {
            "title": "Reference/Recommendation Letter",
            "body": f"""To Whom It May Concern,

I am writing to recommend {applicant_name if applicant_name else '[PERSON NAME]'} for [POSITION/PURPOSE].

I have known [him/her/them] for [DURATION] in my capacity as [YOUR TITLE] at [ORGANIZATION].

During this time, I have observed [him/her/them] to be [POSITIVE QUALITIES].

I recommend [him/her/them] without reservation.

[Your Name]
[Title]
[Organization]
[Contact]
Date: _______________""",
            "use_cases": "Employment, school admission, loan applications, visa applications",
        },
        "complaint_letter": {
            "title": "Formal Complaint Letter",
            "body": f"""[Authority Name]
[Address]

Dear Sir/Madam,

Re: Formal Complaint — [SUBJECT]

I, {applicant_name}, wish to formally bring to your attention the following matter:

[DESCRIPTION OF THE PROBLEM]

This has caused me [IMPACT/HARM].

I have attempted to resolve this through [PREVIOUS ATTEMPTS] without success.

I respectfully request that your office:
1. [ACTION REQUESTED 1]
2. [ACTION REQUESTED 2]

I am available for further information at [CONTACT].

Yours faithfully,
{applicant_name}
ID: _______________
Date: _______________""",
            "use_cases": "KPLC complaint, KRA dispute, county services complaint, NHIF complaint",
        },
        "land_inquiry": {
            "title": "Land Inquiry Letter",
            "body": f"""The Land Registrar
[County] Land Registry

Dear Sir/Madam,

Re: Land Inquiry — [LR/IR Number]

I, {applicant_name}, holding National ID _______________, write to inquire about the parcel of land described as:

Title/IR Number: _______________
Location: _______________

I wish to confirm: ownership, any charges or caveats, and the current status of this parcel.

Please provide a formal search certificate.

Yours faithfully,
{applicant_name}
Date: _______________""",
            "use_cases": "Land purchase due diligence, inheritance claims, boundary disputes",
        },
    }
    l = letter_type.lower().replace(" ", "_").replace("-", "_")
    template = TEMPLATES.get(l)
    if not template:
        return {"source": "DEMO", "error": f"Letter type '{letter_type}' not found",
                "available": list(TEMPLATES.keys())}
    body = template["body"]
    if details:
        body = body.replace("[PURPOSE]", details).replace("[SUBJECT]", details)
    return {"source": "DEMO — Kenya formal letter templates", "letter_type": letter_type,
            "title": template["title"], "draft": body, "use_cases": template["use_cases"],
            "disclaimer": "Draft only. Review with the relevant authority before submitting. DEMO."}

@mcp.tool(name="form_requirements_check", description="Check if user has all requirements for a Kenya government form. DEMO.")
def form_requirements_check(form_type: str = Field(..., description="Form type to check against e.g. 'business_registration', 'passport', 'land_title_search'"), user_has: list = Field(..., description="List of documents the applicant already has e.g. ['national_id', 'kra_pin', 'passport_photo']")) -> dict:
    f = form_type.lower().replace(" ", "_").replace("-", "_")
    form = FORMS.get(f)
    if not form:
        return {"source": "DEMO", "error": f"Form '{form_type}' not found",
                "available": list(FORMS.keys())}
    required = form["documents"] + form["fields"]
    user_has_lower = [h.lower() for h in user_has]
    missing = []
    have = []
    for req in required:
        matched = any(word in " ".join(user_has_lower) for word in req.lower().split()[:3])
        if matched:
            have.append(req)
        else:
            missing.append(req)
    ready = len(missing) == 0
    return {"source": f"DEMO — {form['authority']}", "form": form_type,
            "ready_to_apply": ready, "have": have, "missing": missing,
            "completeness_pct": round(len(have) / len(required) * 100, 0),
            "next_step": "Proceed to application" if ready else f"Obtain missing items: {missing[:2]}",
            "portal": form["portal"]}

@mcp.tool(name="ecitizen_guide", description="Guide to Kenya eCitizen portal services. DEMO.")
def ecitizen_guide(service_category: Optional[str] = Field(None, description="eCitizen service category e.g. 'ntsa', 'immigration', 'kra', 'nhif', 'nssf'. Leave empty for full service catalogue.")) -> dict:
    """Return step-by-step guide for completing Kenya government services on eCitizen portal."""
    SERVICES = {
        "business": ["Business name registration (BRS)", "Single Business Permit", "Trade licence",
                     "Tourism enterprise registration"],
        "documents": ["National ID application and replacement", "Passport application",
                      "Certificate of Good Conduct", "Birth/death/marriage certificates"],
        "lands": ["Land title search", "Land rates clearance", "Valuation rolls",
                  "Survey plan requests"],
        "immigration": ["Work permit", "Dependant pass", "Student pass", "Special pass"],
        "tax": ["KRA PIN registration", "iTax filing (links to itax.kra.go.ke)",
                "Tax compliance certificate"],
        "county": ["County-specific services vary. Check your county eCitizen portal."],
    }
    if service_category:
        s = service_category.lower()
        matched = {k: v for k, v in SERVICES.items() if k in s or s in k}
        return {"source": "DEMO — eCitizen Kenya", "category": service_category,
                "services": matched or SERVICES, "portal": "ecitizen.go.ke"}
    return {"source": "DEMO — eCitizen Kenya", "portal": "ecitizen.go.ke",
            "all_services": SERVICES, "payment": "M-PESA, debit/credit card, bank transfer",
            "helpdesk": "0800-221333 (toll-free) | support@ecitizen.go.ke"}

@mcp.tool(name="huduma_centre_guide", description="Guide to Kenya Huduma Centre services and locations. DEMO.")
def huduma_centre_guide(county: Optional[str] = Field(None, description="Kenya county name e.g. 'Nairobi', 'Mombasa', 'Kisumu'. Leave empty for all Huduma Centre locations.")) -> dict:
    """Return location, services, and operating hours for Huduma Centre offices in Kenya."""
    CENTRES = {
        "Nairobi": ["Huduma Centre GPO (Kenyatta Ave)", "Huduma Centre Teleposta (Ngong Rd)",
                    "Huduma Centre KICC", "Huduma Centre Athi River"],
        "Mombasa": ["Huduma Centre Mombasa (Treasury Square)"],
        "Kisumu": ["Huduma Centre Kisumu (Swan Centre)"],
        "Nakuru": ["Huduma Centre Nakuru (Gilgil Rd)"],
        "Eldoret": ["Huduma Centre Eldoret (Uganda Rd)"],
    }
    SERVICES_OFFERED = [
        "National ID card (application and replacement)",
        "Passport services", "Birth and death certificates",
        "KRA services", "NHIF registration", "NSSF services",
        "Certificate of Good Conduct (fingerprinting)",
        "Land title search", "Higher Education Loans Board (HELB)",
        "Business name registration", "Immigration services",
    ]
    centres = CENTRES.get(county.title() if county else "Nairobi", CENTRES)
    return {"source": "DEMO — Huduma Kenya", "county": county or "All",
            "centres": centres if county else CENTRES,
            "services": SERVICES_OFFERED,
            "opening_hours": "Monday–Friday: 8:00 AM–5:00 PM",
            "contact": "0800221333 (toll-free) | info@hudumakenya.go.ke",
            "portal": "hudumakenya.go.ke"}

@mcp.tool(name="form_timeline_planner", description="Plan timeline for Kenya government processes. DEMO.")
def form_timeline_planner(processes: list = Field(..., description="List of government processes to schedule e.g. ['business_registration', 'kra_pin', 'nhif_registration']"), start_date: Optional[str] = Field(None, description="ISO date to start planning from e.g. '2025-01-15'. Defaults to today if omitted.")) -> dict:
    import datetime
    start = start_date or datetime.date.today().isoformat()
    try:
        start_dt = datetime.date.fromisoformat(start)
    except:
        start_dt = datetime.date.today()
    plan = []
    current = start_dt
    total_days = 0
    for process in processes:
        p = process.lower().replace(" ", "_").replace("-", "_")
        form = FORMS.get(p)
        days = form["processing_days"] if form else 7
        name = form["name"] if form else process
        prep_days = 3
        plan.append({
            "process": name, "prep_start": current.isoformat(),
            "apply_by": (current + datetime.timedelta(days=prep_days)).isoformat(),
            "expected_completion": (current + datetime.timedelta(days=prep_days + days)).isoformat(),
            "total_days": prep_days + days,
        })
        current = current + datetime.timedelta(days=prep_days + days + 2)
        total_days += prep_days + days + 2
    end = (start_dt + datetime.timedelta(days=total_days)).isoformat()
    return {"source": "DEMO — Kenya government processing times", "start_date": start,
            "estimated_completion": end, "total_calendar_days": total_days,
            "plan": plan, "tip": "Apply for processes in parallel where possible to save time.",
            "disclaimer": "Processing times are estimates. Actual times vary by office and season."}
