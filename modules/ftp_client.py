"""Menu 12 — Mini Shell FTP Client"""
import os
import ftplib
from colorama import Fore, Style

HELP = """
Command tersedia:
  ls                    — list direktori
  cwd <path>            — pindah direktori
  pwd                   — direktori aktif
  get <remote> [local]  — download file
  put <local> [remote]  — upload file
  delete <file>         — hapus file
  mkdir <dir>           — buat direktori
  rmdir <dir>           — hapus direktori
  rename <old> <new>    — rename
  help                  — tampilkan bantuan
  exit                  — keluar
"""


def run():
    print(f"{Fore.CYAN}[*] Mini Shell FTP Client{Style.RESET_ALL}")
    host = input("Host (IP / domain): ").strip()
    port = int(input("Port [21]: ").strip() or 21)
    use_tls = input("Pakai FTPS? [y/N]: ").strip().lower() == "y"
    user = input("Username: ").strip()
    password = input("Password: ").strip()

    try:
        ftp = ftplib.FTP_TLS() if use_tls else ftplib.FTP()
        ftp.connect(host, port, timeout=15)
        ftp.login(user, password)
    except Exception as e:
        print(f"{Fore.RED}[!] Login gagal: {e}{Style.RESET_ALL}")
        return

    print(f"{Fore.GREEN}[+] Terhubung. Ketik 'help' untuk bantuan.{Style.RESET_ALL}")

    try:
        while True:
            try:
                line = input(f"{Fore.GREEN}ftp> {Style.RESET_ALL}").strip()
            except EOFError:
                break
            if not line:
                continue
            parts = line.split()
            cmd = parts[0].lower()

            try:
                if cmd in ("exit", "quit"):
                    break
                elif cmd == "help":
                    print(HELP)
                elif cmd == "ls":
                    ftp.retrlines("LIST")
                elif cmd == "pwd":
                    print(ftp.pwd())
                elif cmd == "cwd" and len(parts) > 1:
                    ftp.cwd(parts[1])
                    print(f"{Fore.GREEN}[+] OK{Style.RESET_ALL}")
                elif cmd == "get" and len(parts) > 1:
                    local = parts[2] if len(parts) > 2 else os.path.basename(parts[1])
                    with open(local, "wb") as f:
                        ftp.retrbinary(f"RETR {parts[1]}", f.write)
                    print(f"{Fore.GREEN}[+] Tersimpan: {local}{Style.RESET_ALL}")
                elif cmd == "put" and len(parts) > 1:
                    remote = parts[2] if len(parts) > 2 else os.path.basename(parts[1])
                    with open(parts[1], "rb") as f:
                        ftp.storbinary(f"STOR {remote}", f)
                    print(f"{Fore.GREEN}[+] Terupload: {remote}{Style.RESET_ALL}")
                elif cmd == "delete" and len(parts) > 1:
                    ftp.delete(parts[1])
                    print(f"{Fore.GREEN}[+] Terhapus{Style.RESET_ALL}")
                elif cmd == "mkdir" and len(parts) > 1:
                    ftp.mkd(parts[1])
                    print(f"{Fore.GREEN}[+] Dibuat{Style.RESET_ALL}")
                elif cmd == "rmdir" and len(parts) > 1:
                    ftp.rmd(parts[1])
                    print(f"{Fore.GREEN}[+] Dihapus{Style.RESET_ALL}")
                elif cmd == "rename" and len(parts) > 2:
                    ftp.rename(parts[1], parts[2])
                    print(f"{Fore.GREEN}[+] Renamed{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}[?] Command tidak dikenal. Ketik 'help'.{Style.RESET_ALL}")
            except ftplib.all_errors as e:
                print(f"{Fore.RED}[!] {e}{Style.RESET_ALL}")
    finally:
        try:
            ftp.quit()
        except Exception:
            ftp.close()
        print(f"{Fore.YELLOW}[+] Koneksi ditutup.{Style.RESET_ALL}")
