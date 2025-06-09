import os
import subprocess
from datetime import datetime

# Configuration
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_dir = f"android_forensics_{timestamp}"
os.makedirs(output_dir, exist_ok=True)

def run_adb(command):
    return subprocess.run(["adb"] + command.split(), capture_output=True, text=True)

def pull_file(remote_path, local_path):
    run_adb(f"pull {remote_path} {local_path}")

def get_device_info():
    print("🔍 Getting device information...")
    info = run_adb("shell getprop")
    with open(os.path.join(output_dir, "device_info.txt"), "w") as f:
        f.write(info.stdout)

def list_installed_apps():
    print("📦 Listing installed apps...")
    apps = run_adb("shell pm list packages -f")
    with open(os.path.join(output_dir, "installed_apps.txt"), "w") as f:
        f.write(apps.stdout)

def pull_call_logs():
    print("📞 Pulling call logs (requires backup permissions)...")
    logs = run_adb("shell content query --uri content://call_log/calls")
    with open(os.path.join(output_dir, "call_logs.txt"), "w") as f:
        f.write(logs.stdout)

def pull_sms():
    print("💬 Pulling SMS messages (requires backup permissions)...")
    sms = run_adb("shell content query --uri content://sms")
    with open(os.path.join(output_dir, "sms_messages.txt"), "w") as f:
        f.write(sms.stdout)

def pull_internal_dirs():
    print("📁 Pulling directories (DCIM, WhatsApp, Downloads)...")
    for dir_name in ["DCIM", "Download", "WhatsApp"]:
        local_path = os.path.join(output_dir, dir_name)
        os.makedirs(local_path, exist_ok=True)
        pull_file(f"/sdcard/{dir_name}", local_path)

# Run all steps
print("🚀 Starting Android Forensic Collection...\n")
get_device_info()
list_installed_apps()
pull_call_logs()
pull_sms()
pull_internal_dirs()
print(f"\n✅ Forensic collection complete. Output saved in: {output_dir}")
