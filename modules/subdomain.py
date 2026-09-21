"""Menu 4 — Subdomain Scanner"""
import os
import socket
import requests
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor, as_completed

WORDLIST = os.path.join("wordlists", "subdomains.txt")

DEFAULT_SUBS = [
    "www", "mail", "ftp", "webmail", "smtp", "pop", "ns1", "ns2",
    "dev", "test", "staging", "api", "admin", "portal", "blog",
    "shop", "cdn", "static", "img", "assets", "vpn", "remote",
]


def resolve(sub, domain):
    full = f"{sub}.{domain}"
    try:
        ip = socket.gethostbyname(full)
        return (full, ip)
    except socket.gaierror:
        return None


def run():
    print(f"{Fore.CYAN}[*] Subdomain Scanner{Style.RESET_ALL}")
    domain = input("Domain (example.com): ").strip().replace("https://", "").replace("http://", "").strip("/")
    if not domain:
        print(f"{Fore.RED}[!] Domain kosong.{Style.RESET_ALL}")
        return

    subs = list(DEFAULT_SUBS)
    if os.path.exists(WORDLIST):
        with open(WORDLIST, "r", errors="ignore") as f:
            subs += [line.strip() for line in f if line.strip()]
        print(f"{Fore.YELLOW}[*] Wordlist dimuat: {len(subs)} subdomain{Style.RESET_ALL}")

    threads = int(input("Threads [default 20]: ").strip() or 20)
    found = []

    with ThreadPoolExecutor(max_workers=threads) as ex:
        futures = {ex.submit(resolve, s, domain): s for s in subs}
        for fut in as_completed(futures):
            res = fut.result()
            if res:
                sub, ip = res
                print(f"{Fore.GREEN}[+] {sub} -> {ip}{Style.RESET_ALL}")
                found.append((sub, ip))

    print(f"\n{Fore.GREEN}[+] Selesai. Ditemukan {len(found)} subdomain.{Style.RESET_ALL}")
    if found:
        os.makedirs("results", exist_ok=True)
        with open("results/subdomains.txt", "w") as f:
            for s, ip in found:
                f.write(f"{s}\t{ip}\n")
        print(f"{Fore.GREEN}[+] Disimpan ke results/subdomains.txt{Style.RESET_ALL}")
