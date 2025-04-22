from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired
from wtforms.widgets import ListWidget, CheckboxInput

class ScanForm(FlaskForm):
    target = StringField("Target (IP or URL)", validators=[DataRequired()])
    tool = SelectField("Tool", choices=[
        ("nmap", "Nmap"),
        ("sqlmap", "SQLMap"),
        ("zap", "ZAP"),
        ("theharvester", "theHarvester"),
        ("whois", "Whois"),
        ("dig", "Dig"),
        ("nslookup", "Nslookup"),
        ("nikto", "Nikto"),
        ("hydra", "Hydra")
    ])

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
        "SQLMap Options",
        choices=[
            ("--batch", "Batch Mode (no prompts)"),
            ("--risk=3", "Risk Level 3"),
            ("--level=5", "Level 5"),
            ("--random-agent", "Use Random User-Agent"),
            ("--crawl=3", "Crawl depth 3")
        ],
        option_widget=CheckboxInput(),
        widget=ListWidget(prefix_label=False)
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
        ],
        validate_choice=False
    )

    nikto_options = SelectMultipleField(
        "Nikto Scan Options",
        choices=[
            ("-Display V", "Verbose Output (-Display V)"),
            ("-no404", "Ignore 404 responses (-no404)")
        ]
    )

    hydra_options = SelectMultipleField(
        "Hydra Options",
        choices=[
            ("-V", "Verbose Output (-V)"),
            ("-f", "Exit after first found login (-f)"),
            ("-t 4", "Parallel Tasks (-t 4)"),
            ("-s 22", "Custom Port (-s 22)")
        ],
        option_widget=CheckboxInput(),
        widget=ListWidget(prefix_label=False)
    )

    hydra_username = StringField("Username")
    hydra_password = StringField("Password")

    submit = SubmitField("Run Scan")

    def validate(self, extra_validators=None):
        initial_validation = super().validate(extra_validators)
        if not initial_validation:
            return False

        if self.tool.data == "theharvester" and not self.harvester_sources.data:
            self.harvester_sources.errors.append("Please select a data source for theHarvester.")
            return False

        return True
