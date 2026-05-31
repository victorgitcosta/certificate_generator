from dotenv import load_dotenv
load_dotenv()  # ← must come before os.environ
import csv
import os
import smtplib
from email.message import EmailMessage

print(f"USER: {os.environ.get('GMAIL_USER')}")
print(f"PASS: {os.environ.get('GMAIL_APP_PASS')}")

GMAIL_USER     = os.environ["GMAIL_USER"]
GMAIL_APP_PASS = os.environ["GMAIL_APP_PASS"]

CSV_FILE       = "attendes.txt"
PDF_OUTPUT_DIR = "certificates"

EMAIL_SUBJECT  = "Your Certificate"
EMAIL_BODY     = """\
Hi {name},

Please find your certificate attached.

Best regards,
Your Team
"""

# Column names in your CSV — adjust if different
NAME_COL  = "name"
HRS_COL = "hours"
EMAIL_COL = "email"
# ───────────────────────────────────────────────────────────────

def find_pdf_for(name: str, pdf_dir: str) -> str | None:
    """Return the PDF path whose filename contains the attendee's name."""
    for filename in os.listdir(pdf_dir):
        if filename.endswith(".pdf") and name.strip() in filename:
            return os.path.join(pdf_dir, filename)
    return None

#def find_pdf_for(name: str, pdf_dir: str) -> str | None:
#    """Return the PDF path whose filename contains the attendee's name."""
#    for filename in os.listdir(pdf_dir):
#        if filename.endswith(".pdf") and name.lower().replace(" ", "_") in filename.lower():
#            return os.path.join(pdf_dir, filename)
#    return None

def send_certificate(name: str, email: str, pdf_path: str) -> None:
    msg = EmailMessage()
    msg["From"]    = GMAIL_USER
    msg["To"]      = email
    msg["Subject"] = EMAIL_SUBJECT
    msg.set_content(EMAIL_BODY.format(name=name))

    with open(pdf_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="pdf",
            filename=os.path.basename(pdf_path),
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(GMAIL_USER, GMAIL_APP_PASS)
        smtp.send_message(msg)
        print(f"  ✓ Sent to {name} <{email}>")


def main():
    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name  = row[NAME_COL].strip()
            email = row[EMAIL_COL].strip()

            pdf_path = find_pdf_for(name, PDF_OUTPUT_DIR)
            if not pdf_path:
                print(f"  ✗ PDF not found for: {name} — skipping")
                continue

            try:
                send_certificate(name, email, pdf_path)
            except Exception as e:
                print(f"  ✗ Failed for {name}: {e}")


if __name__ == "__main__":
    # Optional: generate all PDFs first
    # import subprocess; subprocess.run(["python", "pdf_gen.py"], check=True)

    print("Sending certificates…")
    main()
    print("Done.")