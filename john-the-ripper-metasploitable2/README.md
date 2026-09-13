# Password Cracking with John the Ripper - Metasploitable2

## Overview
Gained root access to Metasploitable2 via the vsftpd/bindshell backdoor, extracted /etc/passwd and /etc/shadow, then cracked user password hashes offline using John the Ripper and the rockyou.txt wordlist.

## Step 1: Gain Root Access
nc -v <Metasploitable2-IP> 1524

Result: Direct root shell (no authentication required - known bindshell backdoor on port 1524)

## Step 2: Extract Password Files
cat /etc/passwd
cat /etc/shadow

Copied both outputs into local files (passwd.txt and shadow.txt) on the attacking machine.

## Step 3: Combine Files with Unshadow
unshadow passwd.txt shadow.txt > combined.txt

unshadow merges the username/UID info from passwd.txt with the actual password hashes from shadow.txt into a single crackable format.

## Step 4: Crack Hashes with John the Ripper
john --wordlist=/home/jubair/rockyou.txt combined.txt

Loaded 7 password hashes (md5crypt format), ran using 12 OpenMP threads.

## Step 5: View Cracked Passwords
john --show combined.txt

## Results

| User    | Cracked Password |
|---------|-------------------|
| sys     | batman            |
| klog    | 123456789         |
| service | service           |

3 out of 7 password hashes cracked. Remaining accounts (root, msfadmin, postgres, user) were not present in the rockyou.txt wordlist, showing that stronger/uncommon passwords resist dictionary attacks.

## Key Takeaway
This exercise demonstrates why:
- Wordlist-based attacks succeed against weak, common, or reused passwords (klog's "123456789", service's "service" matching the username).
- Critical system accounts (root, admin-level users) should always use long, unique, non-dictionary passwords.
- Password hashes should never be exposed or readable by unauthorized users - here, gaining shell access directly enabled hash extraction.
