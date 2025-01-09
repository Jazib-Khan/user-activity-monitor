from flask import Flask, request, jsonify
from collections import deque

app = Flask(__name__)

# Store recent user activity
user_activity = {}

# Define alert codes
ALERT_CODES = {
    "1100": "Withdrawal amount over 100",
    "30": "3 consecutive withdrawals",
    "300": "3 consecutive deposits with increasing amounts",
    "123": "Total amount deposited in 30 seconds exceeds 200"
}

@app.route('/event', methods=['POST'])
def process_event():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        event_type = data.get('type')
        amount = float(data.get('amount'))
        timestamp = data.get('time')

        if user_id not in user_activity:
            user_activity[user_id] = {
                "withdrawals": deque(maxlen=3),
                "deposits": deque(maxlen=3),
                "deposit_window": deque(maxlen=30),
                "last_deposit_time": 0
            }

        user_data = user_activity[user_id]

        # Check for alert 1100
        if event_type == "withdraw" and amount > 100:
            return jsonify({"alert": True, "alert_codes": ["1100"], "user_id": user_id})

        # Check for alert 30
        if event_type == "withdraw":
            user_data["withdrawals"].append(amount)
            if len(user_data["withdrawals"]) == 3:
                return jsonify({"alert": True, "alert_codes": ["30"], "user_id": user_id})

        # Check for alert 300
        if event_type == "deposit":
            user_data["deposits"].append(amount)
            if len(user_data["deposits"]) == 3:
                if user_data["deposits"][0] < user_data["deposits"][1] < user_data["deposits"][2]:
                    return jsonify({"alert": True, "alert_codes": ["300"], "user_id": user_id})

        # Check for alert 123
        if event_type == "deposit":
            user_data["deposit_window"].append(amount)
            if timestamp - user_data["last_deposit_time"] <= 30:
                total_deposit = sum(user_data["deposit_window"])
                if total_deposit > 200:
                    return jsonify({"alert": True, "alert_codes": ["123"], "user_id": user_id})
            user_data["last_deposit_time"] = timestamp

        return jsonify({"alert": False, "alert_codes": [], "user_id": user_id})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
