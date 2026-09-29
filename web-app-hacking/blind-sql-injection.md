# Blind SQL Injection with Conditional Responses (Burp Suite)

## Lab
Blind SQL injection with conditional responses
https://portswigger.net/web-security/sql-injection/blind

## Vulnerability
The application uses a TrackingId cookie in a SQL query. No errors or data
are shown directly, but the page displays a "Welcome back" message when the
query returns a row - this became the oracle for extracting data blindly.

## Step 1: Confirm Injection Point via Cookie
Modified TrackingId cookie value using browser DevTools (Application tab):

TrackingId=xxxx' AND '1'='1   -> "Welcome back" appears (TRUE)
TrackingId=xxxx' AND '1'='2   -> "Welcome back" disappears (FALSE)

This confirmed a working boolean-based blind SQL injection point.

## Step 2: Confirm the administrator Account Exists
TrackingId=xxxx' AND (SELECT 'a' FROM users WHERE username='administrator')='a

Result: "Welcome back" appeared, confirming the administrator user exists.

## Step 3: Determine Password Length
Used LENGTH() with binary search to find the password length:

TrackingId=xxxx' AND (SELECT 'a' FROM users WHERE username='administrator'
AND LENGTH(password)>N)='a

Result: password length = 19 characters

## Step 4: Extract Password Character by Character
Used SUBSTRING() to test one character at a time, for each position 1-19:

TrackingId=xxxx' AND (SELECT SUBSTRING(password,N,1) FROM users
WHERE username='administrator')='X'--

Manually confirmed first two characters (q, c) to understand the technique,
then used Burp Suite Intruder to automate the remaining positions:

1. Captured the request via Burp Proxy (using Burp's built-in browser)
2. Sent request to Intruder
3. Marked the guessed character as the payload position (Sniper attack)
4. Set payload type to Brute forcer, character set a-z0-9, length 1
5. Ran the attack and identified the correct character by response length
   (the TRUE response returns a longer page due to "Welcome back" text)
6. Repeated for each of the 19 positions, changing the SUBSTRING position
   each time

## Step 5: Login as Administrator
Used the fully reconstructed 19-character password to log in as
administrator via the My Account page. Lab solved.

## Key Takeaway
Blind SQL injection proves that even when an application shows no visible
error messages or query output, an attacker can still extract data entirely
through the application's behavior (response content/length/timing) as a
side channel. This is why input validation and parameterized queries must
be applied everywhere user input reaches a database query - not just where
results are directly displayed on the page.

Tools used: Browser DevTools (cookie manipulation), Burp Suite Community
Edition (Proxy + Intruder for automated character extraction).

## Legal Note
Practiced only on PortSwigger Web Security Academy - an authorized, legal
practice platform. Blind SQL injection against any website without explicit
written permission is illegal (IT Act 2000, India).

