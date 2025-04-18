# 🛡️ Pentesting Dashboard (Flask + SQLAlchemy)

A lightweight, self-hosted Python Flask web app that provides a dashboard to run common penetration testing tools like **Nmap**, **SQLMap**, and **OWASP ZAP**, and view scan results in a web browser.

---

## 🚀 Features

- Run scans via browser: Nmap, SQLMap, ZAP
- Custom scan options for each tool
- Store scan output in MySQL using SQLAlchemy
- View detailed scan history
- Dark/Light theme toggle
- Clean, responsive frontend (HTML, CSS, Bootstrap)
- No React or external APIs
- Fully self-hosted, ideal for VMs or labs

---

## 🧐 Technologies Used

- **Python 3**
- **Flask** – Backend web server
- **SQLAlchemy** – ORM to interact with MySQL
- **MySQL** – Persistent scan storage
- **HTML + CSS + Bootstrap** – Frontend
- **OWASP ZAP, Nmap, SQLMap** – Core pentesting tools
- **Flask-WTF** – Form handling

---

## 🔧 Required Tools

Make sure the following tools are installed on your system:

```bash
# Nmap
sudo apt install nmap -y

# SQLMap
git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git
sudo ln -s $(pwd)/sqlmap/sqlmap.py /usr/local/bin/sqlmap

# OWASP ZAP (zap-cli wrapper)
sudo snap install zaproxy --classic
pip install zap-cli
```

---

## 🔶 Installation Guide (on Fresh Linux VM)

### 1. Install Base Dependencies:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv mysql-server libmysqlclient-dev -y
```

### 2. Create Project Environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python Packages:

```bash
pip install -r requirements.txt
```

### 4. Clone the Project:

```bash
git clone <your_repo_url>
cd pentesting-dashboard
```

---

## 🌛 How to Run the App

The app runs on **port 80**. Use the following command to launch:

```bash
sudo env "PATH=$PATH" "PYTHONPATH=$PYTHONPATH" "VIRTUAL_ENV=$VIRTUAL_ENV" python run.py
```

Then open your browser at:  
👉 `http://127.0.0.1`

---

## 📁 Project Structure

```
pentesting-dashboard/
├── app.py
├── config.py
├── run.py
├── forms.py                # Flask-WTF forms and option logic
├── requirements.txt
├── README.md
├── templates/
│   ├── base.html
│   ├── index.html
│   └── history.html
├── static/
│   └── css/
│       └── style.css
├── pentesting/
│   ├── nmap_scan.py
│   ├── sqlmap_scan.py
│   └── zap_scan.py
├── models/
│   └── scan_model.py
├── routes/
│   └── main_routes.py
```

---

## 🌐 App Flow

1. User lands on `/` and submits a scan form.
2. Flask handles the scan via `/scan` POST route.
3. The selected tool runs using `subprocess`.
4. Output is stored in MySQL via SQLAlchemy.
5. Scan history is accessible via `/history`.

---

## 🧒 Flask Routes Summary

| Route           | Method | Description                          |
|----------------|--------|--------------------------------------|
| `/`            | GET    | Main form for launching a scan       |
| `/scan`        | POST   | Handles scan logic and stores result |
| `/history`     | GET    | Lists previous scans                 |
| `/scan/<id>`   | GET    | Shows full output of a specific scan |
| `/clear-history` | POST | Clears all scans (optional future)   |

---

## 🧰 Database (SQLAlchemy)

### Table: `scans`

| Column       | Type        | Description              |
|--------------|-------------|--------------------------|
| `id`         | Integer     | Primary key              |
| `target`     | String(255) | Target URL or IP         |
| `tool_used`  | String(50)  | nmap, sqlmap, zap        |
| `scan_output`| Text        | Raw output of the tool   |
| `timestamp`  | DateTime    | When scan was executed   |

---

## 🛠️ Tool Wrappers (`/pentesting/`)

| File            | Tool     | Sample Command                          |
|------------------|----------|------------------------------------------|
| `nmap_scan.py`   | Nmap     | `nmap -sV <target>`                     |
| `sqlmap_scan.py` | SQLMap   | `sqlmap -u <target> --batch --level=1` |
| `zap_scan.py`    | OWASP ZAP| `zap -cmd -quickurl <target>`          |

---

## 🎨 UI/UX Highlights

- Clean Bootstrap UI
- Option checkboxes for each tool
- All tool options toggle dynamically (JS)
- Dark/Light mode with toggle (via localStorage)
- Fully responsive and mobile friendly

---

## ⚙️ Python Dependencies

```txt
Flask
Flask-WTF
SQLAlchemy
mysqlclient
python-dotenv
```

---

## 🔮 Possible Future Upgrades

- Auth system (Flask-Login)
- Scan export (PDF, CSV)
- Scan scheduling
- Task queuing via Celery
- OSINT tool integrations
- Charts or visual result rendering

---

## ✍️ Author Notes

This app is built for ethical hacking students, red-team beginners, and pentest labs. It focuses on core tools, security learning, and practical results — no fluff.

