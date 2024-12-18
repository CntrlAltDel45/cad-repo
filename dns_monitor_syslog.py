import socket
import time
from datetime import datetime
import logging
import logging.handlers

# Configuration
dns_to_monitor = "anward8.ip.afrihost.co.za"  # DNS address to monitor
check_interval = 5 * 60  # 5 minutes in seconds

# Initialize variables
current_ip = None
last_change_time = None

# Configure syslog handler
syslog_handler = logging.handlers.SysLogHandler(address='/var/run/log')
logger = logging.getLogger()
logger.addHandler(syslog_handler)
logger.setLevel(logging.INFO)

# Helper function to log messages to syslog
def log_message(message):
    logger.info(f"DNS Monitor: {message}")

# Initial log
log_message(f"Monitoring started for DNS: {dns_to_monitor} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

while True:
    try:
        # Resolve the DNS to an IP address
        resolved_ip = socket.gethostbyname(dns_to_monitor)
        now = datetime.now()

        if current_ip is None:
            # First-time resolution
            current_ip = resolved_ip
            last_change_time = now
            log_message(f"Initial IP resolved: {current_ip} at {now.strftime('%Y-%m-%d %H:%M:%S')}")
        elif resolved_ip != current_ip:
            # IP has changed
            duration = now - last_change_time
            duration_str = str(duration).split('.')[0]  # Format the duration without microseconds

            log_message(f"IP change detected: {current_ip} -> {resolved_ip} at {now.strftime('%Y-%m-%d %H:%M:%S')}\n"
                        f"Duration with previous IP ({current_ip}): {duration_str}")

            # Update current IP and last change time
            current_ip = resolved_ip
            last_change_time = now

    except Exception as e:
        log_message(f"Error resolving DNS: {str(e)} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Wait for the next check
    time.sleep(check_interval)
