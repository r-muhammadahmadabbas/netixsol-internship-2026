"""Generate Executive Report PDF."""

from fpdf import FPDF

class ReportPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.cell(0, 8, "Web3Geeks Client Inquiry Qualification Agent", align="C", new_x="LMARGIN", new_y="NEXT")
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def section_title(self, title):
        self.set_font("Helvetica", "B", 12)
        self.set_fill_color(41, 128, 185)
        self.set_text_color(255, 255, 255)
        self.cell(0, 8, f"  {title}", fill=True, new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(0, 0, 0)
        self.ln(3)

    def body_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 5, text)
        self.ln(2)

    def bullet(self, text):
        self.set_font("Helvetica", "", 10)
        self.cell(5, 5, "-")
        self.multi_cell(0, 5, text)
        self.ln(1)

    def add_table(self, headers, rows):
        self.set_font("Helvetica", "B", 9)
        col_width = 190 / len(headers)
        for h in headers:
            self.cell(col_width, 7, h, border=1, align="C")
        self.ln()
        self.set_font("Helvetica", "", 9)
        for row in rows:
            for cell in row:
                self.cell(col_width, 6, str(cell), border=1, align="C")
            self.ln()
        self.ln(3)


pdf = ReportPDF()
pdf.alias_nb_pages()
pdf.set_auto_page_break(auto=True, margin=20)
pdf.add_page()

# Title
pdf.set_font("Helvetica", "B", 16)
pdf.cell(0, 10, "Executive Report", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", "", 11)
pdf.cell(0, 7, "Web3Geeks Client Inquiry Qualification Agent", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(6)

# 1. Business Goal
pdf.section_title("1. Business Goal")
pdf.body_text(
    "Web3Geeks receives numerous client inquiries daily. Currently, sales team "
    "manually reviews each inquiry, researches the client company, and drafts "
    "responses. This process is time-consuming (15-30 minutes per inquiry), "
    "inconsistent, and cannot scale without hiring."
)
pdf.body_text(
    "Solution: Automated client inquiry qualification agent that validates "
    "inquiries, researches companies, qualifies leads, drafts responses, and "
    "pauses for human approval on critical decisions."
)

# 2. Architecture
pdf.section_title("2. Architecture")
pdf.body_text(
    "Flow: User Input -> Validate -> Research -> Qualify -> Draft -> Human Approve -> End\n"
    "Error Handler catches bad input at any stage."
)
pdf.bullet("Validator: Checks required fields, email format")
pdf.bullet("Researcher: Looks up company in local database")
pdf.bullet("Qualifier: Scores lead (high/medium/low)")
pdf.bullet("Drafter: Creates personalized response using LLM")
pdf.bullet("Human Review: Approves before sending")

# 3. Framework Choice
pdf.section_title("3. Framework Choice Rationale")
pdf.body_text("Selected: LangGraph (with CrewAI-style role design)")
pdf.bullet("Control-heavy workflow: HITL requires precise control")
pdf.bullet("Conditional routing: Bad input -> error handler")
pdf.bullet("State management: Track data through stages")
pdf.bullet("Why NOT CrewAI: Lacks precise HITL control")

# 4. Evaluation Results
pdf.section_title("4. Evaluation Results")
pdf.add_table(
    ["Criterion", "Score", "Notes"],
    [
        ["Task Success", "3/8 (38%)", "Edge cases as errors (expected)"],
        ["Factual Accuracy", "5/5", "Correct company info"],
        ["Latency", "8.5s avg", "Within acceptable range"],
        ["Cost per Run", "$0.002", "Very affordable"],
        ["Tone/Quality", "5/5", "Professional responses"],
        ["Safety", "100%", "All tests passed safely"],
    ]
)

# 5. Known Limitations
pdf.section_title("5. Known Limitations")
pdf.bullet("Small database: Only 5 companies in DB")
pdf.bullet("No web search: Cannot look up unknown companies")
pdf.bullet("Auto-approval: High/medium leads auto-approved")
pdf.bullet("Single LLM: No fallback if primary LLM fails")
pdf.bullet("No persistence: Results not saved to database")

# 6. Next Steps
pdf.section_title("6. Recommended Next Steps")
pdf.bullet("Scaling: Expand DB, add web search, deploy to cloud")
pdf.bullet("Guardrails: Content filtering, rate limiting, retry logic")
pdf.bullet("Human Oversight: Email notifications, approval dashboard")
pdf.bullet("Monitoring: Dashboard, alerting, cost tracking")

pdf.output(r"C:\Internship\Netixsol\week-2\day-5\executive_report.pdf")
print("PDF generated: executive_report.pdf")
