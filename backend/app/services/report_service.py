import logging
from fpdf import FPDF
from datetime import datetime
import google.generativeai as genai
from app.core.config import settings
from app.services.supabase_service import upload_pdf_to_supabase

logger = logging.getLogger(__name__)

def configure_gemini():
    if not settings.GEMINI_API_KEY:
        raise Exception("GEMINI_API_KEY is not configured in .env")
    genai.configure(api_key=settings.GEMINI_API_KEY)
    return genai.GenerativeModel("gemini-flash-lite-latest")  # free tier model

# ─────────────────────────────────────────────
# Prompt Builders
# ─────────────────────────────────────────────

def build_postmortem_prompt(incident, notes, creator_name: str, assignee_name: str) -> str:
    notes_text = "\n".join([f"  - [{n.created_at.strftime('%Y-%m-%d %H:%M')}] {n.note_text}" for n in notes]) or "  No internal notes recorded."
    return f"""You are a professional IT incident analyst. Write a formal and detailed post-mortem report for the following incident. Use professional language suitable for management review.

INCIDENT DETAILS:
Title: {incident.title}
Category: {incident.category}
Priority: {incident.priority.upper()}
Status: {incident.status.replace('_', ' ').title()}
Description: {incident.description}
Raised By: {creator_name}
Assigned To: {assignee_name}
Date Raised: {incident.created_at.strftime('%B %d, %Y at %H:%M')}
Last Updated: {incident.updated_at.strftime('%B %d, %Y at %H:%M')}

INTERNAL NOTES / ACTIVITY LOG:
{notes_text}

Write a structured post-mortem report with exactly these 6 sections. Use plain text only, no markdown symbols like **, ##, or *. Use numbered lists where appropriate:

1. EXECUTIVE SUMMARY
2. INCIDENT TIMELINE
3. ROOT CAUSE ANALYSIS
4. IMPACT ASSESSMENT
5. RESOLUTION STEPS TAKEN
6. RECOMMENDATIONS TO PREVENT RECURRENCE
"""

def build_summary_prompt(incident, creator_name: str) -> str:
    return f"""You are a professional IT support assistant. Write a concise and clear incident summary report for an end user. Keep it simple and avoid technical jargon.

INCIDENT DETAILS:
Title: {incident.title}
Category: {incident.category}
Priority: {incident.priority.upper()}
Status: {incident.status.replace('_', ' ').title()}
Description: {incident.description}
Raised By: {creator_name}
Date Raised: {incident.created_at.strftime('%B %d, %Y')}

Write a brief incident summary with these 3 sections using plain text only, no markdown symbols:
1. INCIDENT OVERVIEW
2. CURRENT STATUS
3. NEXT STEPS
"""

def build_analytics_prompt(stats: dict) -> str:
    return f"""You are a senior IT operations analyst. Write an executive monthly analytics report based on the following incident statistics. Use professional language suitable for C-level management.

INCIDENT STATISTICS FOR THIS PERIOD:
Total Incidents: {stats.get('total', 0)}
Open: {stats.get('open', 0)}
In Progress: {stats.get('in_progress', 0)}
Resolved: {stats.get('resolved', 0)}
Closed: {stats.get('closed', 0)}

By Priority:
  Critical: {stats.get('critical', 0)}
  High: {stats.get('high', 0)}
  Medium: {stats.get('medium', 0)}
  Low: {stats.get('low', 0)}

By Category: {stats.get('by_category', 'Not available')}

Write a concise executive report with these 4 sections using plain text only, no markdown symbols:
1. PERIOD SUMMARY
2. KEY TRENDS AND OBSERVATIONS
3. RISK AREAS
4. RECOMMENDATIONS FOR NEXT PERIOD
"""

# ─────────────────────────────────────────────
# Gemini API Call
# ─────────────────────────────────────────────

def generate_with_gemini(prompt: str) -> str:
    try:
        model = configure_gemini()
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        raise Exception(f"Failed to generate report with Gemini: {str(e)}")

# ─────────────────────────────────────────────
# PDF Generation with fpdf2
# ─────────────────────────────────────────────

def generate_pdf(title: str, subtitle: str, content: str, report_type: str) -> bytes:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Header bar
    pdf.set_fill_color(0, 85, 135)  # TCS Blue
    pdf.rect(0, 0, 210, 35, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_y(10)
    pdf.cell(0, 8, "TCS Enterprise Incident Management System", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, report_type.upper() + " REPORT", align="C", new_x="LMARGIN", new_y="NEXT")

    # Reset color
    pdf.set_text_color(30, 41, 59)
    pdf.set_y(45)

    # Sanitize content to avoid latin-1 unicode encoding errors with Helvetica
    def sanitize_text(text: str) -> str:
        replacements = {
            '—': '-', '–': '-', '“': '"', '”': '"', '‘': "'", '’': "'", '…': '...', '•': '-', '\u200b': ''
        }
        for k, v in replacements.items():
            text = text.replace(k, v)
        # Force encode/decode to latin-1 to strip any other unmappable unicode chars
        return text.encode('latin-1', errors='replace').decode('latin-1')

    title = sanitize_text(title)
    subtitle = sanitize_text(subtitle)
    content = sanitize_text(content)
    
    # Title
    pdf.set_font("Helvetica", "B", 15)
    pdf.multi_cell(0, 8, title, align="L", wrapmode="CHAR")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 6, f"Generated on: {datetime.utcnow().strftime('%B %d, %Y at %H:%M UTC')}", new_x="LMARGIN", new_y="NEXT")
    if subtitle:
        pdf.cell(0, 6, subtitle, new_x="LMARGIN", new_y="NEXT")

    # Divider
    pdf.set_draw_color(226, 232, 240)
    pdf.set_y(pdf.get_y() + 3)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.set_y(pdf.get_y() + 6)

    # Content
    pdf.set_text_color(30, 41, 59)
    pdf.set_font("Helvetica", "", 11)

    for line in content.split("\n"):
        stripped = line.strip()
        if not stripped:
            pdf.ln(3)
            continue
        # Detect section headers (lines ending with nothing but all caps or numbered)
        if stripped and (stripped[0].isdigit() and stripped[1] in ".):") or stripped.isupper():
            pdf.ln(4)
            pdf.set_font("Helvetica", "B", 12)
            pdf.set_text_color(0, 85, 135)
            pdf.multi_cell(0, 7, stripped, wrapmode="CHAR")
            pdf.set_font("Helvetica", "", 11)
            pdf.set_text_color(30, 41, 59)
        else:
            pdf.multi_cell(0, 6, stripped, wrapmode="CHAR")

    # Footer
    pdf.set_y(-20)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(148, 163, 184)
    pdf.cell(0, 5, sanitize_text("Confidential - TCS Enterprise IMS | AI-generated report using Google Gemini"), align="C")

    return bytes(pdf.output())

# ─────────────────────────────────────────────
# Full Pipeline: Generate + Upload
# ─────────────────────────────────────────────

def generate_and_upload_report(
    prompt: str,
    pdf_title: str,
    pdf_subtitle: str,
    report_type: str,
    file_name: str
) -> str:
    """Full pipeline: Gemini → PDF → Supabase → returns public URL"""
    content = generate_with_gemini(prompt)
    pdf_bytes = generate_pdf(pdf_title, pdf_subtitle, content, report_type)
    url = upload_pdf_to_supabase(pdf_bytes, file_name)
    return url
