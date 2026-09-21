#!/usr/bin/env python3
"""
WebShell Finder Toolkit - Main Menu
Author : LO
License: MIT
"""

import os
import sys
from colorama import init, Fore, Style

init(autoreset=True)

BANNER = f"""
{Fore.GREEN}╔══════════════════════════════════════════════════════════╗
║        WEBSHELL FINDER TOOLKIT — by LO                   ║
║        For Authorized Security Testing Only               ║
╚══════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""

MENU = f"""
{Fore.CYAN}[ 01 ]{Style.RESET_ALL} WebShell Finder  (Dir Scan 48k Path)
{Fore.CYAN}[ 02 ]{Style.RESET_ALL} WebShell Finder  (Auto Filename Enumeration)
{Fore.CYAN}[ 03 ]{Style.RESET_ALL} Reverse IP
{Fore.CYAN}[ 04 ]{Style.RESET_ALL} Subdomain Scanner
{Fore.CYAN}[ 05 ]{Style.RESET_ALL} Scanner ENV & Debug Method
{Fore.CYAN}[ 06 ]{Style.RESET_ALL} Extract Domain (Auto Add https)
{Fore.CYAN}[ 07 ]{Style.RESET_ALL} WordPress Register Finder
{Fore.CYAN}[ 08 ]{Style.RESET_ALL} Grab Registered Domain by Date
{Fore.CYAN}[ 09 ]{Style.RESET_ALL} Grab Domain from haxor.id
{Fore.CYAN}[ 10 ]{Style.RESET_ALL} Grab Domain from zone-h.org
{Fore.CYAN}[ 11 ]{Style.RESET_ALL} FTP Bruteforce (FTP, FTPS)
{Fore.CYAN}[ 12 ]{Style.RESET_ALL} Mini Shell FTP Client
{Fore.CYAN}[ 13 ]{Style.RESET_ALL} Mass Proxy Validator
{Fore.RED}[ 14 ]{Style.RESET_ALL} Logout / Exit
"""


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input(f"\n{Fore.YELLOW}[!] Tekan ENTER untuk kembali ke menu...{Style.RESET_ALL}")


def dispatch(choice):
    try:
        if choice == "1":
            from modules import webshell_dir
            webshell_dir.run()
        elif choice == "2":
            from modules import webshell_name
            webshell_name.run()
        elif choice == "3":
            from modules import reverse_ip
            reverse_ip.run()
        elif choice == "4":
            from modules import subdomain
            subdomain.run()
        elif choice == "5":
            from modules import env_debug
            env_debug.run()
        elif choice == "6":
            from modules import extract_domain
            extract_domain.run()
        elif choice == "7":
            from modules import wp_register
            wp_register.run()
        elif choice == "8":
            from modules import domain_by_date
            domain_by_date.run()
        elif choice == "9":
            from modules import haxor_grab
            haxor_grab.run()
        elif choice == "10":
            from modules import zoneh_grab
            zoneh_grab.run()
        elif choice == "11":
            from modules import ftp_brute
            ftp_brute.run()
        elif choice == "12":
            from modules import ftp_client
            ftp_client.run()
        elif choice == "13":
            from modules import proxy_validator
            proxy_validator.run()
        else:
            print(f"{Fore.RED}[!] Menu tidak valid.{Style.RESET_ALL}")
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Dibatalkan oleh user.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")


def main():
    while True:
        clear()
        print(BANNER)
        print(MENU)
        choice = input(f"{Fore.GREEN}Pilih menu [1-14]: {Style.RESET_ALL}").strip()

        if choice == "14":
            print(f"{Fore.YELLOW}[+] Keluar... Sampai jumpa, LO!{Style.RESET_ALL}")
            sys.exit(0)

        dispatch(choice)
        pause()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Interrupted.{Style.RESET_ALL}")
        sys.exit(0)
