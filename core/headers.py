#!/usr/bin/env python3
import email
import re
from email import policy

class HeaderForensics:
    """Parses raw email headers to extract routing IPs and client data."""
    def __init__(self, eml_path):
        self.eml_path = eml_path

    def analyze(self):
        try:
            with open(self.eml_path, 'r', encoding='utf-8', errors='ignore') as f:
                msg = email.message_from_file(f, policy=policy.default)
        except Exception as e:
            print(f"[-] Error reading file: {e}")
            return

        print("\n[+] --- EMAIL HEADER FORENSICS ---")
        print(f"[*] Subject: {msg.get('Subject', 'N/A')}")
        print(f"[*] From:    {msg.get('From', 'N/A')}")
        print(f"[*] To:      {msg.get('To', 'N/A')}")
        print(f"[*] Date:    {msg.get('Date', 'N/A')}")

        received_headers = msg.get_all('Received', [])
        print(f"\n[+] Tracing IP Hops ({len(received_headers)} hops found):")
        
        ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
        
        for idx, hop in enumerate(received_headers):
            ips = ip_pattern.findall(hop)
            if ips:
                print(f"    - Hop {idx+1}: IPs detected -> {', '.join(ips)}")

        print(f"\n[+] Authentication Results:")
        print(f"    - SPF:  {msg.get('Received-SPF', 'Not Found')}")
        print(f"    - DKIM: {msg.get('DKIM-Signature', 'Not Found')}")
        print(f"    - DMARC: {msg.get('Authentication-Results', 'Not Found')}")
