# 🛡️ Pentesting Dashboard (Flask + MySQL)

A lightweight, self-hosted Python Flask web app that provides a dashboard to run common penetration testing tools like **Nmap**, **SQLMap**, and **OWASP ZAP**, and view scan results in a web browser.

---

## 🚀 Features

- Run scans from browser (Nmap, SQLMap, ZAP)
- Store scan output in MySQL
- View scan history with details
- Simple frontend (HTML, CSS, JS)
- No React or external APIs
- Self-hosted, runs on any Linux VM

---

## 🧐 Technologies Used

- **Python 3**
- **Flask** (Backend web server)
- **MySQL** (Database)
- **HTML + CSS + JS** (Frontend)
- **OWASP ZAP, Nmap, SQLMap** (Pentesting tools)
- **Flask-WTF** for forms
- **Flask-MySQLdb** for MySQL integration

---

## 🛆 Installation Guide (on fresh Linux VM)

### 1. Install base dependencies:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv mysql-server libmysqlclient-dev -y
```

### 2. Create project folder & virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python packages:

```bash
pip install -r requirements.txt
```

### 4. Clone or copy project files:

```bash
# If you're cloning:
git clone <your_repo_url>
cd pentesting-dashboard
```

---

## 🏃 How to Run the App

```bash
source venv/bin/activate
python run.py
```

Then open your browser at:  
`http://127.0.0.1:5000`

---

## 📺 Project Structure

```
pentesting-dashboard/
├── app.py
├── config.py
├── run.py
├── requirements.txt
├── README.md
├── templates/
├── static/
├── pentesting/
├── models/
├── routes/
```

---

## 📘 Full Project Summary & Planning

This is a self-hosted **Python Flask web application** that provides a dashboard interface to run various **penetration testing tools** (like **Nmap, SQLMap, and OWASP ZAP**) on a given target IP or URL. It saves scan history in a **MySQL database**, and uses basic **HTML, CSS, and JavaScript** for the frontend — no frameworks like React or Vue.

> Target Audience: Beginner-to-intermediate cybersecurity learners or testers who want a **local, browser-accessible pentesting environment**.

---

### 🪚 Project File Structure

```
pentesting-dashboard/
├── app.py
├── config.py
├── run.py
├── requirements.txt
├── README.md
├── templates/
├── static/
├── pentesting/
├── models/
├── routes/
```

---

### ⚙️ Python Libraries Used

```txt
Flask
Flask-MySQLdb
Flask-WTF
mysqlclient
python-dotenv
```

---

### 🗂️ Flask Routes

| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Landing page with scan form |
| `/scan` | POST | Handles scan form submission and runs selected tool |
| `/history` | GET | Shows scan history from MySQL |
| `/scan/<id>` | GET | Detailed result of a specific scan |
| `/clear-history` | POST | Deletes old scan data (optional feature) |

---

### 💃 Database Schema (MySQL)

#### Table: `scans`

| Column | Type | Description |
|--------|------|-------------|
| `id` | INT (PK) | Auto increment |
| `target` | VARCHAR(255) | Target IP or URL |
| `tool_used` | VARCHAR(50) | Nmap, SQLMap, ZAP |
| `scan_output` | TEXT | Raw scan output |
| `timestamp` | DATETIME | When scan was run |

---

### 🧬 Tool Wrappers in Python (`pentesting/`)

| Script | Tool | Command |
|--------|------|---------|
| `nmap_scan.py` | Nmap | `nmap -sV <target>` |
| `sqlmap_scan.py` | SQLMap | `sqlmap -u <target> --batch --level=1` |
| `zap_scan.py` | OWASP ZAP | CLI or API scan call |

---

### 💽 Module Responsibilities

- `app.py`: Main Flask setup, blueprint registration.
- `run.py`: Starts the app.
- `config.py`: DB & app configs (from `.env`).
- `models/`: DB connection and models.
- `routes/`: Route logic for dashboard & scans.
- `templates/`: HTML views for user interaction.
- `static/`: CSS, JS, and images.

---

### 💻 Scan Workflow

1. User visits `/` and inputs target + tool.
2. Flask handles the form via `/scan` POST.
3. The selected tool is run via `subprocess`.
4. Output is parsed and stored in MySQL.
5. `/history` shows scan results to user.

---

### 📀 Optional Future Enhancements

- Login authentication (Flask-Login)
- Export scans as PDF
- Email reports (SMTP)
- Celery task queuing for long scans
- Visual result rendering (e.g., Nmap port map)

---

### 🧑‍💻 Author Notes

This project is a practical penetration testing lab tool for small networks or web app targets. You can extend it with more tools or export features like PDF/Email alerts later.

