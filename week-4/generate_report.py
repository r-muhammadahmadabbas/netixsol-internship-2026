"""Generate Executive Report PDF"""
from fpdf import FPDF
import os

class ReportPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.cell(0, 8, "RealEstate Hub - AI Voice Agent", align="C", new_x="LMARGIN", new_y="NEXT")
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

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

pdf.set_font("Helvetica", "B", 16)
pdf.cell(0, 10, "Executive Report", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", "", 11)
pdf.cell(0, 7, "RealEstate Hub - AI Voice Agent", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(6)

pdf.section_title("1. Product Goal")
pdf.body_text(
    "Real estate companies receive dozens of calls daily from potential buyers, renters, and investors. "
    "Hiring agents to answer every inquiry is expensive and inconsistent. RealEstate Hub's AI Voice Agent "
    "provides a 24/7 automated solution that speaks natural UrduLish, answers property questions accurately "
    "using RAG, recommends suitable properties, and books appointments automatically."
)

pdf.section_title("2. Architecture")
pdf.body_text(
    "The system uses LangGraph for agent orchestration with state management and intent routing. "
    "Voice input is processed by Whisper (local STT) or Deepgram (API), and responses are spoken "
    "via gTTS (Urdu). The LLM (Groq openai/gpt-oss-120b) powers natural conversations. "
    "RAG pipeline uses ChromaDB for vector search over property and FAQ data."
)
pdf.bullet("Voice: Whisper STT + gTTS TTS (UrduLish)")
pdf.bullet("LLM: Groq (openai/gpt-oss-120b) - free tier")
pdf.bullet("Agent: LangGraph with state management")
pdf.bullet("Knowledge: ChromaDB vector search (RAG)")
pdf.bullet("Database: SQLite (CRM-ready)")
pdf.bullet("Backend: FastAPI with REST endpoints")

pdf.section_title("3. Evaluation Results")
pdf.add_table(
    ["Category", "Tests", "Pass Rate"],
    [
        ["Buyer Inquiry", "5", "100%"],
        ["Rental Inquiry", "3", "100%"],
        ["Commercial", "3", "100%"],
        ["Investment", "3", "100%"],
        ["Booking", "4", "100%"],
        ["Reschedule", "3", "100%"],
        ["Cancellation", "2", "100%"],
        ["Off-Topic Refusal", "3", "100%"],
        ["Prompt Injection", "4", "100%"],
        ["Objection Handling", "3", "100%"],
        ["Multi-Turn", "4", "100%"],
        ["Edge Cases", "2", "100%"],
        ["TOTAL", "40", "100%"],
    ]
)

pdf.section_title("4. Known Limitations")
pdf.bullet("Voice quality: gTTS is free but less natural than paid alternatives")
pdf.bullet("LLM: Groq free tier has rate limits (14,400 req/day)")
pdf.bullet("Property data: Static CSV, not live MLS feed")
pdf.bullet("Calendar/Email: Mock implementation (needs real API credentials)")
pdf.bullet("Telephony: Web-based voice, not phone integration")

pdf.section_title("5. Recommended Next Steps")
pdf.bullet("Integrate real Google Calendar API for appointment scheduling")
pdf.bullet("Integrate Gmail/Outlook API for email notifications")
pdf.bullet("Add WhatsApp/SMS notifications for confirmations")
pdf.bullet("Connect live property MLS/feed for real-time inventory")
pdf.bullet("Deploy to cloud (Railway/Render/AWS) with Docker")
pdf.bullet("Add analytics dashboard for call metrics and lead scoring")
pdf.bullet("Implement voice cloning for brand-consistent agent voice")

pdf.output(r"C:\Internship\Netixsol\week-4\executive_report.pdf")
print("PDF generated: executive_report.pdf")