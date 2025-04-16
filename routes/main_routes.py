# routes/main_routes.py
from flask import Blueprint, render_template, request, redirect, url_for
from forms import ScanForm
from models.scan import Scan
from app import db
from pentesting.nmap_scan import run_nmap_scan
from pentesting.sqlmap_scan import run_sqlmap_scan
from pentesting.zap_scan import run_zap_scan

main_routes = Blueprint('main_routes', __name__)

@main_routes.route('/', methods=["GET"])
def index():
    form = ScanForm()
    form.nmap_options.data = []
    return render_template('index.html', form=form)

@main_routes.route('/scan', methods=['POST'])
def scan():
    form = ScanForm()

    if not form.validate_on_submit():
        return "Invalid form submission", 400

    target = form.target.data
    tool = form.tool.data

    print("FORM SUBMITTED")
    print("Target:", target)
    print("Scan Type:", tool)

    output = ""

    if tool == 'nmap':
        nmap_option = form.nmap_options.data or ''
        output = run_nmap_scan(target, nmap_option)
    elif tool == 'sqlmap':
        output = run_sqlmap_scan(target)
    elif tool == 'zap':
        output = run_zap_scan(target)
    else:
        return "Unsupported tool", 400

    scan = Scan(target=target, tool_used=tool, scan_output=output)
    db.session.add(scan)
    db.session.commit()

    return redirect(url_for('main_routes.history'))

@main_routes.route('/history')
def history():
    scans = Scan.query.order_by(Scan.timestamp.desc()).all()
    return render_template('history.html', scans=scans)

@main_routes.route('/scan/<int:scan_id>')
def scan_detail(scan_id):
    scan = Scan.query.get_or_404(scan_id)
    return render_template('scan_detail.html', scan=scan)

@main_routes.route('/clear-history', methods=['POST'])
def clear_history():
    Scan.query.delete()
    db.session.commit()
    return redirect(url_for('main_routes.history'))
