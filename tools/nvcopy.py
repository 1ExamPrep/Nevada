"""Copy for passyournevadacontractorexam.com: what each license covers and the facts per license group.

Edit freely, then run python3 build.py. Figures here were checked on 2026-11-10 against the Nevada State
Contractors Board (NSCB), PSI, ICC and City of Reno pages listed in SOURCES. Re-check them when the boards change
their rules. Things to watch:
  - The CMS (Business and Law) figures come from the PSI Nevada bulletin updated 3/25/2026.
  - The B-7 Restricted License (SB 130) opened for applications in March 2026; its rules are new.
  - Electrician ID cards: ICC national exams come in more than one NEC edition. CURRENT_NEC below decides which
    package years get the "older code" note.
  - The NASCLA line (accepted in place of the B trade exam) comes from the NSCB equivalency rules as reported
    by NASCLA; confirm on the NSCB State Equivalency Chart if the Board changes it.
"""
import nvclass

STATE = "Nevada"

NSCB = "https://www.nvcontractorsboard.com/"
NSCB_EXAMS = "https://www.nvcontractorsboard.com/licensing/license-examinations/"
NSCB_BONDS = "https://nvcontractorsboard.com/bonds"
NSCB_APP = "https://www.nvcontractorsboard.com/wp-content/uploads/2026/08/New-License-Application.pdf"
NSCB_B7 = "https://www.nvcontractorsboard.com/wp-content/uploads/2026/03/03-17-2026-Restricted-License-Industry-Bulletin_2026.pdf"
NSCB_B7_CLASS = "https://www.nvcontractorsboard.com/wp-content/uploads/2023/03/01-26-23-B-7-Residential-Remodeling-Classification.pdf"
PSI_NV = "https://test-takers.psiexams.com/nvcon"
PSI_CMS = "https://test-takers.psiexams.com/api/content/bulletin/304"
ICC_NV = "https://support.iccsafe.org/?p=1415"
ICC_EXAMS = "https://www.iccsafe.org/professional-development/certification/"
RENO_CARDS = "https://reno.gov/business-development/development-services/electrical-plumbing-journeyman-cards.php"
NASCLA = "https://www.nascla.org/page/AccreditedExam"

MAIN_SOURCES = [("Nevada State Contractors Board: license examinations", NSCB_EXAMS), ("PSI: Nevada contractor exams", PSI_NV), ("ICC: Nevada electrician exam and ID card program", ICC_NV)]

_CONTRACTOR_SOURCES = [("NSCB: license examinations", NSCB_EXAMS), ("PSI: Nevada contractor management (CMS) bulletin", PSI_CMS), ("NSCB: license bonds", NSCB_BONDS), ("NSCB: new license application", NSCB_APP)]
SOURCES = {g: list(_CONTRACTOR_SOURCES) for g in ("electrical", "mechanical", "finish", "structure", "specialty", "engineering")}
SOURCES.update({
    "building": _CONTRACTOR_SOURCES + [("NSCB: B-7 Restricted License bulletin, March 17, 2026", NSCB_B7), ("NASCLA accredited examinations", NASCLA)],
    "electricians": [("ICC: Nevada exam and ID card program", ICC_NV), ("City of Reno: electrical and plumbing journeyman cards", RENO_CARDS), ("ICC certification exams", ICC_EXAMS)],
    "business": [("NSCB: license examinations", NSCB_EXAMS), ("PSI: Nevada contractor management (CMS) bulletin", PSI_CMS), ("NSCB: new license application", NSCB_APP)],
    "plumbing": [("City of Reno: electrical and plumbing journeyman cards", RENO_CARDS), ("NSCB: license examinations", NSCB_EXAMS)],
    "codes": [("ICC certification exams", ICC_EXAMS), ("NASCLA accredited examinations", NASCLA), ("ICC: Nevada exam and ID card program", ICC_NV)],
})

_LETTER = {"A": "Class A general engineering", "B": "Class B general building", "C": "Class C specialty"}
_KIND = {"electrical": "electrical work", "mechanical": "plumbing, heating, air conditioning or gas work", "finish": "interior and finish work",
         "structure": "structural and roofing work", "specialty": "specialty work", "engineering": "engineering work", "building": "building work"}

def _generic_scope(code, name, grp):
    sub = "classification" if "-" not in code else "subclassification"
    return ("The Nevada %s license is an NSCB %s %s for %s. It takes four years of experience, the Business and Law (CMS) exam, "
            "the %s trade exam, a bond and a monetary limit." % (name, _LETTER[code[0]], sub, _KIND[grp], code))

SCOPE = {}
for _c, _n, _g in nvclass.CODES:
    SCOPE[nvclass._slug(_c, _n)] = _generic_scope(_c, nvclass._name(_c, _n).replace(" (%s)" % _c, "") + " (%s)" % _c, _g)
SCOPE.update({
    "b-general-building": "The Nevada B General Building license covers building work of any size, residential or commercial. It takes four years of experience, the Business and Law (CMS) exam, the B trade exam, a bond and a monetary limit.",
    "b-2-residential-and-small-commercial": "The Nevada B-2 Residential and Small Commercial license covers homes and smaller commercial buildings, the license most home builders and remodelers hold. It takes the same CMS exam plus the B-2 trade exam, four years of experience in the last 15, a bond and a monetary limit.",
    "b-6-commercial-remodeling": "The Nevada B-6 Commercial Remodeling license covers remodeling and improving existing commercial buildings. Like the other B licenses it needs the CMS exam, the B-6 trade exam, four years of experience in the last 15, a bond and a monetary limit.",
    "b-7-residential-remodeling": "The Nevada B-7 Residential Remodeling license covers remodeling an existing single-family home without adding enclosed space. Since March 2026 the Board also issues a B-7 Restricted License for jobs up to $7,000 with no trade exam.",
    "c-2-electrical": "The Nevada C-2 Electrical Contractor license is the NSCB license an electrical contracting business needs to bid and pull permits. The electricians who do the work also need an Electrical Qualifications ID card in Las Vegas, Clark County and Reno.",
    "c-2d-low-voltage": "The Nevada C-2D Low Voltage license covers low voltage systems such as data, communications and security wiring. It needs the CMS exam and the C-2D trade exam, plus experience, a bond and a monetary limit.",
    "c-2g-photovoltaics": "The Nevada C-2G Photovoltaics license covers solar electric (PV) systems. It needs the CMS exam and the C-2G trade exam, plus experience, a bond and a monetary limit.",
    "licensing-services": "Licensing services handle the paperwork: the NSCB license application, where the Board checks experience and finances and sets the bond and monetary limit, and the LLC or corporation the license goes under.",
    "business-and-law-cms": "The Business and Law exam, which PSI calls the Contractor Management Survey (CMS), is required for every Nevada contractor license, A, B or C. It is open book with the Construction Business and Law Manual for Nevada.",
    "nascla-commercial-general-building": "The NASCLA Commercial General Building exam is a national contractor exam. Nevada accepts a passing score in place of the B General Building trade exam, but the Nevada Business and Law (CMS) exam is still required.",
    "nascla-business-law": "NASCLA's Contractors Guide to Business, Law and Project Management is the reference for the business exams in several NASCLA states. In Nevada the business exam is the CMS, written to the Nevada manual instead.",
    "nascla-electrical": "The NASCLA electrical exams are national exams for journeyman, residential and master unlimited electrical licenses, used by the states that accept them.",
    "code-books-and-courses": "Code courses and practice tests cover the International Building and Plumbing Codes, the National Electrical Code, older electrician question banks and OSHA construction rules.",
    "clark-county-structural-welding": "The Clark County Structural Welding special inspector module is an ICC exam (S2CY in the ICC catalog) for inspectors who check structural welding on Clark County projects.",
    "journeyman-electrician": "A Nevada journeyman electrician needs an Electrical Qualifications ID card to work in Las Vegas, Clark County or Reno. The card comes from Electrical Safety Professionals after you pass the ICC G17 Journeyman Electrician exam.",
    "master-electrician": "A Nevada master electrician card is issued by Electrical Safety Professionals after the ICC G16 Master Electrician exam. It sits above the journeyman card and is often the qualified person behind a C-2 contractor.",
    "residential-electrician": "The residential electrician card covers residential wiring in Las Vegas, Clark County and Reno. It comes from Electrical Safety Professionals after the ICC G18 Residential Electrician exam.",
    "low-voltage-electrician": "The low voltage electrician card is issued by Electrical Safety Professionals after the ICC G21 Low-Voltage Electrician exam, for electricians who work on low voltage systems.",
    "journeyman-plumber": "Nevada journeyman plumber cards are issued locally, not by the Contractors Board. In Reno the journeyman exam is open book and written to the 2024 Uniform Plumbing Code.",
    "other": "Other exam prep collects products that do not fit a single license.",
})

# license pages that sell a service, not exam prep: no "exam prep" after their name
NOT_EXAMS = ("licensing-services",)

# extra facts for one license, shown before the group facts. Keep each one a plain sentence with a number in it.
CLASS_FACTS = {
    "business-and-law-cms": ["The CMS has 60 scored questions in 120 minutes, plus 3 unscored ones, and you need 45 right (75 percent) to pass.",
                             "PSI charges $95 for one exam portion and $140 for a trade exam and the CMS together."],
    "b-7-residential-remodeling": ["The B-7 Restricted License covers jobs up to $7,000 including labor and materials, needs no trade exam and is valid for 2 years.",
                                   "A restricted license holder may not do life-safety trades such as electrical, plumbing or HVAC work."],
    "nascla-commercial-general-building": ["Nevada accepts a passing NASCLA Commercial General Building score in place of the B trade exam; the CMS is still required."],
    "journeyman-electrician": ["The ICC G17 Journeyman Electrician exam has 80 questions in 4 hours and is open book with the NEC.",
                               "The ID card is valid for 3 years and renews with continuing education from an approved provider."],
    "residential-electrician": ["In Reno, the G17 and G18 exams need no pre-approval: you book them through ICC and send the score report to ESP."],
}

# facts per group, used in the "How does the exam work" section and the FAQ
_CONTRACTOR_FACTS = [
    "Every Nevada contractor license needs the Business and Law (CMS) exam plus a trade exam for the classification, both given by PSI.",
    "The CMS is open book with the Construction Business and Law Manual for Nevada; trade exams are closed book except for the code references their outline allows.",
    "PSI charges $95 for one exam portion, or $140 for a trade exam taken with the CMS, and you get three attempts before the application is void.",
    "The Board sets a bond from $1,000 to $500,000 and a monetary limit on every license, based on your experience and financial statements.",
]
GROUP_FACTS = {g: list(_CONTRACTOR_FACTS) for g in ("electrical", "mechanical", "finish", "structure", "specialty", "engineering")}
GROUP_FACTS.update({
    "building": _CONTRACTOR_FACTS[:3] + ["Nevada accepts a passing NASCLA Commercial General Building exam in place of the B trade exam, and since March 2026 issues a B-7 Restricted License for jobs up to $7,000."],
    "electricians": [
        "Nevada has no state electrician license; Las Vegas, Clark County and Reno require an Electrical Qualifications ID card on every job site.",
        "Electrical Safety Professionals (ESP) issues the cards, after you pass an ICC national exam: G17 journeyman, G16 master, G18 residential or G21 low voltage.",
        "ICC electrician exams are open book with the NEC, and ICC offers them in more than one code edition, so match the edition to the exam you book.",
        "Cards are valid for 3 years; one expired for more than a year means taking the exam again.",
    ],
    "business": [
        "The Business and Law exam (CMS) is required for every Nevada contractor license, whatever the classification.",
        "The CMS is open book: the only reference allowed is the Construction Business and Law Manual for Nevada.",
        "The CMS has 60 scored questions in 120 minutes, and 45 right (75 percent) is a pass.",
        "The NSCB application fee is $300, and the Board sets your bond and monetary limit when it approves the license.",
    ],
    "plumbing": [
        "Nevada journeyman plumber cards are issued by local boards, not by the Contractors Board.",
        "In Reno the journeyman plumbing exam is open book and written to the 2024 Uniform Plumbing Code.",
        "Plumbing contractors also need an NSCB license, such as C-1 Plumbing and Heating or C-1D Plumbing, with the CMS exam.",
        "Packages here cover the 2024 IPC and the 2021 UPC, so check which code your local board tests before you order.",
    ],
    "codes": [
        "ICC and NASCLA exams are national exams; each candidate bulletin lists the references allowed and the code edition.",
        "Nevada electrician ID cards use ICC national exams, and the Clark County special inspector modules are ICC exams too.",
        "Nevada contractor trade exams are closed book except for the code references named in the PSI outline.",
        "Books ship from the fulfillment center; online courses arrive by email after purchase.",
    ],
})
GROUP_HOW = {g: "The {name} license comes from the Nevada State Contractors Board. You apply to the NSCB with your experience and financial statement, the Board sends an exam eligibility letter, and you book the CMS and the trade exam with PSI. Scores come right after the exam." for g in ("building", "electrical", "mechanical", "finish", "structure", "specialty", "engineering")}
GROUP_HOW.update({
    "electricians": "The {name} card is part of the Electrical Qualifications ID card program run by Electrical Safety Professionals for Las Vegas, Clark County and Reno. You pass the ICC national exam, then apply to ESP with the score report.",
    "business": "The {name} side of a Nevada license is the same for every classification: the NSCB application, the Board's review of experience and finances, and the open-book CMS at PSI.",
    "plumbing": "The {name} card is issued by a local plumbing board. The board approves you to test, then tells you how to book the open-book code exam; the card arrives after you pass.",
    "codes": "The {name} items are national exams, references and short courses that sit beside the exam prep for the Nevada licenses on this site.",
})

_CONTRACTOR_OPEN = "Partly. The Business and Law (CMS) exam is open book with the Construction Business and Law Manual for Nevada. Trade exams are closed book except for the code references named in the PSI content outline for your classification, which is why the exam-room book packages are sold as allowed in the exam."
OPEN_BOOK = {g: _CONTRACTOR_OPEN for g in ("building", "electrical", "mechanical", "finish", "structure", "specialty", "engineering")}
OPEN_BOOK.update({
    "electricians": "Yes. The ICC national electrician exams are open book with the National Electrical Code edition named for your exam, and ICC lists a few other references, such as Ugly's Electrical References, as allowed.",
    "business": "Yes. The CMS is open book, and the only reference allowed is the Construction Business and Law Manual for Nevada. Highlighted and tabbed copies save the most time.",
    "plumbing": "Yes in Reno, where the journeyman plumbing exam is open book on the 2024 Uniform Plumbing Code. Check with your local board, since cards are issued locally.",
    "codes": "ICC and NASCLA exams are open book for most categories. The bulletin for your exam lists the references allowed and the editions.",
})
WHO_ISSUES = {g: "the Nevada State Contractors Board (NSCB), with exams by PSI" for g in ("building", "electrical", "mechanical", "finish", "structure", "specialty", "engineering", "business")}
WHO_ISSUES.update({"electricians": "Electrical Safety Professionals (ESP), which runs the ID card program for Las Vegas, Clark County and Reno, after an ICC exam",
                   "plumbing": "your local plumbing board, not the Contractors Board",
                   "codes": "the city, county or state that uses the exam"})

# two extra FAQ entries per group: (question template with {name}, answer)
_CONTRACTOR_FAQ = [("What does the {name} exam cost?", "PSI charges $95 for one exam portion and $140 when the trade exam is taken with the Business and Law (CMS) exam. The NSCB application fee of $300 is separate."),
                   ("What is the monetary limit on a Nevada license?", "Every Nevada contractor license carries a monetary limit, the most you can contract for on one job. The Board sets it, along with a bond of $1,000 to $500,000, from your financial statement and experience.")]
GROUP_FAQ = {g: list(_CONTRACTOR_FAQ) for g in ("electrical", "mechanical", "finish", "structure", "specialty", "engineering")}
GROUP_FAQ.update({
    "building": [_CONTRACTOR_FAQ[0], ("Can I use the NASCLA exam for a Nevada B license?", "Yes. Nevada accepts a passing NASCLA Commercial General Building score in place of the B General Building trade exam. You still take the Nevada Business and Law (CMS) exam and meet the experience, bond and financial rules.")],
    "electricians": [("Does Nevada have a state electrician license?", "No. Nevada licenses electrical contractors through the NSCB (C-2), but individual electricians carry an Electrical Qualifications ID card required by Las Vegas, Clark County and Reno, issued by Electrical Safety Professionals after an ICC exam."),
                     ("Which NEC edition should I study?", "The one named for the ICC exam you book. ICC offers its national electrician exams in more than one edition, so check the exam title in the ICC catalog, then pick the package for that code year.")],
    "business": [("How many questions are on the Nevada Business and Law exam?", "The CMS has 60 scored questions plus 3 unscored ones, with 120 minutes for the scored part. You need 45 correct, which is 75 percent."),
                 ("How many tries do I get?", "Three. If you fail the third attempt the application becomes void, and you can apply again after 30 days.")],
    "plumbing": [("Does the Contractors Board issue journeyman plumber cards?", "No. Journeyman cards come from local plumbing boards. The NSCB licenses plumbing contractors, such as C-1 and C-1D, which also need the Business and Law exam."),
                 ("Which plumbing code is the exam on?", "In Reno it is the 2024 Uniform Plumbing Code. Packages here cover the 2024 IPC and the 2021 UPC, so match the code to the exam your board gives.")],
    "codes": [("Which code edition is the exam on?", "Each ICC and NASCLA bulletin names the edition. Check it before ordering, since jurisdictions adopt new codes on their own schedules."),
              ("Can I bring these books into the exam?", "For open-book exams, yes, if the edition is the one in your bulletin. Nevada trade exams are closed book except for the references named in the PSI outline.")],
})

# electrician packages older than this NEC year get the "older code" note
CURRENT_NEC = "2023"
OLD_CODE_NOTE = "ICC's national electrician exams come in more than one NEC edition, and packages for the 2023 and 2026 NEC are listed here, so pick the edition named for the exam you book."

# what each package type is, in one line
TYPE_BLURB = {
    "online-practice-exams": "timed practice questions online",
    "online-course": "an online course with practice exams",
    "flash-cards": "flash cards for the key numbers and rules",
    "tabs": "pre-printed tabs for the reference books",
    "study-guide-online-course": "the study guide plus the online course",
    "study-guide-flash-cards": "the study guide with practice exams plus flash cards",
    "study-guide": "the printed study guide with practice exams",
    "code-book": "the printed reference book",
    "book-package": "the reference books, new and unmarked",
    "exam-room-books": "the references PSI allows in the exam room",
    "highlighted-tabbed": "the reference books already highlighted and tabbed",
    "exam-room-books-highlighted": "exam-room references, highlighted and tabbed",
    "study-guide-nec-tabs": "the study guide, the National Electrical Code and tabs",
    "study-guide-calculations-nec": "the study guide, the calculations guide and the National Electrical Code",
    "super-combo": "study guide, calculations guide, flash cards, the NEC and tabs",
    "jump-start-package": "a starter set of books and online practice",
    "complete-package": "the books, tabs and course together",
    "electrician-package": "books and practice for an earlier code",
    "ultimate-combo": "the full study set plus the online test kit",
    "nec-course-package": "study package plus an NEC course",
    "live-training": "live virtual classes plus self-study",
    "rental-package": "rental books plus the online course",
    "exam-room-rental": "rental exam-room books plus the online course",
    "ultimate-rental": "tabbed rental books, course and live training",
    "ultimate-exam-room": "exam-room books, course and application help",
    "complete-pass-package": "everything for the Business and Law exam in one order",
    "licensing-service": "help preparing and filing the NSCB license application",
    "llc-formation": "forming the Nevada LLC or corporation the license goes under",
    "application-business-package": "the NSCB application plus business formation",
    "the-1-package": "exam prep, books, paperwork and business setup",
    "ultimate-package": "the complete exam prep package",
    "exam-prep-package": "an exam prep package",
    "other": "exam prep",
}

# home page
HOME_H1 = "Nevada contractor exam prep for every license"
HOME_LEAD = ("Exam prep for {n} Nevada licenses: NSCB general building, engineering and specialty classifications from B-2 to C-15A, "
             "the Business and Law (CMS) exam every contractor takes, and the ICC exams behind Las Vegas, Clark County and Reno electrician cards. "
             "Pick your license to compare its packages, then check out in one click.")
HOME_TITLE = "Nevada Contractor Exam Prep for Every NSCB License"
HOME_DESC = "Nevada exam prep for {n} licenses: NSCB A, B and C classifications, the Business and Law (CMS) exam and electrician ID card exams. Books, courses and The 1 Package."
HOME_TAKEAWAYS = [
    "Every Nevada contractor takes the open-book Business and Law (CMS) exam plus a trade exam, both at PSI.",
    "PSI charges $95 for one exam or $140 for a trade exam with the CMS; you get three attempts.",
    "Electricians in Las Vegas, Clark County and Reno need an ID card from ESP after an ICC exam.",
]
HOME_SEARCH_PLACEHOLDER = "Try B-2, C-15A, CMS or journeyman"
LICENSES_COVERED = "Nevada licenses covered"
HOME_TABLE = {
    "h2": "Which Nevada license needs which exam?",
    "sub": "The Contractors Board licenses businesses by classification, and every classification shares one business exam. Electricians and plumbers carry local cards on top.",
    "head": ["License", "Who issues it", "Exams", "Book rules"],
    "rows": [
        ["B General Building", "NSCB", "CMS + B trade exam at PSI", "CMS open book; trade exam with listed codes"],
        ["B-2 Residential and Small Commercial", "NSCB", "CMS + B-2 trade exam at PSI", "CMS open book; trade exam with listed codes"],
        ["B-7 Restricted (jobs up to $7,000)", "NSCB", "No trade exam", "Valid 2 years, no life-safety trades"],
        ["C specialty (C-1 to C-42)", "NSCB", "CMS + trade exam at PSI", "CMS open book; trade exam with listed codes"],
        ["Business and Law (CMS)", "NSCB, given by PSI", "60 scored questions, 120 minutes, 75% to pass", "Open book, Nevada manual"],
        ["Journeyman electrician card", "ESP, after ICC G17", "80 questions, 4 hours", "Open book, NEC"],
        ["Master electrician card", "ESP, after ICC G16", "ICC national exam", "Open book, NEC"],
    ],
    "hot": 1,
    "note": "Figures from the NSCB, PSI, ICC and the City of Reno, checked November 10, 2026. Confirm with the board before you apply, since fees and rules change.",
}
HOME_FAQ = [
    ("Which Nevada license do I need?", "The right license depends on the work. Building contractors hold a B, B-2, B-6 or B-7; engineering work such as grading, pipelines and pools is Class A; each trade has a C classification, from C-1 plumbing to C-42. Electricians also carry a local ID card."),
    ("What exams does a Nevada contractor take?", "Two, both at PSI: the Business and Law exam, called the CMS, which every applicant takes, and the trade exam for your classification. The Board can waive the trade exam in some cases, for example licensure by endorsement."),
    ("Are the Nevada exams open book?", "The CMS is open book with the Construction Business and Law Manual for Nevada. Trade exams are closed book except for the code references their PSI outline allows. ICC electrician exams are open book with the NEC."),
    ("What do the exams cost?", "PSI charges $95 for one exam portion, or $140 for a trade exam taken with the CMS. The NSCB application fee is $300, and your bond and monetary limit are set by the Board."),
    ("What is the new B-7 Restricted License?", "A license created by SB 130 for residential remodeling jobs up to $7,000, labor and materials included. It needs no trade exam, lasts 2 years and excludes life-safety trades. The NSCB began taking applications in March 2026."),
    ("Are these the real exam questions?", "No. Licensing exam questions are confidential. The courses and practice exams here are original material written to the same subjects and format, with explanations."),
    ("Does buying a package register me for the exam?", "No. The NSCB approves your application and sends an eligibility letter, then you book with PSI. Electrician card candidates book the ICC exam. A package gets you ready for the test itself."),
    ("How do orders arrive?", "Books ship from our fulfillment center, {ful}; online courses and practice exams arrive by email after purchase. Rental books go back after your exam."),
]
GENERAL_FAQ_LEAD = "{n} answers about Nevada contractor, Business and Law and electrician card exams: which board issues what, what PSI charges, how the CMS works, the open and closed book rules, how to study and how ordering works. Each of the {k} license pages adds questions of its own, built from the same NSCB, PSI and ICC sources."
FAQ_TAKEAWAYS = [
    "The NSCB licenses contractors in Classes A, B and C; every applicant takes the CMS plus a trade exam.",
    "PSI exams cost $95 for one portion or $140 with the CMS, with three attempts.",
    "Electrician ID cards come from ESP after an ICC national exam.",
]
BLOG_FAQ = [
    ("How long should I study for the Nevada Business and Law exam?", "Most candidates do well with three to four weeks at about an hour a day: learn the layout of the Construction Business and Law Manual for Nevada, then run timed practice. The CMS gives you 120 minutes for 60 scored questions."),
    ("Is the exam open book, and which books do I bring?", "The CMS is open book with the Nevada manual only. Trade exams are closed book except for the code references named in the PSI outline for your classification."),
    ("Do I need a separate license to work as an electrician in Nevada?", "Electricians in Las Vegas, Clark County and Reno need an Electrical Qualifications ID card from ESP after an ICC exam. The contracting business needs an NSCB C-2 license."),
    ("Are the practice questions the real exam questions?", "No. Licensing exam questions are confidential. Our courses and practice exams are original material written to the same subjects and format."),
    ("Does buying a package register me for the exam?", "No. The NSCB approves you first and sends an eligibility letter, then you book with PSI."),
    ("How do orders arrive?", "Books ship from our fulfillment center, {ful}; online courses arrive by email after purchase."),
]
FAQ_LICENSE_SECTIONS = [
    ("licenses", "Where are the questions for building, electrician and CMS exams?", ("building", "electricians", "electrical", "business", "plumbing", "codes")),
    ("licenses-trades", "Where are the questions for the C trade licenses?", ("mechanical", "finish", "structure")),
    ("licenses-specialty", "Where are the questions for specialty and Class A licenses?", ("specialty", "engineering")),
]
FAQ_GROUP_INTRO = {"contractor": "Nevada licensing", "trades": "Trade licenses"}
LLM_SUMMARY = "Exam prep for {n} Nevada licenses: NSCB Class A general engineering, Class B general building (B, B-2, B-6, B-7) and Class C specialty classifications, the Nevada Business and Law (CMS) exam, ICC exams for the Las Vegas, Clark County and Reno Electrical Qualifications ID cards, journeyman plumber cards, NASCLA and code courses."
LLM_FACTS = [
    "- Nevada contractors are licensed by the Nevada State Contractors Board (NSCB) in Class A (general engineering), Class B (general building) and Class C (specialty) classifications.",
    "- Every applicant takes the Business and Law exam (CMS) plus a trade exam for the classification, both at PSI. PSI charges $95 for one portion or $140 for a trade exam with the CMS. Three attempts, then the application is void.",
    "- The CMS is open book with the Construction Business and Law Manual for Nevada: 60 scored questions, 120 minutes, 45 correct (75%) to pass. Trade exams are closed book except for the code references in their outline.",
    "- The Board sets a bond of $1,000 to $500,000 and a monetary limit on every license. The application fee is $300.",
    "- B-7 Restricted License (SB 130): residential remodel jobs up to $7,000, no trade exam, valid 2 years, no life-safety trades; applications open since March 2026.",
    "- Electricians in Las Vegas, Clark County and Reno need an Electrical Qualifications ID card from Electrical Safety Professionals after an ICC exam (G16 master, G17 journeyman, G18 residential, G21 low voltage). Cards last 3 years.",
]
BLOG_LEAD = "Study plans, NSCB licensing rules and exam strategy for Nevada contractor, Business and Law and electrician card exams, written for people who work full days and study at night. Each post links to the license it covers, and every rule we quote links to the board that sets it."

# short labels for the Quick facts box on license pages
_ISS = "NSCB, exams by PSI"; _BK = "CMS open book; trade exam with listed codes"
ISSUER_SHORT = {g: _ISS for g in ("building", "electrical", "mechanical", "finish", "structure", "specialty", "engineering", "business")}
ISSUER_SHORT.update({"electricians": "ESP, after an ICC exam", "plumbing": "Local plumbing board", "codes": "ICC or NASCLA"})
BOOK_SHORT = {g: _BK for g in ("building", "electrical", "mechanical", "finish", "structure", "specialty", "engineering")}
BOOK_SHORT.update({"business": "Open book, Nevada manual only", "electricians": "Open book, NEC", "plumbing": "Open book in Reno, 2024 UPC", "codes": "Open book, most categories"})
# the line across the top of every page in designs that show it
PROMO = "Every Nevada contractor takes the Business and Law (CMS) exam: open book, 60 questions"
# products pictured in the home page collage: (license, package type); the newest code year wins
COLLAGE = [("b-2-residential-and-small-commercial", "highlighted-tabbed"), ("business-and-law-cms", "highlighted-tabbed"), ("journeyman-electrician", "ultimate-combo"), ("c-2-electrical", "exam-room-books")]  # (license, package type)

# the words people use for each license, for the exam advisor (Max) if it is switched on
MAX_ALIASES = {
    "b-general-building": ["general contractor", "general building", "class b", "b license", "gc license"],
    "b-2-residential-and-small-commercial": ["b-2", "b2", "residential contractor", "home builder", "small commercial"],
    "b-6-commercial-remodeling": ["b-6", "b6", "commercial remodel"],
    "b-7-residential-remodeling": ["b-7", "b7", "handyman", "residential remodel", "restricted license"],
    "business-and-law-cms": ["cms", "business and law", "business law", "management survey", "law exam"],
    "licensing-services": ["llc", "application help", "business setup", "corporation", "apply for my license"],
    "journeyman-electrician": ["journeyman electrician", "g17", "journeyman card", "electrician card"],
    "master-electrician": ["master electrician", "g16", "master card"],
    "residential-electrician": ["residential electrician", "g18", "residential card"],
    "low-voltage-electrician": ["low voltage electrician", "g21"],
    "c-2-electrical": ["electrical contractor", "c-2", "c2"],
    "journeyman-plumber": ["journeyman plumber", "plumber card"],
    "nascla-commercial-general-building": ["nascla", "commercial general"],
}
