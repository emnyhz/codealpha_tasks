from flask import Flask, request, jsonify
import ast
import hashlib
import ipaddress
import operator
import os
import secrets
import sqlite3


app = Flask(__name__)

# Load the secret from an environment variable.
# A temporary secure value is generated if one is not provided.
app.config["SECRET_KEY"] = (
    os.environ.get("FLASK_SECRET_KEY") or secrets.token_hex(32)
)


def create_database():
    connection = sqlite3.connect("secure_users.db")
    cursor = connection.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users "
        "(id INTEGER PRIMARY KEY, username TEXT)"
    )

    cursor.execute(
        "INSERT OR IGNORE INTO users (id, username) VALUES (?, ?)",
        (1, "admin")
    )

    connection.commit()
    connection.close()


@app.route("/")
def home():
    return jsonify(
        {
            "project": "CodeAlpha Secure Coding Review",
            "version": "Secure Demo Application"
        }
    )


@app.route("/hash")
def secure_hash():
    value = request.args.get("value", "")

    if not value or len(value) > 256:
        return jsonify({"error": "Invalid input"}), 400

    hashed_value = hashlib.sha256(value.encode()).hexdigest()

    return jsonify({"sha256": hashed_value})


ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv
}


def safe_calculate(expression):
    tree = ast.parse(expression, mode="eval")

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)

        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Only numbers are allowed")

        if isinstance(node, ast.BinOp):
            operation = ALLOWED_OPERATORS.get(type(node.op))

            if operation is None:
                raise ValueError("Operator is not allowed")

            return operation(
                evaluate(node.left),
                evaluate(node.right)
            )

        raise ValueError("Invalid expression")

    return evaluate(tree)


@app.route("/calculate")
def calculate():
    expression = request.args.get("expression", "0")

    if len(expression) > 100:
        return jsonify({"error": "Expression is too long"}), 400

    try:
        result = safe_calculate(expression)
        return jsonify({"result": result})

    except (ValueError, SyntaxError, ZeroDivisionError):
        return jsonify({"error": "Invalid expression"}), 400


@app.route("/user")
def find_user():
    username = request.args.get("username", "")

    if not username or len(username) > 50:
        return jsonify({"error": "Invalid username"}), 400

    connection = sqlite3.connect("secure_users.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, username FROM users WHERE username = ?",
        (username,)
    )

    result = cursor.fetchall()
    connection.close()

    return jsonify({"users": result})


@app.route("/validate-host")
def validate_host():
    host = request.args.get("host", "")

    try:
        validated_ip = ipaddress.ip_address(host)

    except ValueError:
        return jsonify({"error": "Invalid IP address"}), 400

    return jsonify(
        {
            "host": str(validated_ip),
            "status": "Valid IP address"
        }
    )


if __name__ == "__main__":
    create_database()
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )