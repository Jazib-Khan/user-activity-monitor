# user-activity-monitor

building an API endpoint called /event that receives a payload representing a user's action
(like a deposit or withdrawal). Based on the activity in the payload, your endpoint should check against
some predefined rules to determine if an alert should be raised.
Here's the expected payload format:
{
"type": "deposit",
"amount": "42.00",
"user_id": 1,
"time": 10
}
• type: str The type of user action, either deposit or withdraw .
• amount: str The amount of money the user is depositing or withdrawing.
• user_id: int A unique identifier for the user.
• time: int The timestamp of the action (this value is always increasing).
The response should look like this:
{
"alert": true,
"alert_codes": [30, 123],
"user_id": 1
}
Expected behaviour
You'll be checking for these conditions to trigger alerts:
• alert: Should be true if any alert codes are triggered, otherwise false.
• alert_codes: A list of alert codes that have been triggered (if any)
• user_id: The user_id of the user whose action was processed

Alert codes
• Code: 1100 : A withdrawal amount over 100
• Code: 30 : The user makes 3 consecutive withdrawals
• Code: 300 : The user makes 3 consecutive deposits where each one is larger than the previous
deposit (withdrawals in between deposits can be ignored).
• Code: 123 : The total amount deposited in a 30-second window exceeds 200

To test your endpoint, you can use this curl command:
curl -XPOST http://127.0.0.1:5000/event -H 'Content-Type: application/json' \
-d '{"type": "deposit", "amount": "42.00", "user_id": 1, "time": 0}'
