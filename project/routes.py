from flask import request, jsonify, render_template
from orders import store_order, get_order, count_pending
from fractions import pick_fraction, release_fraction
from qr import generate_upi_uri, generate_qr_data_uri
from config import LIVE_LIMIT, ORDER_TTL_SECONDS, RECEIVER_UPI_ID
from datetime import datetime, timedelta, timezone
import uuid
import threading

def register_routes(app):

    @app.route("/create_order", methods=["POST"])
    def create_order_endpoint():
        data = request.json or {}
        try:
            base_amount = float(data.get("amount",0))
        except:
            return jsonify({"error":"invalid amount"}), 400
        expected_payer = (data.get("expected_payer") or "").strip()
        upi_id = data.get("upi_id") or RECEIVER_UPI_ID

        if base_amount <=0 or not expected_payer:
            return jsonify({"error":"invalid payload"}), 400

        if count_pending() >= LIVE_LIMIT:
            return jsonify({"error":"server busy, try later"}), 429

        frac = pick_fraction()
        if frac is None:
            return jsonify({"error":"no fraction available"}), 429

        full_amount = round(base_amount + (frac/100.0),2)
        txn_id = str(uuid.uuid4())
        created_at = datetime.now(timezone.utc)
        expires_at = created_at + timedelta(seconds=ORDER_TTL_SECONDS)

        upi_uri = generate_upi_uri(upi_id, full_amount, txn_id)
        qr_data = generate_qr_data_uri(upi_uri)

        order = {
            "txn_id": txn_id,
            "base_amount": base_amount,
            "full_amount": full_amount,
            "fraction": frac,
            "expected_payer": expected_payer,
            "upi_id": upi_id,
            "status": "PENDING",
            "created_at": created_at.isoformat(),
            "expires_at": expires_at.isoformat(),
            "matched_email_txn": None,
            "raw_email": None,
            "amount_received": None,
            "payer_name": None
        }
        store_order(order)

        def expire_order(txn, f):
            import time
            time.sleep(ORDER_TTL_SECONDS)
            o = get_order(txn)
            if o and o["status"] == "PENDING":
                from orders import update_order
                update_order(txn, {"status":"EXPIRED"})
                release_fraction(f)
                print(f"[Order Expired] txn={txn}")
        threading.Thread(target=expire_order, args=(txn_id, frac), daemon=True).start()

        return jsonify({
            "txn_id": txn_id,
            "upi_uri": upi_uri,
            "qr_data_uri": qr_data,
            "full_amount": f"{full_amount:.2f}",
            "expires_at": expires_at.isoformat(),
            "message": "Order created. Waiting for payment."
        }), 201

    @app.route("/order/<txn_id>", methods=["GET"])
    def order_status(txn_id):
        o = get_order(txn_id)
        if not o:
            return jsonify({"error":"not found"}), 404

        amount_received = o['amount_received'] if o['amount_received'] is not None else 0.00
        payer_name = o['payer_name'] if o['payer_name'] else "Unknown"

        msg_map = {
            "PENDING": "Waiting for payment ⏳",
            "PAID": f"Payment received ✅ Amount: ₹{amount_received:.2f}, Payer: {payer_name}",
            "EXPIRED": "Payment time expired ⏰"
        }
        message = msg_map.get(o["status"], "Unknown status")
        return jsonify({**o, "message": message})

    @app.route('/')
    def index():
        return render_template('index.html')
