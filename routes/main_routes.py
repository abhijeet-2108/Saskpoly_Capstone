# routes/main_routes.py
from flask import Blueprint, render_template, request, redirect, url_for
from forms import ScanForm
from models.scan import Scan
from app import db
from pentesting.nmap_scan import run_nmap_scan
from pentesting.sqlmap_scan import run_sqlmap_scan
from pentesting.zap_scan import run_zap_scan
from pentesting.whois_scan import run_whois_scan
from pentesting.dig_scan import run_dig_scan
from pentesting.nslookup_scan import run_nslookup_scan
from pentesting.theharvester_scan import run_theharvester_scan

main_routes = Blueprint('main_routes', __name__)

@main_routes.route('/', methods=["GET"])
def index():
    form = ScanForm()
    form.nmap_options.data = []
    form.sqlmap_options.data = []
    form.zap_options.data = []
    return render_template('index.html', form=form)

@main_routes.route('/page1', methods=["GET"])
def page1():
    form = ScanForm()
    form.nmap_options.data = []
    form.sqlmap_options.data = []
    form.zap_options.data = []
    return render_template('page1.html', form=form)

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
    # elif tool == 'sqlmap':
    #     output = run_sqlmap_scan(target)
    elif tool == "sqlmap":
        selected_options = form.sqlmap_options.data
        output = run_sqlmap_scan(target, selected_options)
    elif tool == 'zap':
        selected_options = form.zap_options.data
        output = run_zap_scan(target, selected_options)
    elif tool == 'whois':  # ✅ New block
        output = run_whois_scan(target)
    elif tool == 'dig':
        output = run_dig_scan(target)
    elif tool == 'nslookup':
        output = run_nslookup_scan(target)
    elif tool == 'theharvester':
        source = form.harvester_sources.data
        output = run_theharvester_scan(target, source)

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


@main_routes.route('/stage1/nmap', methods=['GET'])
def nmap_scan_page():
    form = ScanForm()
    form.nmap_options.data = []
    form.tool.data = 'nmap'  # Pre-set tool value for this form
    return render_template('stage1/nmap.html', form=form)

@main_routes.route('/stage1/whois', methods=['GET', 'POST'])
def stage1_whois():
    form = ScanForm()
    return render_template('stage1/whois.html', form=form)

@main_routes.route('/stage1/dig', methods=['GET', 'POST'])
def stage1_dig():
    form = ScanForm()
    return render_template('stage1/dig.html', form=form)

@main_routes.route('/stage1/nslookup', methods=['GET', 'POST'])
def stage1_nslookup():
    form = ScanForm()
    return render_template('stage1/nslookup.html', form=form)

@main_routes.route('/stage1/theharvester', methods=['GET', 'POST'])
def stage1_theharvester():
    form = ScanForm()
    return render_template('stage1/theharvester.html', form=form)

@main_routes.route('/stage1', methods=['GET'])
def stage1_index():
    return render_template('stage1/index.html')
