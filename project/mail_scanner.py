import threading
import time
import socket
from imapclient import IMAPClient
from imapclient.exceptions import IMAPClientError
import pyzmail
from config import IMAP_HOST, IMAP_USER, IMAP_PASS, IMAP_SSL, IMAP_MAILBOX, MAIL_POLL_INTERVAL, UPI_PARTNER_EMAILS
from orders import find_pending_by_amount_and_payer, update_order
from fractions import release_fraction
from utils import extract_amount_and_payer

def start_imap_polling():
    def _poller():
        last_uid = None
        retry_delay = MAIL_POLL_INTERVAL
        print("[MailScanner] Starting mail scanner...")
        while True:
            try:
                with IMAPClient(IMAP_HOST, ssl=IMAP_SSL) as client:
                    client.login(IMAP_USER, IMAP_PASS)
                    client.select_folder(IMAP_MAILBOX)
                    all_uids = client.search(['ALL'])
                    if last_uid is None:
                        last_uid = max(all_uids) if all_uids else 0
                        print(f"[MailScanner] Ignoring past emails. Starting from UID {last_uid}")
                    new_uids = [uid for uid in all_uids if uid > last_uid]

                    for uid in new_uids:
                        try:
                            raw = client.fetch(uid, ["RFC822"])[uid][b"RFC822"]
                            msg = pyzmail.PyzMessage.factory(raw)
                            sender_email = msg.get_addresses('from')[0][1].lower()
                            if sender_email not in UPI_PARTNER_EMAILS:
                                client.add_flags(uid, [b"\\Seen"])
                                continue

                            body_text = ""
                            if msg.text_part:
                                body_text = msg.text_part.get_payload().decode(msg.text_part.charset or "utf-8", errors="ignore")
                            elif msg.html_part:
                                body_text = msg.html_part.get_payload().decode(msg.html_part.charset or "utf-8", errors="ignore")

                            amount, payer, txnid = extract_amount_and_payer(body_text)
                            if amount and payer:
                                rows = find_pending_by_amount_and_payer(round(amount, 2), payer)
                                for row in rows:
                                    matched_txn = row[0]
                                    update_order(matched_txn, {
                                        "status": "PAID",
                                        "matched_email_txn": txnid,
                                        "raw_email": body_text,
                                        "amount_received": amount,
                                        "payer_name": payer
                                    })
                                    release_fraction(row[1])
                                    print(f"[MailScanner] ✅ matched txn {matched_txn} amount={amount} payer={payer}")
                            else:
                                print("[MailScanner] ⚠️ Could not match regex in email body:")
                                print(body_text)

                            client.add_flags(uid, [b"\\Seen"])
                            last_uid = max(last_uid, uid)

                        except Exception as e:
                            print("[MailScanner] Mail parse error:", e)

                retry_delay = MAIL_POLL_INTERVAL  # reset retry delay after successful poll

            except (socket.error, OSError, IMAPClientError) as e:
                print(f"[MailScanner] IMAP connection error: {e}. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, 300)  # exponential backoff up to 5 min

            time.sleep(MAIL_POLL_INTERVAL)

    t = threading.Thread(target=_poller, daemon=True)
    t.start()
    return t
