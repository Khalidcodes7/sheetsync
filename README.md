# SheetSync

> Sync local CSV data directly to Google Sheets using Python.

[![CI](https://github.com/Khalidcodes7/sheetsync/actions/workflows/ci.yml/badge.svg)](https://github.com/Khalidcodes7/sheetsync/actions)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**SheetSync** is a Python automation tool that takes local CSV files and pushes their contents directly into a Google Sheet. It uses the official Google Sheets API to instantly update cloud documents.

---

## ✨ Features

- ☁️ **Direct Cloud Sync** — Push data straight to Google Sheets, no more emailing Excel files.
- 🔐 **Service Account Auth** — Uses Google Cloud Service Accounts for secure, headless authentication.
- 📊 **Pandas Integration** — Reads complex CSVs and handles missing data smoothly.
- 🖥️ **CLI & Python API** — Easy to run from the terminal or integrate into your own scripts.
- 🧪 **Tested** — Mocked unit tests guarantee the sync logic works.

---

## 📦 Installation

```bash
git clone https://github.com/Khalidcodes7/sheetsync.git

cd sheetsync
pip install -e ".[dev]"

