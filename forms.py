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

    submit = SubmitField("Run Scan")
