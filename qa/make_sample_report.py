from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

TEAL, OCHRE, BLACK, GREY = RGBColor(0x09, 0x56, 0x56), RGBColor(0xC0, 0x8A, 0x2E), RGBColor(0x1A, 0x1A, 0x1A), RGBColor(0x6B, 0x6B, 0x6B)
FONT = "Aptos"
TM = "™"
CLIENT = "[Client company name]"
SPONSOR = "[Sponsor name]"

doc = Document()
sec = doc.sections[0]
sec.left_margin = sec.right_margin = Cm(2.2)
sec.top_margin, sec.bottom_margin = Cm(2.2), Cm(2.0)
st = doc.styles["Normal"]
st.font.name, st.font.size, st.font.color.rgb = FONT, Pt(10), BLACK
st.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
st.paragraph_format.line_spacing = 1.15
st.paragraph_format.space_after = Pt(4)


def run(p, text, bold=False, italic=False, color=None, size=None):
    r = p.add_run(text)
    r.bold, r.italic, r.font.name = bold, italic, FONT
    if color is not None:
        r.font.color.rgb = color
    if size:
        r.font.size = Pt(size)
    return r


def para(text="", bold=False, italic=False, color=None, size=None, align=None, after=None, keep=False):
    p = doc.add_paragraph()
    if text:
        run(p, text, bold, italic, color, size)
    if align:
        p.alignment = align
    if after is not None:
        p.paragraph_format.space_after = Pt(after)
    if keep:
        p.paragraph_format.keep_with_next = True
    return p


def h1(text):
    p = para(text, bold=True, color=OCHRE, size=15, keep=True)
    p.paragraph_format.space_before = Pt(14)
    pPr = p._p.get_or_add_pPr()
    b = OxmlElement("w:pBdr")
    bt = OxmlElement("w:bottom")
    for k, v in (("val", "single"), ("sz", "6"), ("space", "1"), ("color", "C08A2E")):
        bt.set(qn("w:" + k), v)
    b.append(bt)
    pPr.append(b)
    return p


def h2(text):
    p = para(text, bold=True, color=TEAL, size=11.5, keep=True)
    p.paragraph_format.space_before = Pt(8)
    return p


def labelled(label, text):
    p = doc.add_paragraph()
    run(p, label + " ", bold=True)
    run(p, text)
    return p


def bullet(text, label=None):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.8)
    p.paragraph_format.first_line_indent = Cm(-0.5)
    p.paragraph_format.space_after = Pt(3)
    run(p, "•  ", color=OCHRE, bold=True)
    if label:
        run(p, label + " ", bold=True)
    run(p, text)
    return p


def shade(cell, hex_fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_fill)
    tcPr.append(shd)


def table(headers, rows, widths):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    for i, h in enumerate(headers):
        c = t.rows[0].cells[i]
        shade(c, "095656")
        c.paragraphs[0].text = ""
        run(c.paragraphs[0], h, bold=True, color=RGBColor(0xFF, 0xFF, 0xFF))
    for r in rows:
        cells = t.add_row().cells
        for i, v in enumerate(r):
            cells[i].paragraphs[0].text = ""
            if i == 0:
                run(cells[i].paragraphs[0], v, bold=True)
            else:
                run(cells[i].paragraphs[0], v)
    for i, w in enumerate(widths):
        t.columns[i].width = Cm(w)
    for row in t.rows:
        for i, w in enumerate(widths):
            row.cells[i].width = Cm(w)
    for row in t.rows:
        for c in row.cells:
            for p in c.paragraphs:
                p.paragraph_format.space_after = Pt(2)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t


def pagebreak():
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


def add_field(p, code):
    r = p.add_run()
    r.font.name = FONT
    r.font.size = Pt(9)
    for t, txt in (("begin", None), (None, code), ("end", None)):
        if t:
            e = OxmlElement("w:fldChar")
            e.set(qn("w:fldCharType"), t)
        else:
            e = OxmlElement("w:instrText")
            e.set(qn("xml:space"), "preserve")
            e.text = txt
        r._r.append(e)


# header and footer
hp = sec.header.paragraphs[0]
hp.alignment = WD_ALIGN_PARAGRAPH.CENTER
run(hp, "ILLUSTRATIVE SAMPLE  |  Fictional data and client  |  Not a real engagement", bold=True, color=TEAL, size=9)
fp = sec.footer.paragraphs[0]
fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
run(fp, f"© Hannie Consultants cc  ·  HannieVerse Enterprise{TM}, 2026  ·  Confidential  ·  Page ", color=GREY, size=9)
add_field(fp, "PAGE")

# ---------------- cover ----------------
for _ in range(5):
    para()
para(f"THE HONOUR{TM} REPORT", bold=True, color=OCHRE, size=28, align=WD_ALIGN_PARAGRAPH.CENTER, after=4)
para("Organisational Diagnostic Report", bold=True, color=TEAL, size=16, align=WD_ALIGN_PARAGRAPH.CENTER, after=18)
para(f"Prepared for: {CLIENT}", bold=True, size=12, align=WD_ALIGN_PARAGRAPH.CENTER, after=14)
para("Engagement dates", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, after=2)
for s in ("Session 1 (Reveal): Tuesday 3 November 2026",
          "Session 2 (Align): Friday 6 November 2026",
          "Session 3 (Direct): Wednesday 11 November 2026"):
    para(s, align=WD_ALIGN_PARAGRAPH.CENTER, after=1)
para()
para("Report delivered: Wednesday 18 November 2026", align=WD_ALIGN_PARAGRAPH.CENTER, after=14)
para(f"Facilitated and prepared by Priscilla Hannie, Honour{TM} Facilitator", align=WD_ALIGN_PARAGRAPH.CENTER, after=0)
para(f"on behalf of HannieVerse Enterprise{TM}", align=WD_ALIGN_PARAGRAPH.CENTER, after=30)
para("CONFIDENTIAL", bold=True, color=RGBColor(0xC0, 0x30, 0x30), size=14, align=WD_ALIGN_PARAGRAPH.CENTER)
pagebreak()

# ---------------- confidentiality ----------------
h1("Confidentiality & Distribution")
para(f"This report was prepared exclusively for {CLIENT} as part of an Honour{TM} Diagnostic engagement by Hannie Consultants cc. "
     "It is intended only for the sponsor and the leadership team named in the Corporate Intake & Consent Form. "
     "Please do not share it beyond that group.")
h2("How participant anonymity is protected")
bullet("No finding, quote or observation is attributed to any individual, and no participant is named.")
bullet("Functions, teams and roles are not named in connection with any finding. In a group of this size, naming a function could point to one person.")
bullet("A theme appears in this report only if at least three participants raised it. Anything raised by fewer than three is withheld.")
bullet("Where participants' own words inform a finding, they are paraphrased so they cannot be traced to a person.")
bullet("Each participant receives an individual report, prepared and delivered separately under separate consent terms. The sponsor does not receive these.")

h1("About This Report")
h2(f"What is the Honour{TM} Diagnostic?")
para(f"Honour{TM} is a two-week organisational diagnostic built on the R·A·D Model: Reveal, Align, Direct. "
     "It gives a clear and objective view of an organisation's current realities, free from urgency, assumptions and internal politics, "
     "together with recommendations. It does not implement change or replace leadership. "
     "The organisation decides what to act on and when.")
h2("How to read the findings")
para("Findings describe the group as a whole. Each theme carries a strength marker so you can see how widely it was shared:")
bullet("raised by 6 or more of the 9 participants.", "Most:")
bullet("raised by 4 or 5 participants.", "Many:")
bullet("raised by 3 participants. This is the minimum for inclusion.", "Several:")

h2("The R·A·D Model in this engagement")
table(["Stage", "Session", "Purpose"],
      [["Reveal", "Session 1, Tuesday 3 November", "Surface current realities and identify patterns that are sensed but not openly discussed."],
       ["Align", "Session 2, Friday 6 November", "Review the anonymised diagnostic data together and map where misalignment lies: in roles, communication, systems, leadership or the work itself."],
       ["Direct", "Session 3, Wednesday 11 November", "Consolidate findings, test assumptions and confirm the overall picture. This is where insight becomes direction."]],
      [2.6, 5.0, 8.8])

h2("How the engagement unfolded")
table(["When", "Step"],
      [["Before Session 1", "Sponsor completed the Corporate Intake & Consent Form. Each participant completed the Individual Participant Experience form."],
       ["Tue 3 Nov", "Session 1: Reveal (90 minutes, online, live)."],
       ["After Session 1", "Each participant received a private Reflect questionnaire by email, due by Thursday 5 November. 9 of 9 completed it."],
       ["Fri 6 Nov", "Session 2: Align (90 minutes, online, live)."],
       ["After Session 2", "Each participant received a private Integrate questionnaire by email, due by Tuesday 10 November. 9 of 9 completed it."],
       ["Wed 11 Nov", "Session 3: Direct (90 minutes, online, live)."],
       ["Wed 18 Nov", "This report was delivered to the sponsor, within 5 business days of Session 3. Individual participant reports were delivered at the same time."]],
      [3.4, 13.0])

h2("Data sources & anonymisation")
para("This report draws on six data sources: the Corporate Intake & Consent Form, the Individual Participant Experience form, "
     "the three live sessions, and the private Reflect and Integrate questionnaires.")
para("All personal identifiers, such as names and email addresses, were removed and replaced with each participant's Tally submission ID before analysis. "
     "The facilitator securely retains the mapping of submission IDs to identities. It is not included in this report.")
para("This process complies with South Africa's POPIA and, where applicable, the EU/UK's GDPR. "
     "No individual response is attributed by name, function or role anywhere in this document.")
pagebreak()

# ---------------- summary ----------------
h1("Executive Summary")
para("This report summarises an Honour™ Diagnostic with nine participants, held eight months after the organisation's merger.".replace("™", TM))
para("Participants described an organisation that works hard and absorbs friction that its structure should be absorbing. "
     "The merger is not yet fully integrated. Some core processes still run in parallel, no single role owns finishing the job, "
     "and decisions tend to wait for approval at several levels. The result is that experienced managers carry the cost.")
para("The group's own conclusion was constructive. Participants agreed that speed and control are not opposites, and that a tiered, risk-based way of deciding, "
     "supported by a shared planning rhythm, would give them both. Section Five sets out five recommendations. "
     "Section Six lists the risks to watch if the findings are acknowledged but not owned.")

h1("Engagement Snapshot")
table(["Item", "Detail"],
      [["Organisation", CLIENT],
       ["Industry / context", "Professional services, eight months after a merger"],
       ["Sponsor", SPONSOR],
       ["Session dates", "Tuesday 3, Friday 6 and Wednesday 11 November 2026"],
       ["Participants", "9 (minimum 5, maximum 9 per engagement)"],
       ["Participation", "9 of 9 completed the Reflect questionnaire. 9 of 9 completed the Integrate questionnaire."],
       ["Sponsor attendance", "The sponsor did not attend the sessions, as the participants preferred."],
       ["Who took part", "A cross-section of the organisation. Functions and roles are not named in this report, to protect anonymity."]],
      [4.2, 12.2])

# ---------------- section one ----------------
h1("Section One: What Surfaced (Reveal)")
para("In a post-merger setting, surfacing matters because the realities that shape daily work are rarely visible in formal reporting lines. "
     "Session 1 and the Reflect questionnaire revealed a disconnect between leadership intent and day-to-day execution.")
h2("Patterns & threads identified")
bullet("Decisions are escalated through several management layers, even when the people closest to the work have the expertise to decide.", "Escalation loops (most).")
bullet("Early warnings of risk, especially about technical infrastructure, are often treated as opinion until something fails. Investment tends to follow failure, not precede it.", "\"Wait for it to break\" budgeting (many).")
bullet("For eight months, parallel processes have caused repeated work, duplicated purchase orders and vendor payments, unmerged contract templates and inconsistent messages to clients.", "Parallel processes (most).")
bullet("Teams that support delivery are often brought in to refine decisions already made, instead of helping to shape direction.", "Late involvement (many).")
bullet("Leadership has asked for speed. Execution teams carry the gaps that speed leaves behind.", "Intent and execution (most).")
h2("What is working")
bullet("A strong commitment to the organisation and to clients, and a willingness to speak honestly in the sessions (most).")
bullet("Informal networks that keep work moving while the formal structure catches up (many).")
para("Addressing these patterns means moving from managing symptoms to redesigning how decisions, risk and ownership work.", italic=True)

# ---------------- section two ----------------
h1("Section Two: Where Misalignment Lives (Align)")
para("Misalignment here comes from conflicting structural priorities and incompletely integrated legacy arrangements, not from individual shortcomings.")
h2("The root-cause-to-symptom chain")
bullet("Incomplete integration of core processes: sales, vendor management and legal templates.", "Root cause:")
bullet("High \"absorption\" cost for middle managers, and persistent confusion for clients.", "Symptom:")
h2("Where the group placed the misalignment")
table(["Area", "What the group described"],
      [["Roles", "Clear ownership for completing the merger is missing. Duplicated purchase orders, vendor payments and unmerged contract templates persist because no single role has authority to finalise the integration. (most)"],
       ["Communication", "Policies are sometimes used to avoid direct conversations. Experienced people's pattern recognition is sometimes mistaken for cynicism. Managers absorb stress to shield their teams. (many)"],
       ["Systems", "Legacy systems are not integrated. AI tools are used informally for drafting and monitoring, with no organisation-wide risk, security or verification policy. AI-assisted output is sometimes skimmed, not checked, before it reaches clients or contracts. (many)"],
       ["Leadership", "The directive to move quickly is not matched by the authority to decide closer to the work. Client-facing teams are sometimes pressed to commit before delivery has confirmed it can deliver, which leads to reactive damage control. (most)"],
       ["The work itself", "The handoff between selling and delivering has gaps, so clients do not always hear one consistent story. (many)"]],
      [3.8, 12.6])
h2("Where the group is already aligned")
bullet("A shared wish to close the gap between promises and delivery (most).")
bullet("Agreement that a tiered approach to approvals would help (most).")
bullet("Respect for the people who have been absorbing the friction (several).")

# ---------------- section three ----------------
h1("Section Three: The Fixed Point (Direct)")
para("A fixed point of truth anchors future commitments and helps the organisation avoid slipping back into avoidance. "
     "In Session 3 the group tested and confirmed this statement:")
p = para("“Speed and safety are compatible when supported by a tiered, risk-based approval process and coordinated planning cycles.”",
         bold=True, italic=True, color=TEAL, size=11)
p.paragraph_format.left_indent = Cm(0.8)
para("This marks a shift in how risk is seen. The organisation is moving from viewing its legal and finance controls as gatekeepers "
     "to seeing them as partners in scaling risk. That shift allows decisions on low-risk matters to be made closer to the work, "
     "with collaborative scrutiny kept for high-risk decisions.")

# ---------------- section four ----------------
h1("Section Four: Areas of Appetite & Possibility")
para("The diagnostic identified specific areas where the group showed strong motivation for structural change.")
bullet("Participants from across the business expressed strong interest in quarterly alignment. This would let support teams influence direction instead of being involved only after decisions are made. (most)", "A joint planning rhythm:")
bullet("Participants were interested in making technical and compliance risk a shared business priority, not one person's opinion. (many)", "A shared risk register:")
bullet("There is strong interest in piloting a tiered model to reduce friction on low-spend, low-risk decisions and to free management capacity. (most)", "Simplified approvals:")

# ---------------- section five ----------------
h1("Section Five: Recommendations")
para("Honour™ recommends. It does not implement. Each recommendation below is linked to a finding, with a suggested first step, "
     "so leadership can decide what to act on and when. Owners and dates are for leadership to confirm.".replace("™", TM))
recs = [
    ("1. Complete the merger with a single accountable owner",
     "Addresses the missing ownership and the parallel processes in Sections One and Two.",
     "Name one role with authority to finalise integration. List every unresolved item (purchase orders, vendor payments, contract templates) with an owner and a date.",
     "Within 30 days."),
    ("2. Pilot a tiered approval model",
     "Addresses escalation loops and the perceived conflict between speed and control.",
     "Define three tiers by spend and risk. Pilot for one quarter. The pilot must keep a non-negotiable legal and compliance review on all contract-facing items.",
     "Design within 30 days. Pilot for one quarter."),
    ("3. Formalise a shared technical and legal risk register",
     "Addresses \"wait for it to break\" budgeting.",
     "Create one register that anyone can add to. Review it monthly. Link budget decisions to risk rating, not to failure.",
     "Within 60 days."),
    ("4. Introduce a cross-functional planning rhythm",
     "Addresses late involvement of support teams and the selling-to-delivery handoff gap.",
     "Hold one joint planning session next quarter, with sales, delivery, finance, operations and support teams in the room, and agree one client narrative.",
     "Next quarter."),
    ("5. Agree a simple AI verification policy",
     "Addresses informal AI use without oversight (Systems, Section Two).",
     "Decide which AI-assisted outputs must be checked before they reach clients or contracts, and who checks them. Start with the highest-risk outputs.",
     "Within 60 days."),
]
for title, why, first, when in recs:
    h2(title)
    labelled("Why:", why)
    labelled("Suggested first step:", first)
    labelled("Suggested timing:", when + " Owner: [to be confirmed by leadership].")

# ---------------- section six ----------------
h1("Section Six: Risk Areas & Watch Items")
para("Monitoring cultural resistance and structural barriers is essential to acting on these recommendations.")
bullet("Managers who have been absorbing friction are approaching their limits. If their workload is not reduced, there is a real risk of losing institutional knowledge and of wider failure.", "Absorption fatigue:")
bullet("Some participants see this diagnostic as a final attempt to escalate long-standing issues. If findings are acknowledged but not assigned to an owner, there is a real risk of disengagement.", "Initiative drift:")
bullet("Continued use of AI for sensitive work without a verification policy remains a compliance and data-security liability.", "The AI \"quiet use\" risk:")

# ---------------- closing ----------------
h1("Closing Statement")
para("The group showed real courage in this diagnostic by naming uncomfortable truths that have persisted since the merger. "
     "There is a clear desire to close the gap between promises and delivery and to move toward honest, shared ownership.")
para("Completing the integration is now an operational requirement, not only a strategic goal. By shifting from avoidance to a structured, tiered model of risk and ownership, "
     "leadership can free capacity currently spent on reactive work and focus on sustainable growth.")
h2("What happens next")
bullet("Individual participant reports have been delivered separately to each participant.")
bullet("You decide which recommendations to act on, and when.")
bullet("Questions about this report: Priscilla Hannie, hello@hannieonline.co.za.")
para()
para(f"Honour{TM} Diagnostic is a proprietary framework of HannieVerse Enterprise{TM} and Hannie Consultants cc. Not for redistribution.",
     italic=True, color=GREY, size=9, align=WD_ALIGN_PARAGRAPH.CENTER)

out = "/home/user/Honour-Diagnostic/qa/sample-report/Honour-Report-SAMPLE-rewritten.docx"
doc.save(out)
print("saved", out)
