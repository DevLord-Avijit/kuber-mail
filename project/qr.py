import qrcode
import io
import base64

def generate_upi_uri(upi_id, amount, txn_id):
    # Input validation, but no signature/output change
    if not isinstance(upi_id, str) or "@" not in upi_id:
        raise ValueError("Invalid UPI ID format")
    try:
        amount = float(amount)
    except (ValueError, TypeError):
        raise ValueError("Amount must be a number")
    if amount <= 0:
        raise ValueError("Amount must be positive")
    if not txn_id:
        raise ValueError("Transaction ID must not be empty")
    return f"upi://pay?pa={upi_id}&pn=ReceiverName&am={amount:.2f}&cu=INR&tn={txn_id}"

def generate_qr_data_uri(upi_uri):
    try:
        qr = qrcode.QRCode(box_size=6, border=2)
        qr.add_data(upi_uri)
        qr.make(fit=True)
        img = qr.make_image()
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode()
        buf.close()
        return f"data:image/png;base64,{b64}"
    except Exception as e:
        raise RuntimeError(f"QR code generation failed: {e}")