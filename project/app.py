from flask import Flask
from flask_cors import CORS
from mail_scanner import start_imap_polling
from routes import register_routes

app = Flask(__name__)
CORS(app)
register_routes(app)

if __name__ == "__main__":
    start_imap_polling()
    app.run(host="0.0.0.0", port=5000, debug=True)
