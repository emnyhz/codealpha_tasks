from flask import Flask, request, jsonify
import hashlib
import sqlite3
import subprocess


app = Flask(__name__)

# Intentionally insecure value for security review practice
SECRET_KEY = "codealpha-secret-key"
app.config["SECRET_KEY"] = SECRET_KEY


def create_database():
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users "
        "(id INTEGER PRIMARY KEY, username TEXT)"
    )

    cursor.execute(
        "INSERT OR IGNORE INTO users (id, username) VALUES (1, 'admin')"
    )

    connection.commit()
    connection.close()


@app.route("/")
def home():
    return jsonify(
        {
            "project": "CodeAlpha Secure Coding Review",
            "version": "Vulnerable Demo Application"
        }
    )


@app.route("/hash")
def weak_hash():
    value = request.args.get("value", "")
    hashed_value = hashlib.md5(value.encode()).hexdigest()

    return jsonify({"md5": hashed_value})


@app.route("/calculate")
def calculate():
    expression = request.args.get("expression", "0")
    result = eval(expression)

    return jsonify({"result": result})


@app.route("/user")
def find_user():
    username = request.args.get("username", "")

    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    query = f"SELECT id, username FROM users WHERE username = '{username}'"
    cursor.execute(query)

    result = cursor.fetchall()
    connection.close()

    return jsonify({"users": result})


@app.route("/ping")
def ping_host():
    host = request.args.get("host", "127.0.0.1")

    command = f"ping -n 1 {host}"
    output = subprocess.check_output(
        command,
        shell=True,
        text=True
    )

    return f"<pre>{output}</pre>"


if __name__ == "__main__":
    create_database()
    app.run(host="127.0.0.1", port=5000, debug=True)