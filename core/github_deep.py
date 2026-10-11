#!/usr/bin/env python3
import json
import urllib.request

class GitHubDeepRecon:
    """Extracts deep identity markers and commit metadata from a GitHub handle."""
    def __init__(self, username):
        self.username = username.strip()

    def inspect(self):
        print(f"\n[+] --- DEEP GITHUB INSPECTION: {self.username} ---")
        
        # 1. Fetch User Profile Data
        profile_url = f"https://api.github.com/users/{self.username}"
        req = urllib.request.Request(profile_url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/vnd.github.v3+json'})
        
        try:
            with urllib.request.urlopen(req) as response:
                user_data = json.loads(response.read().decode('utf-8'))
                print(f"    [+] Name:         {user_data.get('name', 'N/A')}")
                print(f"    [+] Company:      {user_data.get('company', 'N/A')}")
                print(f"    [+] Location:     {user_data.get('location', 'N/A')}")
                print(f"    [+] Bio:          {user_data.get('bio', 'N/A')}")
                print(f"    [+] Blog/Site:    {user_data.get('blog', 'N/A')}")
                print(f"    [+] Public Repos: {user_data.get('public_repos', 0)}")
                print(f"    [+] Account Type: {user_data.get('type', 'N/A')}")
        except Exception as e:
            print(f"    [-] Failed to fetch user profile: {e}")
            return

        # 2. Fetch Public Repositories to check commit history for leaked emails/names
        repos_url = f"https://api.github.com/users/{self.username}/repos"
        req_repos = urllib.request.Request(repos_url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/vnd.github.v3+json'})
        
        try:
            with urllib.request.urlopen(req_repos) as response:
                repos = json.loads(response.read().decode('utf-8'))
                print(f"\n    [+] Analyzing Repositories for Leaked Author Signatures...")
                for repo in repos[:5]:  # Check top 5 repos
                    repo_name = repo.get('name')
                    commits_url = f"https://api.github.com/repos/{self.username}/{repo_name}/commits"
                    req_commits = urllib.request.Request(commits_url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/vnd.github.v3+json'})
                    try:
                        with urllib.request.urlopen(req_commits) as commit_resp:
                            commits = json.loads(commit_resp.read().decode('utf-8'))
                            for commit in commits[:3]:  # Check last 3 commits per repo
                                author = commit.get('commit', {}).get('author', {})
                                print(f"        - Repo [{repo_name}] Commit Author: {author.get('name')} <{author.get('email')}>")
                    except Exception:
                        pass
        except Exception:
            print("    [-] Could not parse repository commit logs.")
