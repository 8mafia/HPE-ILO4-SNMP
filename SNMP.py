import subprocess

# فایل حاوی لیست آی‌پی‌های iLO
IP_FILE = "ilo_ips.txt"
ILO_USERNAME = "administrator"
ILO_PASSWORD = "You'pass"

# خواندن لیست آی‌پی‌ها از فایل
with open(IP_FILE, "r") as file:
    ilo_ips = [line.strip() for line in file if line.strip()]

for ilo_ip in ilo_ips:
    print(f"[INFO] در حال ارسال درخواست به {ilo_ip}...")

    curl_cmd = [
        "curl", "-k", "-u", f"{ILO_USERNAME}:{ILO_PASSWORD}", "-X", "PATCH",
        f"https://{ilo_ip}/rest/v1/Managers/1/SnmpService",
        "-H", "Content-Type: application/json",
        "-d", '{"Users": [{"SecurityName": "security", "AuthProtocol": "MD5", "AuthPassphrase": "PAss", "PrivacyProtocol": "DES", "PrivacyPassphrase": "Pass"}]}',
        "--connect-timeout", "3",  # تایم‌اوت اتصال ۵ ثانیه
        "--max-time", "2"  # حداکثر زمان برای دریافت پاسخ ۱۰ ثانیه
    ]

    # اجرای دستور curl
    result = subprocess.run(curl_cmd, capture_output=True, text=True)

    # بررسی نتیجه
    if "Base.0.10.Success" in result.stdout:
        print(f"[SUCCESS] تغییرات روی {ilo_ip} با موفقیت انجام شد! 🚀")
    elif "Couldn't connect" in result.stderr or "Failed to connect" in result.stderr:
        print(f"[ERROR] عدم دسترسی به {ilo_ip} (Timeout). رفتن به آی‌پی بعدی...")
    else:
        print(f"[ERROR] خطا در درخواست برای {ilo_ip}:")
        print(result.stderr)

