# 'G'rab 🔍

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Termux%20%7C%20iOS-lightgrey.svg)](https://github.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**'G'rab** is a modular command-line intelligence and email forensic suite designed for security researchers, red-team operators, and OSINT investigators. It bridges the gap between passive identity footprint enumeration and raw email header forensics to map digital footprints across Linux, Android (Termux), and iOS terminal environments.

---

## 🛠️ Project Architecture

```text
Grab/
├── core/
│   ├── __init__.py
│   ├── headers.py      # Email header parser, hop tracer, & authentication validator
│   ├── osint.py        # Public registry & footprint enumeration module
│   └── github_deep.py  # Deep GitHub metadata & commit author scraper
└── main.py             # CLI entrypoint and workflow orchestrator
```

---

## ✨ Features

- **Email Header Forensics (`headers.py`)**:
  - Parses raw `.eml` files to extract metadata (`Subject`, `From`, `To`, `Date`).
  - Traces Mail Transfer Agent (MTA) routing hops via `Received:` headers to isolate relay IPs.
  - Validates email security hygiene (**SPF**, **DKIM**, and **DMARC**).
- **Passive OSINT Footprinting (`osint.py`)**:
  - Queries public developer and profile registries using target email hashes.
  - Gravatar profile mapping (display names, bios, profile links).
  - GitHub account discovery via email search hooks.
  - Keybase cryptographic identity lookup.
- **Deep GitHub Asset Reconnaissance (`github_deep.py`)**:
  - Extracts rich profile metadata (Name, Company, Location, Bio, Website, Repositories).
  - Audits recent repository commits to scrape author display names and **leaked secondary/personal email addresses**.

---

## 🚀 Installation

Clone the repository and set up your environment:

```bash
# Clone the repository
git clone https://github.com/your-username/Grab.git

# Navigate into the project directory
cd Grab

# Ensure execution permissions (optional)
chmod +x main.py
```

---

## 💻 Usage Guide

### 1. General Help Menu
Display available options, flags, and help documentation:
```bash
python3 main.py -h
```

### 2. Email Address OSINT Reconnaissance
Scan a target email address across public profile registries and developer platforms:
```bash
python3 main.py -e target@gmail.com
```

### 3. Deep GitHub Asset Inspection
Drill down into a specific developer handle discovered during OSINT reconnaissance to pull corporate affiliations, locations, and commit signature emails:
```bash
python3 main.py -g target-username
```

### 4. Raw Email Header Forensics
Analyze a downloaded `.eml` file to trace routing hops and security authentication tokens:
```bash
python3 main.py -f path/to/email.eml
```

---

## 📱 Mobile Compatibility (Termux / iOS)
'G'rab is optimized to run smoothly in mobile terminal simulators:
- **Android (Termux):** Runs out of the box with standard Python 3.
- **iOS (Terminus / Pythonista):** Fully compatible via standard SSH terminal execution.

---

## ⚠️ Security & Operational Disclaimer
This tool is built strictly for authorized security research, forensic investigations, and educational purposes. The authors assume no liability and are not responsible for misuse or unauthorized data collection.

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.