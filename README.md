# user-activity-monitor

## The Task

<p>Build an API endpoint called /event that receives a payload representing a user's action
(like a deposit or withdrawal). Based on the activity in the payload, your endpoint should check against
some predefined rules to determine if an alert should be raised.</p>
Here's the expected payload format:
<pre><code>{
    "type": "deposit",
    "amount": "42.00",
    "user_id": 1,
    "time": 10
}</code></pre>
<ul>
    <li>type: str The type of user action, either deposit or withdraw .</li>
    <li>amount: str The amount of money the user is depositing or withdrawing.</li>
    <li>user_id: int A unique identifier for the user.</li>
    <li>time: int The timestamp of the action (this value is always increasing).</li>
</ul>
The response should look like this:
The response should look like this:
<pre><code>{
    "alert": true,
    "alert_codes": [30, 123],
    "user_id": 1,
}</code></pre>

### Expected behaviour

<p>You'll be checking for these conditions to trigger alerts:</p>
<ul>
    <li>alert: Should be true if any alert codes are triggered, otherwise false.</li>
    <li>alert_codes: A list of alert codes that have been triggered (if any)</li>
    <li>user_id: The user_id of the user whose action was processed</li>
</ul>

### Alert codes

<ul>
    <li>Code: 1100 : A withdrawal amount over 100</li>
    <li>Code: 30 : The user makes 3 consecutive withdrawals</li>
    <li>Code: 300 : The user makes 3 consecutive deposits where each one is larger than the previous
        deposit (withdrawals in between deposits can be ignored).</li>
    <li>Code: 123 : The total amount deposited in a 30-second window exceeds 200</li>
</ul>

<p>To test your endpoint, you can use this curl command:</p>
curl -XPOST http://127.0.0.1:5000/event -H 'Content-Type: application/json' \
-d '{"type": "deposit", "amount": "42.00", "user_id": 1, "time": 0}'
