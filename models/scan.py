# models/scan.py
from datetime import datetime
from app import db

class Scan(db.Model):
    __tablename__ = 'scans'

    id = db.Column(db.Integer, primary_key=True)
    target = db.Column(db.String(255), nullable=False)
    tool_used = db.Column(db.String(50), nullable=False)
    scan_options = db.Column(db.String(255), nullable=True)  # <-- new column
    scan_output = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# how to drop old tables and start new
# from app import db
# from models.scan import Scan

# db.drop_all()
# db.create_all()
# exit()
