from flask import Blueprint, render_template, request, send_file
from models.scan import Scan
from fpdf import FPDF
from io import BytesIO
import re
from report_form import ReportForm  # ✅ you got this right — fine if it's in same dir

reporting_routes = Blueprint("reporting_routes", __name__)

@reporting_routes.route('/stage5', methods=["GET", "POST"])
def stage5():
    scans = Scan.query.order_by(Scan.timestamp.desc()).all()
    form = ReportForm()

    # ✅ Populate the choices for SelectMultipleField dynamically
    form.scan_ids.choices = [
        (scan.id, f"{scan.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {scan.tool_used} on {scan.target}")
        for scan in scans
    ]

    # ✅ Use form.validate_on_submit() instead of checking request.method manually
    if form.validate_on_submit():
        selected_ids = form.scan_ids.data  # ✅ direct from form field
        selected_scans = Scan.query.filter(Scan.id.in_(selected_ids)).all()

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)

        for scan in selected_scans:
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            pdf.cell(200, 10, txt=f"Scan Report - {scan.timestamp.strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
            pdf.ln(5)
            pdf.multi_cell(0, 10, f"Target: {scan.target}")
            pdf.multi_cell(0, 10, f"Tool Used: {scan.tool_used}")
            pdf.multi_cell(0, 10, f"Scan Options: {scan.scan_options or 'N/A'}")
            pdf.ln(3)

            pdf.set_font("Arial", style='B', size=12)
            pdf.cell(0, 10, "Scan Output:", ln=True)
            pdf.set_font("Arial", size=10)
            pdf.multi_cell(0, 8, scan.scan_output)

            findings = detect_findings(scan.scan_output)

            if findings:
                pdf.set_font("Arial", style='B', size=12)
                pdf.ln(4)
                pdf.cell(0, 10, "Detected Findings:", ln=True)
                pdf.set_font("Arial", size=10)
                for f in findings:
                    pdf.multi_cell(0, 8, f"- {f}")
            else:
                pdf.ln(4)
                pdf.set_font("Arial", style='I', size=10)
                pdf.cell(0, 10, "No major findings detected.", ln=True)

        pdf_output = BytesIO()
        pdf.output(pdf_output)
        pdf_output.seek(0)

        return send_file(pdf_output, as_attachment=True, download_name="scan_report.pdf", mimetype="application/pdf")

    # ✅ Always pass the form to template context
    return render_template("stage5.html", form=form)

def detect_findings(scan_output):
    findings = []

    patterns = {
        "Open Ports": r"(?i)(open\s+tcp|open\s+udp|Ports:?.*open)",
        "SQL Injection": r"(?i)(sql.*injection|sqli|sql error)",
        "Login Issues": r"(?i)(login\s+failed|incorrect\s+password|unauthorized|authentication\s+failed)",
        "XSS or Scripting": r"(?i)(cross.?site|xss|<script>)",
        "Server Errors": r"(?i)(5\d\d\s+error|internal\s+server\s+error|crash|segfault)",
        "Exposure": r"(?i)(leak|sensitive\s+data|exposed|publicly\s+accessible)",
        "Vulnerabilities": r"(?i)(vulnerable|cve-\d{4}-\d+|exploit|buffer\s+overflow)",
        "Configuration Issues": r"(?i)(default\s+credentials|directory\s+listing|misconfiguration|outdated)",
        "Warnings": r"(?i)(warning|deprecated|SSL certificate|expired)"
    }

    for label, regex in patterns.items():
        matches = re.findall(regex, scan_output)
        if matches:
            findings.append(f"{label}: {len(matches)} occurrence(s)")

    return findings
