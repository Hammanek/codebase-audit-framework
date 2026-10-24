#!/usr/bin/env python3
"""
Codebase Audit Helper - Quick Static Analysis Scanner
Scans project code for high-risk security, DevOps, and performance anti-patterns.
Usage: python audit_scan.py [path_to_project]
"""

import os
import sys
import re

IGNORE_DIRS = {'.git', '__pycache__', '.venv', 'venv', 'env', 'node_modules', '.idea', '.vscode', 'dist', 'build'}

RULES = [
    {
        "id": "SEC-BIND",
        "category": "Network Exposure",
        "severity": "HIGH",
        "desc": "Binding service to all interfaces (0.0.0.0) without explicit auth",
        "regex": re.compile(r"""(?:host\s*=\s*['"]0\.0\.0\.0['"]|bind\s*:\s*['"]0\.0\.0\.0['"])"""),
        "exts": {'.py', '.js', '.ts', '.yml', '.yaml', '.json'},
    },
    {
        "id": "SEC-SHELL",
        "category": "Command Injection",
        "severity": "CRITICAL",
        "desc": "subprocess execution with shell=True",
        "regex": re.compile(r"""subprocess\.(?:run|Popen|call|check_output)\([^)]*shell\s*=\s*True"""),
        "exts": {'.py'},
    },
    {
        "id": "SEC-TIMEOUT",
        "category": "Subprocess Hang / DoS",
        "severity": "MEDIUM",
        "desc": "subprocess.run call missing explicit timeout parameter",
        "regex": re.compile(r"""subprocess\.run\((?:(?!timeout\s*=)[^)])*\)""", re.DOTALL),
        "exts": {'.py'},
    },
    {
        "id": "SEC-PICKLE",
        "category": "Insecure Deserialization",
        "severity": "CRITICAL",
        "desc": "Unsafe deserialization using pickle.loads / pickle.load",
        "regex": re.compile(r"""pickle\.(?:loads?)\("""),
        "exts": {'.py'},
    },
    {
        "id": "SEC-EVAL",
        "category": "Code Injection",
        "severity": "CRITICAL",
        "desc": "Use of eval() on dynamic expressions",
        "regex": re.compile(r"""\beval\s*\("""),
        "exts": {'.py', '.js', '.ts'},
    },
    {
        "id": "OPS-DOCKER-ROOT",
        "category": "Docker Privilege",
        "severity": "HIGH",
        "desc": "Dockerfile missing non-root USER instruction",
        "custom": "check_docker_user",
        "exts": {'Dockerfile'},
    },
    {
        "id": "OPS-ACTION-PIN",
        "category": "Supply Chain Poisoning",
        "severity": "MEDIUM",
        "desc": "GitHub Action referenced by mutable tag/branch instead of full SHA hash",
        "regex": re.compile(r"""uses:\s*[\w\-\.\/]+@(?!([0-9a-f]{40}))([vV]?\d+|main|master)"""),
        "exts": {'.yml', '.yaml'},
    },
]

def scan_project(root_path):
    findings = []
    print(f"[*] Scanning project at: {os.path.abspath(root_path)}")

    for dirpath, dirnames, filenames in os.walk(root_path):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]

        for fname in filenames:
            ext = os.path.splitext(fname)[1]
            fpath = os.path.join(dirpath, fname)
            rel_path = os.path.relpath(fpath, root_path)

            # Check Dockerfile custom rule
            if fname == "Dockerfile":
                try:
                    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                        lines = f.readlines()
                    has_user = any(l.strip().startswith("USER ") for l in lines)
                    if not has_user:
                        findings.append({
                            "id": "OPS-DOCKER-ROOT",
                            "severity": "HIGH",
                            "category": "Docker Privilege",
                            "location": f"{rel_path}:1",
                            "desc": "Dockerfile does not specify a non-root USER directive.",
                        })
                except Exception:
                    pass

            # Text file scans
            for rule in RULES:
                if "regex" not in rule:
                    continue
                if ext in rule["exts"] or (fname in rule["exts"]):
                    try:
                        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                        
                        for m in rule["regex"].finditer(content):
                            # compute line number
                            line_no = content[:m.start()].count("\n") + 1
                            findings.append({
                                "id": rule["id"],
                                "severity": rule["severity"],
                                "category": rule["category"],
                                "location": f"{rel_path}:{line_no}",
                                "desc": rule["desc"],
                            })
                    except Exception:
                        pass

    return findings

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    results = scan_project(target)
    print(f"\n[+] Scan finished. Found {len(results)} potential items:\n")
    for r in results:
        print(f"[{r['severity']}] {r['id']} ({r['category']}) -> {r['location']}: {r['desc']}")
