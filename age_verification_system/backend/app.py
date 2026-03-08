from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime, date

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return jsonify({
        "message": "Age Verification API is running"
    })


# Calculate age from DOB
def calculate_age(dob):

    birth = datetime.strptime(dob, "%Y-%m-%d").date()
    today = date.today()

    age = today.year - birth.year - (
        (today.month, today.day) < (birth.month, birth.day)
    )

    return age


def get_user(uid):

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT fingerprint, dob FROM users WHERE user_id=?",
        (uid,)
    )

    row = cursor.fetchone()

    conn.close()

    if row:

        fingerprint = row[0]
        dob = row[1]

        age = calculate_age(dob)

        return {
            "fingerprint": fingerprint,
            "age": age
        }

    return None


@app.route("/verify-user", methods=["POST"])
def verify_user():

    data = request.json

    uid = data.get("user_id")
    fingerprint = data.get("fingerprint")

    user = get_user(uid)

    if not user:
        return jsonify({
            "status": "failed",
            "message": "UID not found"
        })

    if fingerprint != user["fingerprint"]:
        return jsonify({
            "status": "failed",
            "message": "Fingerprint mismatch"
        })

    if user["age"] < 18:
        return jsonify({
            "status": "failed",
            "message": "User is underage"
        })

    return jsonify({
        "status": "verified"
    })


if __name__ == "__main__":
    app.run(debug=True)