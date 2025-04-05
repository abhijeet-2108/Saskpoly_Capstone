from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.scan import db, Scan
from pentesting.nmap_scan import run_nmap_scan
from pentesting.sqlmap_scan import run_sqlmap_scan
from pentesting.zap_scan import run_zap_scan

main_routes = Blueprint('main_routes', __name__)

@main_routes.route('/')
def index():
    return render_template('index.html')

@main_routes.route('/scan', methods=['POST'])
def scan():
    target = request.form.get('target')
    tool = request.form.get('tool')

    # Validate if target and tool are provided
    if not target or not tool:
        flash("Missing target or tool selection", "error")
        return redirect(url_for('main_routes.index'))

    # Run selected scan
    output = ""
    try:
        if tool == 'nmap':
            output = run_nmap_scan(target)
        elif tool == 'sqlmap':
            output = run_sqlmap_scan(target)
        elif tool == 'zap':
            output = run_zap_scan(target)
        else:
            flash("Unsupported tool selected", "error")
            return redirect(url_for('main_routes.index'))
    except Exception as e:
        flash(f"Error running the scan: {str(e)}", "error")
        return redirect(url_for('main_routes.index'))

    # Save scan details to DB
    try:
        scan_record = Scan(target=target, tool_used=tool, scan_output=output)
        db.session.add(scan_record)
        db.session.commit()
        flash("Scan completed successfully!", "success")
    except Exception as e:
        db.session.rollback()  # Rollback on error
        flash(f"Error saving scan to database: {str(e)}", "error")

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
    try:
        Scan.query.delete()
        db.session.commit()
        flash("Scan history cleared successfully.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error clearing scan history: {str(e)}", "error")
    return redirect(url_for('main_routes.history'))
