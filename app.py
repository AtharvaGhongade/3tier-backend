import os
import mysql.connector
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=['https://icy-field-088b46d00.7.azurestaticapps.net'])

def get_db_connection():
    return mysql.connector.connect(
        host=os.environ['DB_HOST'],
        port=int(os.environ.get('DB_PORT', 3306)),
        database=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASS'],
        ssl_ca='/etc/ssl/certs/ca-certificates.crt',
        ssl_verify_cert=True
    )

@app.route('/health')
def health():
    return jsonify({'status': 'ok'}), 200

@app.route('/api/data')
def get_data():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT NOW() as server_time')
    result = cursor.fetchone()
    conn.close()
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
