# TryHackMe — Pickle Rick Writeup

**Room:** Pickle Rick (Rick and Morty themed)
**Difficulty:** Easy
**Ingredients found:** 3/3 ✅

## Overview
A Rick and Morty-themed web exploitation challenge. Rick has turned himself
into a pickle and needs three secret ingredients to reverse the potion. The
box involves web recon, a login bypass bug, command injection with filter
evasion, and privilege escalation via a dangerous sudo misconfiguration.

## 1. Reconnaissance

Initial port scan:
nmap -sV -sC -A <target-ip>

Result: two open ports —
- `22/tcp` — SSH (OpenSSH)
- `80/tcp` — HTTP (Apache), page title: "Rick is sup4r cool"

**Note:** The target is only reachable from inside WSL2 (the VPN tunnel
runs in WSL's own network namespace, not Windows'), so the Windows browser
can't reach it directly. All interaction with the web server had to go
through `curl` from the WSL terminal instead.

## 2. Finding credentials

Fetched the homepage:
curl http://<target-ip>/

Inside an HTML comment in the page source was a note:
Username: R1ckRul3s


Checked `robots.txt` next, a common place developers leave hints:

curl http://<target-ip>/robots.txt

This revealed the password: `Wubbalubbadubdub`

## 3. Login — a small but important bug

Found a login form at `/login.php` and POSTed the credentials:

curl -X POST http://<target-ip>/login.php -d "username=R1ckRul3s&password=Wubbalubbadubdub"

This returned `200 OK` but no redirect — login silently failed. Inspecting
the HTML form revealed the submit button had its own `name="sub"`
attribute, which the backend PHP checks to confirm the form was actually
submitted (not just that credentials were present). Adding it fixed the
login:

curl -X POST http://<target-ip>/login.php
-d "username=R1ckRul3s&password=Wubbalubbadubdub&sub=Login"
-c cookies.txt

This returned `302 Found` with `Location: /portal.php` — login succeeded.

## 4. Command injection with filter bypass

`/portal.php` exposed a "Command Panel" that executes shell commands as
`www-data` and reflects the output in the page.

First command tried:

command=whoami → returned: www-data


Attempted to read the first ingredient file directly:

command=cat '/home/rick/second ingredients'

This returned: *"Command disabled to make it hard for future PICKLE RICK"*
— the app blacklists certain command names like `cat` and `head`.

Confirmed the filter wasn't blocking all commands by testing `ls`, which
worked fine — so the block was on specific command *names*, not file paths.

Bypassed the filter using `sort`, which also prints file contents for a
single-line file:

command=sort '/home/rick/second ingredients'

**Result — Ingredient #2: `1 jerry tear`**

## 5. Privilege escalation

Checked sudo permissions for `www-data`:

command=sudo -l

Result:

User www-data may run the following commands on <host>:
(ALL) NOPASSWD: ALL

This is a critical misconfiguration — `www-data` can run *any* command as
root with no password required. This effectively grants full root access
through the same command injection point.

Listed root's home directory:

command=sudo ls -la /root/

Found `3rd.txt`. Read it using the same `sort` bypass with `sudo`:

command=sudo sort /root/3rd.txt

**Result — Ingredient #3: `fleeb juice`**

## 6. Finding the first ingredient

A broad `find` for "ingredient" files only turned up the one already found
in `/home/rick/`. Reasoned that the web root itself (`/var/www/html/`)
was worth checking, since it's the most directly exposed location:

command=sudo ls -la /var/www/html/

This revealed `Sup3rS3cretPickl3Ingred.txt`. Read with `sudo sort`:

command=sudo sort /var/www/html/Sup3rS3cretPickl3Ingred.txt

**Result — Ingredient #1: `mr. meeseek hair`**

## Key Takeaways
- Blacklist-based input filtering (blocking specific command *names* like
  `cat`) is fragile and easy to bypass — there are usually several other
  commands (`sort`, `nl`, `tac`, `more`, `less`, etc.) that read file
  content just as well. Filtering should use an allowlist, not a blocklist.
- `NOPASSWD: ALL` in sudoers is one of the most dangerous misconfigurations
  possible — it turns any code-execution bug (even a lightweight one like
  this command panel) directly into full root compromise.
- Small details matter: a missing form field (`sub=Login`) silently broke
  authentication even with correct credentials — always inspect the full
  HTML form, not just the visible inputs.

## Tools Used
nmap, curl, manual command-injection filter bypass, sudo misconfiguration
abuse

