from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)
CORS(app)

# E-posta ayarları
SENDER_EMAIL = os.environ.get('SENDER_EMAIL', '')
SENDER_PASSWORD = os.environ.get('SENDER_PASSWORD', '')
RECEIVER_EMAIL = os.environ.get('RECEIVER_EMAIL', '')

# SSL (465) üzerinden bağlantı ayarları
SMTP_SERVER = os.environ.get("SMTP_SERVER", "")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "465"))

@app.route('/send-email', methods=['POST'])
def send_email():
    if not request.is_json:
        return jsonify({"error": "İstek JSON formatında olmalıdır."}), 400

    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    service = data.get('service')
    message = data.get('message')

    if not all([name, email, phone, service, message]):
        return jsonify({"error": "Tüm alanlar zorunludur."}), 400

    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = f"İletişim Formu: {service} - {name}"

        body = f"Yeni bir mesaj:\n\nİsim: {name}\nE-posta: {email}\nTelefon: {phone}\nHizmet: {service}\nMesaj:\n{message}"
        msg.attach(MIMEText(body, 'plain'))

        # SMTP_SSL kullanarak güvenli bağlantı
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.set_debuglevel(0)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()

        return jsonify({"message": "E-posta başarıyla gönderildi!"}), 200

    except Exception as e:
        error_msg = f"Bağlantı Hatası: {str(e)}"
        print(error_msg)
        return jsonify({"error": error_msg}), 500

if __name__ == '__main__':
    app.run(debug=True)