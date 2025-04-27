# 🛡️ Pentesting Dashboard (Flask + SQLAlchemy)

A modular, self-hosted Flask-based dashboard to run and manage penetration testing tools in an organized, stage-based workflow. Designed for students, security labs, and red teamers.

---

## 🌐 Overview

The Pentesting Dashboard organizes tools and techniques into **five key stages of penetration testing**, helping users plan, execute, and analyze their assessments effectively:

### 🔹 Pentesting Stages:

1. **Reconnaissance**
2. **Scanning & Enumeration**
3. **Gaining Access**
4. **Maintaining Access**
5. **Reporting**

Each stage will have a dedicated dashboard section with tools and custom configurations.

---

## 🚀 Current Features

- ✅ Run tools directly from the browser  (currently: **Nmap**, **SQLMap**, **WHOSIS Lookup**, **theHarvester**,**and many more**)
- ✅ View scan history with full output
- ✅ Store all results in MySQL via SQLAlchemy
- ✅ Dark/Light theme toggle
- ✅ Fully self-hosted (ideal for VMs, labs)
- ✅ Modular code structure for tool expansion

---

## 💠 Tools (Current & Future)

| Stage                | Current Tools        | Possible Future Additions                        |
|----------------------|----------------------|--------------------------------------------------|
| **Reconnaissance**   | nmap , Whois Lookup, Dig, NSLookup, theHarvester      | shodan, Amaas, Recon-ng           |
| **Scanning**         | Nmap, nikto                  | Dirb, Enum4linux, Masscan                 |
| **Gaining Access**   | SQLMap,Hydra               | Metasploit, XSS-Strike                    |
| **Maintaining Access** | *(Planned)*         | Netcat, Weevely, Reverse Shell Generators        |
| **Reporting**        | inbuilt reporting system          | *Dradis, PDF/Markdown Export, Reporting UI*        |

---

## 🧹 Technologies Used

- **Python 3**
- **Flask** – Web backend
- **SQLAlchemy** – ORM for MySQL
- **MySQL** – Database for persistent scan results
- **HTML + CSS + Bootstrap** – UI Framework
- **Flask-WTF** – Form Handling
- **Tools**: Nmap, SQLMap, whoislookup, dig, nslookup, theHarvester, nikto, hydra

---

## 📦 Project Structure

```
pentesting-dashboard/
├── app.py
├── config.py
├── run.py
├── forms.py                  # Flask-WTF logic
├── templates/
│   ├── base.html             # Common layout
│   ├── index.html            # Home (5-stage dashboard)
│   ├── history.html          # Scan history
│   └── stages/                # Each tool gets its own view
│       ├── nmap.html
│       ├── sqlmap.html
│       ├── whois.html
│       ├── dig.html
│       ├── nikto.html
│       └── theHarvester.html
├── static/
│   └── css/style.css
├── routes/
│   └── main_routes.py
├── models/
│   └── scan_model.py
├── pentesting/
│   ├── nmap_scan.py
│   ├── sqlmap_scan.py
│   ├── dig_scan.py
│   ├── hydra_scan.py
│   ├── nikto_scan.py
│   ├── whois_scan.py
│   └── theharvester_scan.py
├── requirements.txt
├── README.md
```

---

## 📋 Routes (Current)

| Route               | Method | Description                                 |
|--------------------|--------|---------------------------------------------|
| `/`                | GET    | Homepage showing pentest stage cards        |
| `/page1`           | GET    | Legacy form-based tool runner (to migrate)  |
| `/scan`            | POST   | Handles scan logic and stores result        |
| `/history`         | GET    | Shows all past scans                        |
| `/scan/<id>`       | GET    | Shows detailed scan result                  |
| `/clear-history`   | POST   | (Planned) Clears scan logs                  |
| `/stage1/nmap`      | GET    | Nmap tool UI                                |
| `/stage3/sqlmap`    | GET    | SQLMap tool UI                              |


---

## ⚙️ Tool Integration Details

### Nmap
```bash
nmap -sV <target>
```

### SQLMap
```bash
sqlmap -u <target> --batch --level=1
```

### OWASP ZAP (zap-cli)
```bash
zap-cli quick-scan --self-contained <target>
```

*Note: ZAP command execution integration is still under refinement.*

---

## 🔧 Installation Guide (Linux)

### 1. Install Base Packages
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv mysql-server libmysqlclient-dev -y
```

### 2. Clone & Set Up Project
```bash
git clone <your_repo_url>
cd pentesting-dashboard
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 💻 Run the App

```bash
sudo env "PATH=$PATH" "PYTHONPATH=$PYTHONPATH" "VIRTUAL_ENV=$VIRTUAL_ENV" python run.py
```

Visit: [http://127.0.0.1](http://127.0.0.1)

---

## 📚 Database Schema (`scans` table)

| Field         | Type        | Description                      |
|---------------|-------------|----------------------------------|
| `id`          | Integer     | Primary key                      |
| `target`      | String(255) | Target IP or URL                 |
| `tool_used`   | String(50)  | Tool used (nmap, sqlmap, etc.)   |
| `scan_options`| Text        | Command-line options used        |
| `scan_output` | Text        | Raw terminal output              |
| `timestamp`   | DateTime    | Time of execution                |

---

## 🌟 Future Roadmap

- 🔒 Authentication (Flask-Login)
- 📁 File upload support (for target lists)
- 📊 Visualization (charts, ports, severity)
- 📄 Export scan reports (Markdown → PDF)
- ⏱️ Schedule scans (with Celery or cron)
- 🧠 Add AI prompts for tool suggestions

---

## ✍️ Author Notes

Built as a capstone project for ethical hacking learners and lab environments. Designed with flexibility, extensibility, and simplicity in mind — this dashboard encourages curiosity, experimentation, and real-world skills.


<!-- Stage	Tools
Stage 1	nmap, whois, dig, nslookup, theHarvester
Stage 2	nmap -sV/-O, nikto
Stage 3	sqlmap, hydra
Stage 4	netcat, weevely
Stage 5	markdown2pdf, weasyprint -->