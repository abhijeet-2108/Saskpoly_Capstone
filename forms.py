from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired

class ScanForm(FlaskForm):
    target = StringField("Target (IP or URL)", validators=[DataRequired()])
    tool = SelectField("Tool", choices=[("nmap", "Nmap"), ("sqlmap", "SQLMap"), ("zap", "ZAP"), ("theharvester", "theHarvester")])

    nmap_options = SelectMultipleField(
        "Nmap Scan Options",
        choices=[
            ("-sS", "Stealth Scan (-sS)"),
            ("-O", "OS Detection (-O)"),
            ("-sV", "Version Detection (-sV)"),
            ("-Pn", "Skip Host Discovery (-Pn)")
        ]
    )

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

    harvester_sources = SelectField(
        "Data Source",
        choices=[
            ("google", "Google"),
            ("bing", "Bing"),
            ("crtsh", "crt.sh"),
            ("linkedin", "LinkedIn"),
            ("twitter", "Twitter"),
        ]
    )

    submit = SubmitField("Run Scan")

    def validate(self, extra_validators=None):
        """Dynamically validate based on the tool selected."""
        initial_validation = super().validate(extra_validators)
        if not initial_validation:
            return False

        if self.tool.data == "theharvester" and not self.harvester_sources.data:
            self.harvester_sources.errors.append("Please select a data source for theHarvester.")
            return False

        return True
