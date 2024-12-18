import socket
from datetime import datetime
import os

# Configuration
dns_to_monitor = "anward8.ip.afrihost.co.za"  # DNS address to monitor
log_file = os.path.join(os.path.expanduser("~"), "Desktop", "dns_ip_changes.log")
current_ip_file = os.path.join(os.path.expanduser("~"), "Desktop", "current_ip.txt")

# Helper function to log messages to the file
def log_message(message):
    with open(log_file, "a") as log:
        log.write(f"{message}\n")

try:
    # Resolve the DNS to an IP address
    resolved_ip = socket.gethostbyname(dns_to_monitor)
    now = datetime.now()

    # Load the current IP from the file (if it exists)
    if os.path.exists(current_ip_file):
        with open(current_ip_file, "r") as f:
            current_ip = f.read().strip()
    else:
        current_ip = None

    if current_ip is None:
        # First-time resolution
        current_ip = resolved_ip
        with open(current_ip_file, "w") as f:
            f.write(current_ip)
        log_message(f"Initial IP resolved: {current_ip} at {now.strftime('%Y-%m-%d %H:%M:%S')}")
    elif resolved_ip != current_ip:
        # IP has changed
        with open(current_ip_file, "w") as f:
            f.write(resolved_ip)
        log_message(f"IP change detected: {current_ip} -> {resolved_ip} at {now.strftime('%Y-%m-%d %H:%M:%S')}\nDuration since last change: {str(datetime.now() - now).split('.')[0]}")

except Exception as e:
    log_message(f"Error resolving DNS: {str(e)} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
