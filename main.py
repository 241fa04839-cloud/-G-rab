#!/usr/bin/env python3
"""
Tool: 'G'rab CLI
Description: Email header forensics and OSINT footprint reconnaissance.
"""

import argparse
import sys
from core.headers import HeaderForensics
from core.osint import OSINTRecon
from core.github_deep import GitHubDeepRecon

def banner():
    print(r"""
   ____           _     
  / ___|_ __ __ _| |__  
 | |  _| '__/ _` | '_ \ 
 | |_| | | | (_| | |_) |
  \____|_|  \__,_|_.__/ 
    [ 'G'rab Recon Suite ]
    """)

def main():
    banner()
    parser = argparse.ArgumentParser(description="'G'rab Forensic and OSINT CLI Tool")
    parser.add_argument("-e", "--email", help="Target email address for OSINT checks")
    parser.add_argument("-f", "--file", help="Path to raw .eml file for header forensics")
    parser.add_argument("-g", "--github", help="Target GitHub username for deep commit/metadata extraction")
    
    args = parser.parse_args()

    if not args.email and not args.file and not args.github:
        parser.print_help()
        sys.exit(1)

    if args.file:
        hf = HeaderForensics(args.file)
        hf.analyze()

    if args.email:
        osint = OSINTRecon(args.email)
        osint.run()

    if args.github:
        gh_deep = GitHubDeepRecon(args.github)
        gh_deep.inspect()

if __name__ == "__main__":
    main()
