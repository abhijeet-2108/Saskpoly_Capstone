# 🛡️ Pentesting Dashboard (Flask + SQLAlchemy)

A modular, self-hosted Flask-based dashboard to run and manage penetration testing tools in an organized way. Designed for students, security labs, and red teamers.

---

## 🌐 Overview

The Pentesting Dashboard now organizes tools into **Quick Scan** and **Deep Scan** categories, streamlining the workflow and enabling more targeted scanning and enumeration.

---

## 🚀 Current Features

* ✅ Run tools directly from the browser (including **Nmap**, **Whois**, **Nikto**, **Masscan**, **Gobuster**, **Wfuzz**, and more)
* ✅ View scan history with full output
* ✅ Store all results in MySQL via SQLAlchemy
* ✅ Dark/Light theme toggle
* ✅ Fully self-hosted (ideal for VMs, labs)
* ✅ Modular code structure for easy tool expansion

---

## 🛠️ Tools

### 🔹 Quick Scan

A streamlined scan for rapid insights.

* **Nmap** – Basic port scanning
* **Whois** – Domain information

### 🔹 Deep Scan

A comprehensive approach with two sets of tools:

**Reconnaissance Tools:**

* **Nmap** – Basic scans with options (`-sS`, `-O`, etc.)
* **Whois** – Detailed domain information
* **Dig**
* **Nslookup**
* **theHarvester**

**Scanning & Enumeration Tools:**

* **Nmap** – Advanced scanning options
* **Nikto** – Web server vulnerability scanner
* **Masscan** – Fast port scanning
* **Gobuster** – Directory and file brute-forcing
* **Wfuzz** – Content discovery and fuzzing

Each tool takes a target and optional command-line options as input.

---

## 🧹 Technologies Used

* **Python 3**
* **Flask** – Web backend
* **SQLAlchemy** – ORM for MySQL
* **MySQL** – Database for persistent scan results
* **HTML + CSS + Bootstrap** – UI Framework
* **Flask-WTF** – Form handling
* **Tools**: Nmap, Whois, Dig, Nslookup, theHarvester, Nikto, Masscan, Gobuster, Wfuzz

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
│   ├── index.html            # Home (Quick & Deep scans)
│   ├── history.html          # Scan history
│   ├── report.html           # Report viewer
│   ├── quickscan.html        # Quick Scan tool
│   └── deep_scan/
│       ├── reconnaissance.html
│       ├── scanning.html
│       └── tool-specific.html (if needed)
├── static/
│   └── css/style.css
├── routes/
│   └── main_routes.py
├── models/
│   └── scan_model.py
├── pentesting/
│   ├── nmap_scan.py
│   ├── whois_scan.py
│   ├── dig_scan.py
│   ├── nslookup_scan.py
│   ├── theharvester_scan.py
│   ├── nikto_scan.py
│   ├── masscan_scan.py
│   ├── gobuster_scan.py
│   └── wfuzz_scan.py
├── requirements.txt
├── README.md
```

---

## 📋 Routes (Current)

| Route                 | Method | Description                          |
| --------------------- | ------ | ------------------------------------ |
| `/`                   | GET    | Homepage with Quick/Deep scan cards  |
| `/quick-scan`         | GET    | Quick scan tool                      |
| `/deep-scan/recon`    | GET    | Reconnaissance tools                 |
| `/deep-scan/scanning` | GET    | Scanning & Enumeration tools         |
| `/scan`               | POST   | Handles scan logic and stores result |
| `/history`            | GET    | Shows all past scans                 |
| `/scan/<id>`          | GET    | Shows detailed scan report           |

---

## ⚙️ How it Works

1⃣ User inputs a target (and optional command options).
2⃣ Linux system runs the commands using Python subprocess.
3⃣ Results are stored in the MySQL database.
4⃣ Users can view the results in the **history** or **report viewer** pages.
5⃣ Reports can be viewed later from the database.

---

## 🔧 Installation Guide (Linux)

### 1. Install Base Packages

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv mysql-server libmysqlclient-dev -y
```

### 2. Clone & Set Up Project

```bash
git clone https://github.com/abhijeet-2108/Saskpoly_Capstone.git
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

| Field          | Type        | Description                   |
| -------------- | ----------- | ----------------------------- |
| `id`           | Integer     | Primary key                   |
| `target`       | String(255) | Target IP or URL              |
| `tool_used`    | String(50)  | Tool used (nmap, nikto, etc.) |
| `scan_options` | Text        | Command-line options used     |
| `scan_output`  | Text        | Raw terminal output           |
| `timestamp`    | DateTime    | Time of execution             |

---

## ✍️ Author Notes

Built as a capstone project for ethical hacking learners and lab environments. Designed for flexibility, extensibility, and real-world experimentation — this dashboard encourages hands-on exploration and skill-building.
