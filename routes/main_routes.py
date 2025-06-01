# routes/main_routes.py
from flask import Blueprint, render_template, request, redirect, url_for
from flask import request, send_file
from fpdf import FPDF
from io import BytesIO
import re
from forms import ScanForm
from forms import ReportForm
from models.scan import Scan
from app import db
from pentesting.nmap_scan import run_nmap_scan
from pentesting.sqlmap_scan import run_sqlmap_scan
from pentesting.zap_scan import run_zap_scan
from pentesting.whois_scan import run_whois_scan
from pentesting.dig_scan import run_dig_scan
from pentesting.nslookup_scan import run_nslookup_scan
from pentesting.theharvester_scan import run_theharvester_scan
from pentesting.nikto_scan import run_nikto_scan
from pentesting.hydra_scan import run_hydra_scan
from pentesting.netcat_scan import run_netcat
from pentesting.report_pdf import generate_pdf_report

main_routes = Blueprint('main_routes', __name__)

@main_routes.route('/', methods=["GET"])
def index():
    return render_template('index.html')

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
        print("Form submission failed:")
        print(form.errors)  # 👈 Debug form validation issues
        return "Invalid form submission", 400

    target = form.target.data
    tool = form.tool.data

    print("FORM SUBMITTED")
    print("Target:", target)
    print("Tool:", tool)

    output = ""

    if tool == 'nmap':
        options = request.form.getlist("nmap_options") or []
        output = run_nmap_scan(target, options)
    elif tool == 'sqlmap':
        # output = run_sqlmap_scan(target, form.sqlmap_options.data or [])
        options = request.form.getlist("sqlmap_options") or []
        print("SQLMap Options:", options)
        output = run_sqlmap_scan(target, options)
    elif tool == 'zap':
        output = run_zap_scan(target, form.zap_options.data or [])
    elif tool == 'theharvester':
        output = run_theharvester_scan(target, form.harvester_sources.data)
    elif tool == 'whois':
        output = run_whois_scan(target)
    elif tool == 'dig':
        output = run_dig_scan(target)
    elif tool == 'nslookup':
        output = run_nslookup_scan(target)
    elif tool == 'nikto':
        options = request.form.getlist("nikto_options") or []
        output = run_nikto_scan(target, options)
    elif tool == 'hydra':
        options = request.form.getlist("hydra_options") or []
        username = request.form.get("hydra_username")
        password = request.form.get("hydra_password")
        output = run_hydra_scan(target, username, password, options)
    elif tool == 'netcat':
        mode = request.form.get("netcat_mode")
        port = request.form.get("netcat_port")
        listener_ip = request.form.get("netcat_listener_ip") if mode == "reverse" else None

        output = run_netcat(target, port, mode, listener_ip)
    
    else:
        return "Unsupported tool", 400

    scan = Scan(target=target, tool_used=tool, scan_output=output)
    db.session.add(scan)
    db.session.commit()

    return redirect(url_for('main_routes.history'))

@main_routes.route("/fastscan", methods=["GET", "POST"])
def fast_scan():
    form = ScanForm()

    if request.method == "POST" and form.validate_on_submit():
        target = form.target.data

        if not target:
            return "No target specified", 400

        # ✅ Run Nmap scan with basic options
        nmap_output = run_nmap_scan(target, options=['-sS', '-O'])

        # ✅ Run Whois scan
        whois_output = run_whois_scan(target)

        # ✅ Combine outputs
        combined_output = f"--- Nmap Scan ---\n{nmap_output}\n\n--- Whois Info ---\n{whois_output}"

        # ✅ Save to database
        scan = Scan(target=target, tool_used='fast_scan', scan_output=combined_output)
        db.session.add(scan)
        db.session.commit()

        # ✅ Redirect to the history page
        return redirect(url_for('main_routes.history'))

    # ✅ GET request: render form without results
    return render_template("fastscan.html", form=form, result=None)


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


@main_routes.route('/stage1/nmap', methods=['GET'], endpoint='stage1_nmap')
def nmap_scan_page():
    form = ScanForm()
    form.nmap_options.data = []
    # form.tool.data = 'nmap'  # Pre-set tool value for this form
    return render_template('stage1/nmap.html', form=form)

@main_routes.route('/stage1/whois', methods=['GET', 'POST'], endpoint='stage1_whois')
def stage1_whois():
    form = ScanForm()
    return render_template('stage1/whois.html', form=form)

@main_routes.route('/stage1/dig', methods=['GET', 'POST'], endpoint='stage1_dig')
def stage1_dig():
    form = ScanForm()
    return render_template('stage1/dig.html', form=form)

@main_routes.route('/stage1/nslookup', methods=['GET', 'POST'], endpoint='stage1_nslookup')
def stage1_nslookup():
    form = ScanForm()
    return render_template('stage1/nslookup.html', form=form)

@main_routes.route('/stage1/theharvester', methods=['GET', 'POST'], endpoint='stage1_theharvester')
def stage1_theharvester():
    form = ScanForm()
    return render_template('stage1/theharvester.html', form=form)

@main_routes.route('/stage1', methods=['GET'], endpoint='stage1')
def stage1_index():
    return render_template('stage1/index.html')

@main_routes.route('/stage2/nmap', methods=['GET'], endpoint='stage2_nmap')
def stage2_nmap():
    form = ScanForm()
    # form.nmap_options.data = []  # Optional, to clear pre-selected
    return render_template('stage2/nmap.html', form=form)

@main_routes.route('/stage2/nikto', methods=['GET'], endpoint='stage2_nikto')
def stage2_nikto():
    form = ScanForm()
    form.nikto_options.data = []
    return render_template('stage2/nikto.html', form=form)

@main_routes.route('/stage2', methods=['GET'], endpoint='stage2')
def stage2_index():
    return render_template('stage2/index.html')

@main_routes.route('/stage3/sqlmap', methods=['GET'], endpoint='stage3_sqlmap')
def stage3_sqlmap():
    form = ScanForm()
    form.sqlmap_options.data = []
    return render_template('stage3/sqlmap.html', form=form)

@main_routes.route('/stage3/hydra', methods=['GET'], endpoint='stage3_hydra')
def stage3_hydra():
    form = ScanForm()
    return render_template('stage3/hydra.html', form=form)

@main_routes.route('/stage3', methods=['GET'], endpoint='stage3')
def stage3_index():
    return render_template('stage3/index.html')

@main_routes.route('/stage4/netcat', methods=['GET', 'POST'], endpoint='stage4_netcat')
def stage4_netcat():
    form = ScanForm()
    return render_template('stage4/netcat.html', form=form)

@main_routes.route('/stage4', methods=['GET'], endpoint='stage4')
def stage4_index():
    return render_template('stage4/index.html')

@main_routes.route('/stage5', methods=["GET", "POST"])
def stage5():
    scans = Scan.query.order_by(Scan.timestamp.desc()).all()
    form = ReportForm()

    form.scan_ids.choices = [
        (scan.id, f"{scan.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {scan.tool_used} on {scan.target}")
        for scan in scans
    ]

    if form.validate_on_submit():
        selected_ids = form.scan_ids.data
        selected_scans = Scan.query.filter(Scan.id.in_(selected_ids)).all()

        pdf_output = generate_pdf_report(selected_scans)

        return send_file(pdf_output, as_attachment=True, download_name="scan_report.pdf", mimetype="application/pdf")

    return render_template("stage5.html", form=form)
    # return render_template("404.html", form=form)
