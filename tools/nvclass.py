"""Sort the Nevada catalog into license classes and package types.

build.py imports this and works everything out from each product's title and Shopify product type, so the
catalog can come from the dashboard sync or from tools/sync_shopify.py without any special fields.

Nevada contractor titles carry the NSCB classification code, such as (B-2), (C-15A) or (A-10). Each code in
CODES becomes one license page. Products without a code (electrician cards, plumbers, the Business and Law
exam, licensing help, national exams) are matched by the rows in SPECIAL first.

To add a license: put a row in CODES (or SPECIAL for one without a code). Run python3 build.py and check the
"unclassified" line it prints; anything listed there lands under "Other exam prep".
"""
import re

STATE = "Nevada"

GROUPS = [
    ("building", "Class B general building contractors", "NSCB Class B licenses for building work: B General Building, B-2 Residential and Small Commercial, B-6 Commercial Remodeling and B-7 Residential Remodeling, plus the NASCLA exam Nevada accepts in place of the B trade exam."),
    ("electricians", "Electrician ID cards", "Las Vegas, Clark County and Reno require an Electrical Qualifications ID card on every job site. The cards come from Electrical Safety Professionals after an ICC national exam: journeyman, master, residential and low voltage."),
    ("electrical", "C-2 electrical contractors", "NSCB electrical contractor licenses: C-2 Electrical, C-2D Low Voltage, C-2E Lines to Transmit Electricity, C-2F Residential Wiring and C-2G Photovoltaics."),
    ("mechanical", "Plumbing, heating and air (C-1, C-21)", "NSCB mechanical licenses: the C-1 plumbing and heating family, the C-21 refrigeration and air conditioning family, C-13 sheet metal and C-38 gas equipment."),
    ("finish", "Carpentry, drywall, paint and plaster", "Interior and finish trades: C-3 carpentry, C-4 painting and decorating, C-17 lathing and plastering, the drywall and sheet metal stud subclassifications, and C-20 tiling."),
    ("structure", "Concrete, masonry, roofing and steel", "Structural and envelope trades: C-5 concrete, C-14 steel, C-15 roofing and siding and C-18 masonry."),
    ("specialty", "Solar, signs and other specialty", "Other C specialty licenses: the C-37 solar family, C-6B signs, C-7 elevators, C-10 landscaping, C-23 well drilling, C-41C fire detection and C-42."),
    ("engineering", "Class A general engineering contractors", "NSCB Class A licenses for engineering work: A General Engineering and its subclassifications for pools and spas, grading and paving, pipelines, power lines, industrial piping and asbestos."),
    ("business", "Business and Law (CMS) and licensing help", "Every Nevada contractor license needs the open-book Business and Law exam, also called the CMS. This group has the CMS books and courses, plus help with the NSCB application and the LLC or corporation."),
    ("plumbing", "Journeyman plumber cards", "Journeyman plumber cards are issued locally in Nevada, not by the Contractors Board. These packages cover the plumbing code exams."),
    ("codes", "Code books, courses and national exams", "Code courses, OSHA and NEC review, the NASCLA electrical exams and the Clark County structural welding special inspector exam."),
]

# (code, license name, group); the order here is the order on the home page inside each group
CODES = [
    ("B", "General Building Contractor", "building"),
    ("B-2", "Residential and Small Commercial Contractor", "building"),
    ("B-6", "Commercial Remodeling Contractor", "building"),
    ("B-7", "Residential Remodeling Contractor", "building"),
    ("C-2", "Electrical Contractor", "electrical"),
    ("C-2D", "Low Voltage Contractor", "electrical"),
    ("C-2F", "Residential Wiring Contractor", "electrical"),
    ("C-2G", "Photovoltaics Contractor", "electrical"),
    ("C-2E", "Lines to Transmit Electricity Contractor", "electrical"),
    ("C-1", "Plumbing and Heating Contractor", "mechanical"),
    ("C-1D", "Plumbing Contractor", "mechanical"),
    ("C-1F", "Heating, Cooling and Circulating Air Contractor", "mechanical"),
    ("C-1G", "Pipes and Vents for Gas Contractor", "mechanical"),
    ("C-1H", "Water Heater Contractor", "mechanical"),
    ("C-1C", "Pipe and Duct Insulation Contractor", "mechanical"),
    ("C-1E", "Sheet Metal Contractor (C-1E)", "mechanical"),
    ("C-1I", "Chilled-Water Piping Contractor", "mechanical"),
    ("C-1J", "Breathing Air Systems for Firefighters Contractor", "mechanical"),
    ("C-1K", "Industrial Piping Contractor (C-1K)", "mechanical"),
    ("C-21", "Refrigeration and Air Conditioning Contractor", "mechanical"),
    ("C-21A", "Refrigeration Contractor", "mechanical"),
    ("C-21B", "Air Conditioning Contractor", "mechanical"),
    ("C-21C", "Sheet Metal Contractor (C-21C)", "mechanical"),
    ("C-21D", "Refrigeration and Air Conditioning Contractor (C-21D)", "mechanical"),
    ("C-21E", "Solar Air Conditioning Contractor (C-21E)", "mechanical"),
    ("C-21F", "Chilled and Hot Water Systems Contractor", "mechanical"),
    ("C-21G", "Industrial Piping Contractor (C-21G)", "mechanical"),
    ("C-13", "Sheet Metal Contractor", "mechanical"),
    ("C-38", "Gas Equipment Contractor", "mechanical"),
    ("C-3", "Carpentry, Maintenance and Minor Repairs Contractor", "finish"),
    ("C-3A", "Carpentry and Repairs Contractor", "finish"),
    ("C-3B", "Finish Carpentry Contractor", "finish"),
    ("C-3E", "Drywall Contractor (C-3E)", "finish"),
    ("C-4", "Painting and Decorating Contractor", "finish"),
    ("C-4A", "Painting Contractor", "finish"),
    ("C-4E", "Drywall Contractor (C-4E)", "finish"),
    ("C-4F", "Sheet Metal Studs Contractor", "finish"),
    ("C-17", "Lathing and Plastering Contractor", "finish"),
    ("C-17C", "Drywall Contractor", "finish"),
    ("C-17F", "Studs of Sheet Metal Contractor", "finish"),
    ("C-20", "Tiling Contractor", "finish"),
    ("C-5", "Concrete Contractor", "structure"),
    ("C-15", "Roofing and Siding Contractor", "structure"),
    ("C-15A", "Roofing Contractor", "structure"),
    ("C-18", "Masonry Contractor", "structure"),
    ("C-14", "Steel Reinforcing and Erection Contractor", "structure"),
    ("C-14A", "Reinforcing Steel Contractor", "structure"),
    ("C-37", "Solar Contractor", "specialty"),
    ("C-37A", "Solar Water Heating Contractor", "specialty"),
    ("C-37B", "Solar Space Heating Contractor", "specialty"),
    ("C-37C", "Solar Air Conditioning Contractor", "specialty"),
    ("C-37D", "Solar Pool Heating Contractor", "specialty"),
    ("C-6B", "Sign Contractor", "specialty"),
    ("C-7", "Elevation and Conveyance Contractor", "specialty"),
    ("C-10", "Landscape Contractor", "specialty"),
    ("C-23", "Drilling Wells Contractor", "specialty"),
    ("C-41C", "Fire Detection Contractor", "specialty"),
    ("C-42", "Constructing, Altering or Improving Contractor", "specialty"),
    ("A", "General Engineering Contractor", "engineering"),
    ("A-10", "Commercial and Residential Pools Contractor", "engineering"),
    ("A-10A", "Residential Pools Contractor", "engineering"),
    ("A-10B", "Residential Spas Contractor", "engineering"),
    ("A-10C", "Repair of Pools and Spas Contractor", "engineering"),
    ("A-10E", "Pool Alteration and Repair Contractor", "engineering"),
    ("A-7", "Excavating and Grading Contractor", "engineering"),
    ("A-12", "Excavating, Grading, Trenching and Surfacing Contractor", "engineering"),
    ("A-16", "Paving of Streets, Driveways and Parking Lots Contractor", "engineering"),
    ("A-15", "Sewers, Drains and Pipes Contractor", "engineering"),
    ("A-19", "Pipelines and Conduits Contractor", "engineering"),
    ("A-19A", "Pipelines and Conduits for Water Contractor", "engineering"),
    ("A-19B", "Pipelines and Conduits for Gas Contractor", "engineering"),
    ("A-17", "Lines to Transmit Electricity Contractor (A-17)", "engineering"),
    ("A-20", "Industrial Piping Contractor (A-20)", "engineering"),
    ("A-23", "Asbestos Contractor", "engineering"),
]

def slugify(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def _code_rx(code):
    """(C-15A), (C15A), (C4-F) and 'Nevada C-15A ...' all match C-15A; (C-15) does not match C-15A."""
    m = re.match(r"([ABC])(?:-(\d+)([A-K]?))?$", code)
    L, num, suf = m.group(1), m.group(2), m.group(3)
    if not num: return r"\(%s\)|\bNevada %s - General" % (L, L)
    body = r"%s-?%s-?%s" % (L, num, suf) if suf else r"%s-?%s" % (L, num)
    return r"\(\s*%s\s*\)|\bNevada %s-%s%s\b" % (body, L, num, suf)

def _name(code, name):
    n = name if "(" in name else "%s (%s)" % (name, code)
    return n

def _slug(code, name):
    base = re.sub(r"\s*\(.*?\)", "", name).replace(" Contractor", "")
    return slugify("%s %s" % (code, base))

# licenses without an NSCB code, matched before the code rows: (slug, display name, group, regex on the title)
SPECIAL = [
    ("licensing-services", "NSCB License Application and Business Setup Services", "business", r"Application (Processing|Service)|LLC Filing|Corporation or LLC"),
    ("business-and-law-cms", "Business and Law Exam (CMS)", "business", r"Contractor Management Survey|Business and Law Manual"),
    ("nascla-commercial-general-building", "NASCLA Commercial General Building Contractor", "building", r"NASCLA (Commercial General Building|Examination for Commercial)"),
    ("nascla-business-law", "NASCLA Business, Law and Project Management", "codes", r"NASCLA Contractors Guide"),
    ("nascla-electrical", "NASCLA Electrical Exams", "codes", r"NASCLA (Master Unlimited Electrical|Residential Electrical|Journeyman Electrician)"),
    ("code-books-and-courses", "Code Books, Courses and Practice Tests", "codes", r"International (Building|Plumbing) Code|OSHA|National Electrical Code Webinar|Ray Holder"),
    ("clark-county-structural-welding", "Clark County Structural Welding Special Inspector (S2CY)", "codes", r"Structural Welding"),
    ("low-voltage-electrician", "Low Voltage Electrician (ICC G21)", "electricians", r"Low Voltage Electrician"),
    ("residential-electrician", "Residential Electrician (ICC G18)", "electricians", r"Residential Electrician"),
    ("master-electrician", "Master Electrician (ICC G16)", "electricians", r"Master Electrician"),
    ("journeyman-electrician", "Journeyman Electrician (ICC G17)", "electricians", r"Journeyman'?s? Electrician"),
    ("journeyman-plumber", "Journeyman Plumber", "plumbing", r"Journeyman Plumber"),
]

CODE_OF = {}
CLASSES = list(SPECIAL)
for code, name, grp in CODES:
    s = _slug(code, name)
    CODE_OF[s] = code
    CLASSES.append((s, _name(code, name), grp, _code_rx(code)))
OTHER = ("other", "Other Exam Prep", "codes")

# package types, lowest rank first: (slug, name, test(title, productType)). The first match wins.
def _t(rx): return lambda t, ty: re.search(rx, t, re.I) is not None
TYPES = [
    ("online-practice-exams", "Online Practice Questions", lambda t, ty: ty == "Practice Course" or (ty == "Online Course" and re.search(r"Practice (Questions|Exam|Tests)|Code Review|Course Review", t, re.I) is not None)),
    ("online-course", "Online Exam Prep Course", lambda t, ty: ty == "Online Course"),
    ("flash-cards", "Flash Cards", lambda t, ty: re.search(r"Study Flash Cards$", t) is not None),
    ("study-guide-online-course", "Study Guide and Online Course", _t(r"Study Guide & Online Course")),
    ("study-guide-flash-cards", "Study Guide and Flash Cards", _t(r"Flash Card Combo")),
    ("study-guide", "Study Guide", lambda t, ty: ty in ("Book", "Plumber Package") and re.search(r"Study Guide", t, re.I) is not None and not re.search(r"Books, Tabs", t, re.I)),
    ("code-book", "Code Book", lambda t, ty: ty == "Book"),
    ("book-package", "Book Package", lambda t, ty: ty == "Book Package"),
    ("exam-room-books", "Books Allowed in the Exam", lambda t, ty: ty == "Books in Exam"),
    ("highlighted-tabbed", "Highlighted and Tabbed Books", lambda t, ty: ty == "Book Package H/T"),
    ("exam-room-books-highlighted", "Highlighted and Tabbed Exam-Room Books", lambda t, ty: ty == "Books in Exam H&T"),
    ("study-guide-nec-tabs", "Study Guide + NEC with Tabs", _t(r"National Electrical Code Combo with Tabs")),
    ("study-guide-calculations-nec", "Study Guide + Calculations + NEC", _t(r"Calculations Study Guides & National Electrical Code Combo")),
    ("super-combo", "Super Combo", _t(r"Calculations Study Guides \+ Flash Cards")),
    ("jump-start-package", "Jump Start Package", _t(r"Jump Start")),
    ("complete-package", "Complete Package", _t(r"Complete (Journeyman|Master) Electrician|Books, Tabs & Course|Complete Master Electrician Book")),
    ("ultimate-combo", "Ultimate Combo", _t(r"Ultimate Combo")),
    ("nec-course-package", "Study Package with NEC Course", _t(r"Instructor Led NEC Course")),
    ("live-training", "Live Virtual Training", lambda t, ty: ty == "Live Training"),
    ("rental-package", "Books and Courses Rental", lambda t, ty: ty == "Book Rental"),
    # one C-17F rental carries the "Ultimate Package - Exam Only" type in Shopify, so the title decides too
    ("exam-room-rental", "Exam-Room Books and Course Rental", lambda t, ty: ty == "Book Rental - Exam Room Only" or re.search(r"Books & Course Rental - Exam Room Approved", t) is not None),
    ("ultimate-rental", "Ultimate Rental Package", lambda t, ty: ty == "Ultimate Package"),
    ("ultimate-exam-room", "Ultimate Exam-Room Books, Course and Application", lambda t, ty: ty == "Ultimate Package - Exam Only"),
    ("complete-pass-package", "Complete Pass Package", _t(r"Complete Pass Package")),
    ("llc-formation", "LLC or Corporation Setup", _t(r"LLC Filing")),
    ("application-business-package", "Application and Business Formation Package", _t(r"Application Processing & Business Formation")),
    ("licensing-service", "Licensing Service", lambda t, ty: ty in ("Application", "Business Complete Package")),
    ("the-1-package", "The 1 Package (all-inclusive)", lambda t, ty: ty == "1 Package"),
    ("exam-prep-package", "Exam Prep Package", _t(r"Exam Prep Package")),
    ("electrician-package", "Electrician Package", _t(r"(Journeyman|Master) Electrician Package$")),
]
TYPE_RANK = {s: i for i, (s, _, _) in enumerate(TYPES)}

def region(title):
    return "Nevada" if re.search(r"\bNevada\b", title) else "Nationwide"

def classify(title, ptype):
    cls = next((c for c in CLASSES if re.search(c[3], title, re.I)), None) or OTHER
    typ = next(((s, n) for s, n, f in TYPES if f(title, ptype or "")), ("other", ptype or "Exam Prep"))
    m = re.search(r"\b(20\d\d)\b", title)
    return {"cls": cls[0], "clsName": cls[1], "group": cls[2], "type": typ[0], "typeName": typ[1], "rank": TYPE_RANK.get(typ[0], 99),
            "region": region(title), "year": m.group(1) if m else "", "code": CODE_OF.get(cls[0], "")}

def clean_title(t):
    t = re.sub(r"\s*[\(\[]Based on (the )?\d{4} [A-Za-z ]+?[\)\]]\s*", " ", t)
    t = re.sub(r":\s*Trusted by 50k Electricians", "", t)
    t = re.sub(r"\bNevada Nevada\b", "Nevada", t)
    t = re.sub(r"\bContractor Contractor\b", "Contractor", t)
    return re.sub(r"\s+", " ", t).strip()

def assign(products):
    """Give every product its class, package type and a short URL slug that is unique inside its class."""
    used = {}
    out = []
    for p in sorted(products, key=lambda p: (p["title"], p["id"])):
        c = classify(p["title"], p.get("type", ""))
        base = c["type"] if c["type"] != "other" else slugify(clean_title(p["title"]))[:50].rstrip("-")
        extra = [c["year"]] if c["year"] else []
        icc = re.search(r"ICC - ([A-Z]\d{2}(?:-N)?)", p["title"])
        if icc and c["group"] == "electricians": extra.append(slugify(icc.group(1)))
        if c["region"] == "Nationwide" and c["group"] in ("electricians", "plumbing", "building"): extra.append("any-state")
        sl = "-".join([base] + extra)
        key = (c["cls"], sl); n = used.get(key, 0) + 1; used[key] = n
        if n > 1: sl = "%s-%d" % (sl, n)
        out.append(dict(p, **c, slug=sl, path="%s/%s/" % (c["cls"], sl), short=clean_title(p["title"])))
    return out

# order the licenses are listed in on the home page and in menus (the matching order above is for titles only)
DISPLAY_ORDER = (["journeyman-electrician", "master-electrician", "residential-electrician", "low-voltage-electrician", "business-and-law-cms", "licensing-services", "journeyman-plumber"]
                 + [_slug(c, n) for c, n, _ in CODES] + ["nascla-commercial-general-building"])
