from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class ScanForm(FlaskForm):
    target = StringField("Target (IP or URL)", validators=[DataRequired()])
    tool = SelectField("Tool", choices=[("nmap", "Nmap"), ("sqlmap", "SQLMap"), ("zap", "ZAP")])
    submit = SubmitField("Run Scan")
