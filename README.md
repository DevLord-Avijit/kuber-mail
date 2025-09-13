
# Kuber Mail

## Introduction

**Kuber Mail** is a lightweight, email-driven payment gateway that allows businesses, freelancers, or individuals to **accept UPI payments without maintaining a traditional bank account or API integration**.

Unlike conventional payment gateways that require bank APIs, merchant accounts, or payment SDKs, Kuber Mail works by:

1. Generating **unique payment orders** with fractional amounts.
2. **Scanning a configured email inbox** for partner payment notifications.
3. **Automatically matching received payments** to pending orders.

This makes Kuber Mail ideal for **small businesses, freelancers, informal services**, or anyone looking for a simple, automated, and secure way to receive UPI payments.

---

## Key Features

| Feature                       | Description                                                                               |
| ----------------------------- | ----------------------------------------------------------------------------------------- |
| **UPI Payments via Email**    | Payments are tracked by scanning partner emails instead of connecting to bank APIs.       |
| **Unique Fractional Amounts** | Each payment order has a small fraction added to distinguish payments of the same amount. |
| **QR Code Generation**        | Each order generates a UPI QR code for instant scanning and payment.                      |
| **Order Tracking**            | Track orders with statuses: PENDING, PAID, EXPIRED.                                       |
| **Automatic Expiration**      | Orders automatically expire after a configurable TTL.                                     |
| **Threaded IMAP Polling**     | Real-time email scanning for payment confirmations.                                       |
| **Environment Configurable**  | All keys, emails, UPI IDs, and limits are configurable via `.env`.                        |
| **Lightweight & Portable**    | Pure Python 3 implementation with minimal dependencies.                                   |

---

## How It Works

```text
[User] --> Create Order --> [Kuber Mail Backend]
                                |
                                v
                       Generates Full Amount + Fraction
                                |
                                v
                     Generates UPI QR Code & URI
                                |
                                v
                       Payer Scans QR & Pays
                                |
                                v
                     Email Notification Received
                                |
                                v
                     IMAP Polling & Payment Matching
                                |
                                v
                      Order Status Updated (PAID)
```

**Step-by-Step Flow:**

1. User creates a payment order via `/create_order` endpoint or web form.
2. System generates a **full amount** including a fractional value for uniqueness.
3. A **UPI URI and QR code** are generated for the payer to scan.
4. Payer sends money via UPI to the configured receiver ID.
5. Kuber Mail **polls the partner email inbox** using IMAP at regular intervals.
6. Emails are parsed, and payments are matched with pending orders based on **amount + payer name**.
7. Order status is updated to `PAID`, and fractions are released for reuse.

*Illustrative diagram showing the end-to-end flow.*

---

## Technical Backend Overview

The backend is modular and written in **Python 3**, using **Flask** and **IMAP email scanning**.

**Modules:**

| Module             | Purpose                                                                                  |
| ------------------ | ---------------------------------------------------------------------------------------- |
| `app.py`           | Main Flask app, defines routes, and starts the IMAP email scanner.                       |
| `orders.py`        | Handles order storage, retrieval, updates, and pending order management.                 |
| `fractions.py`     | Manages fractional values for differentiating multiple payments of the same base amount. |
| `qr_generator.py`  | Generates UPI payment URIs and QR codes.                                                 |
| `email_scanner.py` | Polls the configured IMAP inbox, parses emails, and matches payments.                    |
| `utils.py`         | Shared helper functions such as regex extraction and common utilities.                   |

**Backend Logic Highlights:**

* Threaded IMAP polling runs continuously to detect incoming payments.
* Each payment order is assigned a **fractional amount** for uniqueness.
* Orders are persisted in a JSON file (`orders.json` by default).
* Payments are automatically matched based on **payer name + amount** using regex parsing.
* Fractional amounts are **released** after payment confirmation or order expiration.

---

## API Endpoints

### Create a Payment Order

**POST** `/create_order`

**Payload:**

```json
{
  "amount": 1000.0,
  "expected_payer": "John Doe",
  "upi_id": "receiver@upi"   // optional, defaults to configured receiver UPI
}
```

**Response:**

```json
{
  "txn_id": "uuid-generated-id",
  "upi_uri": "upi://pay?pa=receiver@upi&pn=ReceiverName&am=1000.12&cu=INR&tn=uuid-generated-id",
  "qr_data_uri": "data:image/png;base64,...",
  "full_amount": "1000.12",
  "expires_at": "2025-09-13T12:34:56Z",
  "message": "Order created. Waiting for payment."
}
```

---

### Check Order Status

**GET** `/order/<txn_id>`

**Response:**

```json
{
  "txn_id": "uuid-generated-id",
  "base_amount": 1000.0,
  "full_amount": 1000.12,
  "fraction": 12,
  "expected_payer": "John Doe",
  "upi_id": "receiver@upi",
  "status": "PENDING",
  "created_at": "2025-09-13T12:00:00Z",
  "expires_at": "2025-09-13T12:05:00Z",
  "amount_received": null,
  "payer_name": null,
  "message": "Waiting for payment"
}
```

---

## Environment Variables (`.env`)

```
ORDERS_FILE=orders.json
LIVE_LIMIT=100
FRACTION_MIN=0
FRACTION_MAX=99
ORDER_TTL_SECONDS=300
MAIL_POLL_INTERVAL=10

RECEIVER_UPI_ID=receiver@upi
UPI_PARTNER_EMAILS=partner1@example.com,partner2@example.com

IMAP_HOST=imap.gmail.com
IMAP_USER=your-email@gmail.com
IMAP_PASS=your-app-password
IMAP_SSL=True
IMAP_MAILBOX=INBOX
```

---

## Running the Project

1. Clone the repository:

```bash
git clone https://github.com/DevLord-Avijit/kuber-mail.git
cd kuber-mail
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create `.env` with your configuration.

4. Start the Flask server:

```bash
python app.py
```

5. Access the web UI at [http://localhost:5000](http://localhost:5000)

---

## Future Improvements

* WebSocket notifications for **real-time frontend updates**.
* Database integration (PostgreSQL/MySQL) for persistent storage.
* Multi-partner email support with separate folders per partner.
* Admin dashboard for monitoring **live payments and reports**.

---

## License

MIT License


