# 💸 Kuber Mail 

**Kuber Mail** is a lightweight, email-driven payment gateway that lets businesses, freelancers, or anyone **accept UPI payments without needing a bank account or API integration**.

Forget the hassle of connecting to banks, handling APIs, or complex payment SDKs. Kuber Mail works by:

1. Generating **unique payment orders** with tiny fractional amounts.
2. **Scanning a configured email inbox** for partner payment notifications.
3. **Automatically matching received payments** to pending orders.

Perfect for **small businesses, freelancers, or informal services** looking for a **simple, automated, and secure payment solution**.

---

## ✨ Key Features

| Feature                       | Why It Rocks                                                        |
| ----------------------------- | ------------------------------------------------------------------- |
| **UPI Payments via Email**    | Track payments via email—no bank APIs required.                     |
| **Unique Fractional Amounts** | Add tiny fractions to amounts to easily distinguish payments.       |
| **QR Code Generation**        | Each order gets its own UPI QR code for instant payment scanning.   |
| **Order Tracking**            | See statuses: `PENDING`, `PAID`, `EXPIRED`.                         |
| **Automatic Expiration**      | Orders automatically expire after a set time (TTL).                 |
| **Threaded IMAP Polling**     | Continuously scans emails for payment confirmations.                |
| **Environment Configurable**  | All settings (emails, UPI IDs, limits) are configurable via `.env`. |
| **Lightweight & Portable**    | Runs on pure Python 3 with minimal dependencies.                    |

---

## 🛠 How It Works

```text
[User] --> Create Order --> [Kuber Mail Backend]
                                |
                                v
                       Adds Fraction to Amount
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

1. Create a payment order via `/create_order` or web form.
2. Kuber Mail generates the **full amount** (base + fractional).
3. A **UPI URI and QR code** are created for the payer.
4. Payer sends money via UPI.
5. Kuber Mail polls your **email inbox** using IMAP.
6. Payment emails are parsed and matched with pending orders.
7. Order status updates to `PAID`, and fractions are released for reuse.

> 💡 Tip: Each fractional amount ensures you can distinguish payments even if multiple payers send the same base amount.

---

## 🖥 Technical Backend Overview

Built in **Python 3**, Kuber Mail uses **Flask** for APIs and **IMAP scanning** for emails.

**Modules at a glance:**

| Module             | Purpose                                            |
| ------------------ | -------------------------------------------------- |
| `app.py`           | Main Flask app + IMAP scanner.                     |
| `orders.py`        | Manage orders (store, retrieve, update).           |
| `fractions.py`     | Handle fractional amounts for uniqueness.          |
| `qr_generator.py`  | Generate UPI URIs & QR codes.                      |
| `email_scanner.py` | Poll IMAP inbox, parse emails, and match payments. |
| `utils.py`         | Helper functions (regex, utilities, etc).          |

**Backend Highlights:**

* Threaded IMAP polling detects incoming payments in real-time.
* Orders have **unique fractional amounts**.
* All orders are stored in a JSON file (`orders.json`).
* Payments are matched automatically via **amount + payer name** regex.
* Fractions are released once payments are confirmed or orders expire.

---

## 📡 API Endpoints

### Create a Payment Order

**POST** `/create_order`

**Payload Example:**

```json
{
  "amount": 1000.0,
  "expected_payer": "John Doe",
  "upi_id": "receiver@upi" // optional, defaults to configured receiver UPI
}
```

**Response Example:**

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

**Response Example:**

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

## ⚙ Environment Variables (`.env`)

```env
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

## 🏃 Running the Project

```bash
git clone https://github.com/DevLord-Avijit/kuber-mail.git
cd kuber-mail
pip install -r requirements.txt
```

Create your `.env` file, then:

```bash
python app.py
```

Open your browser: [http://localhost:5000](http://localhost:5000) 🚀

---

## 🌟 Future Improvements

* WebSocket notifications for **live updates**
* Database integration (PostgreSQL/MySQL)
* Multi-partner email support with separate folders
* Admin dashboard for monitoring **live payments & reports**

---

## 📜 License

MIT License


