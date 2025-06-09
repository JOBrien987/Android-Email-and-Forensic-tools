# Email Tools Suite

A collection of Python-based forensic and productivity tools designed for handling email attachments, mobile device data, and file system analysis.

## 🧩 Tools Included

### 1. 📥 Email Attachment Parser
Parses Gmail inbox via IMAP to:
- Identify attachments
- Filter by type (e.g., PDFs)
- Download files to local directory
- (Planned) OCR & metadata extraction

### 2. 🧮 Duplicate File Finder
Finds duplicate files based on:
- File type
- Size similarity
- Metadata comparison (name, modified time)
- (Planned) Hash-based deep comparison

### 3. 🔍 Mobile Forensics Collector *(ADB-based)*
Automates forensic acquisition from Android devices:
- Device build info (`getprop`)
- Installed apps
- Call logs & SMS (`content://`)
- User files from `/sdcard/`
- (Planned) APK dump, SQLite parsing, timeline creation

## 🧠 Requirements
- Python 3.8+
- `imaplib`, `email`, `os`, `hashlib`, `adb` (for mobile)
- ADB installed for mobile dive
- Gmail app password or OAuth (for email parsing)

## 🚧 Limitations
- Android tools require ADB access and permissions
- No iOS support (yet)
- Encrypted app data (e.g., Signal) not accessible without root

## 🪪 License
[MIT License](LICENSE) – free to use, modify, and distribute with credit.

## 🤝 Contributions
Pull requests and issues welcome! Add features, improve performance, or report bugs.

