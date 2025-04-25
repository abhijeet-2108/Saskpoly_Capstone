from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SubmitField
from wtforms.validators import DataRequired

class ReportForm(FlaskForm):
    scan_ids = SelectMultipleField("Select scans", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Generate PDF")
