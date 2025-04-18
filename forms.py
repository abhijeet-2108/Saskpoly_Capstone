from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired

class ScanForm(FlaskForm):
    target = StringField("Target (IP or URL)", validators=[DataRequired()])
    tool = SelectField("Tool", choices=[("nmap", "Nmap"), ("sqlmap", "SQLMap"), ("zap", "ZAP")])

    # Nmap options - values are actual CLI flags, labels are user-friendly
    nmap_options = SelectMultipleField(
        "Nmap Scan Options",
        choices=[
            ("-sS", "Stealth Scan (-sS)"),
            ("-O", "OS Detection (-O)"),
            ("-sV", "Version Detection (-sV)"),
            ("-Pn", "Skip Host Discovery (-Pn)")
        ]
    )
    # SQLmao optoins
    sqlmap_options = SelectMultipleField(
    "SQLMap Scan Options",
        choices=[
            ("--batch", "Non-interactive Mode (--batch)"),
            ("--crawl=1", "Crawl Level (--crawl=1)"),
            ("--level=3", "Level of Tests (--level=3)"),
            ("--risk=2", "Risk Level (--risk=2)"),
            ("--dump", "Dump DB Contents (--dump)")
        ]
    )
    # ZAP options
    zap_options = SelectMultipleField(
    "ZAP Scan Options",
        choices=[
            ("-quick", "Quick Scan (-quick)"),
            ("-full", "Full Scan (-full)"),
            ("-ajax", "AJAX Spider (-ajax)"),
            ("-passive", "Passive Scan Only (-passive)"),
            ("-report", "Generate Report (-report)")
        ]
    )

    submit = SubmitField("Run Scan")
