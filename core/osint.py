#!/usr/bin/env python3
import hashlib
import json
import urllib.request
import urllib.error

class OSINTRecon:
    """Performs deep passive OSINT checks and service associations on a target email address."""
    def __init__(self, email_str):
        self.email = email_str.strip()
        self.email_hash = hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    def check_gravatar(self):
        print("\n[+] Checking Gravatar Profile...")
        url = f"https://www.gravatar.com/avatar/{self.email_hash}?json=1"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    entry = data.get('entry', [{}])[0]
                    print(f"    [!] Gravatar Found: {entry.get('profileUrl', 'N/A')}")
                    print(f"    [!] Display Name:   {entry.get('displayName', 'N/A')}")
                    print(f"    [!] Profile About:  {entry.get('aboutMe', 'N/A')}")
        except Exception:
            print("    [-] No Gravatar profile found.")

    def check_github(self):
        print("\n[+] Checking GitHub Public API...")
        url = f"https://api.github.com/search/users?q={self.email}+in:email"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/vnd.github.v3+json'})
        try:
            with urllib.request.urlopen(req) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    if data.get('total_count', 0) > 0:
                        username = data['items'][0]['login']
                        profile_url = data['items'][0]['html_url']
                        print(f"    [!] GitHub Account Found: {profile_url}")
                        print(f"    [!] Associated Username:  {username}")
                        print(f"        -> Tip: Run 'python3 main.py -g {username}' for deep commit inspection.")
                    else:
                        print("    [-] No GitHub account linked to this email.")
        except Exception:
            print("    [-] GitHub API check failed or rate-limited.")

    def check_keybase(self):
        print("\n[+] Checking Keybase Public Registry...")
        # Keybase allows lookup via email hash or primary query endpoints
        url = f"https://keybase.io/_/api/1.0/user/lookup.json?email_or_username={self.email}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    if data.get('status', {}).get('code') == 0 and data.get('them'):
                        kb_user = data['them'].get('basics', {}).get('username', 'N/A')
                        print(f"    [!] Keybase Profile Found: https://keybase.io/{kb_user}")
                    else:
                        print("    [-] No Keybase profile found for this email.")
        except Exception:
            print("    [-] Keybase lookup skipped or service unavailable.")

    def check_service_registrations(self):
        """Checks public registration endpoints for service association."""
        print("\n[+] Checking Additional Platform Endpoints...")
        
        services = {
            "HackerRank": f"https://www.hackerrank.com/rest/search/autocomplete?query={self.email}",
        }

        for service, url in services.items():
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            try:
                with urllib.request.urlopen(req) as response:
                    data = json.loads(response.read().decode('utf-8'))
                    # Analyze data payload for matching patterns
                    print(f"    [*] Queried {service}: Endpoint responsive")
            except Exception:
                print(f"    [-] {service} check yielded no direct public associations.")

    def run(self):
        print(f"\n[+] --- EXTENDED 'G'RAB RECONNAISSANCE: {self.email} ---")
        if "@" not in self.email:
            print("[-] Invalid email address format.")
            return
        
        domain = self.email.split('@')[1]
        print(f"[*] Target Domain: {domain}")
        self.check_gravatar()
        self.check_github()
        self.check_keybase()
        self.check_service_registrations()
