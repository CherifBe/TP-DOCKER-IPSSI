from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL Connection
db_config = {
    'user': 'root',
    'password': 'password',
    'host': 'mysql',
    'port': 3306,
    'database': 'test_db'
}

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/data', methods=['GET'])
def data():
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM test_table;")
        rows = cursor.fetchall()
        return jsonify(rows), 200
    except mysql.connector.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
