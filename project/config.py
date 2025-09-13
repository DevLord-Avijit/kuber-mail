import os
from dotenv import load_dotenv
load_dotenv()  # Load .env file

# ---------------- ENV CONFIG ----------------
ORDERS_FILE = os.environ.get("ORDERS_FILE", "orders.json")
LIVE_LIMIT = int(os.environ.get("LIVE_LIMIT", 100))
FRACTION_MIN = int(os.environ.get("FRACTION_MIN", 0))
FRACTION_MAX = int(os.environ.get("FRACTION_MAX", 99))
ORDER_TTL_SECONDS = int(os.environ.get("ORDER_TTL_SECONDS", 300))
MAIL_POLL_INTERVAL = int(os.environ.get("MAIL_POLL_INTERVAL", 10))

RECEIVER_UPI_ID = os.environ.get("RECEIVER_UPI_ID")
UPI_PARTNER_EMAILS = os.environ.get("UPI_PARTNER_EMAILS", "").split(",")

IMAP_HOST = os.environ.get("IMAP_HOST")
IMAP_USER = os.environ.get("IMAP_USER")
IMAP_PASS = os.environ.get("IMAP_PASS")
IMAP_SSL  = os.environ.get("IMAP_SSL", "True").lower() == "true"
IMAP_MAILBOX = os.environ.get("IMAP_MAILBOX", "INBOX")
