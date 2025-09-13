import qrcode
import io
import base64

def generate_upi_uri(upi_id, amount, txn_id):
    return f"upi://pay?pa={upi_id}&pn=ReceiverName&am={amount:.2f}&cu=INR&tn={txn_id}"

def generate_qr_data_uri(upi_uri):
    qr = qrcode.QRCode(box_size=6, border=2)
    qr.add_data(upi_uri)
    qr.make(fit=True)
    img = qr.make_image()
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"data:image/png;base64,{b64}"
