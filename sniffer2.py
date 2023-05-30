import pyshark
import datetime

from datetime import datetime
from getpass import getpass
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import sys

velocity = {}
email = None
password = None


def packet_callback(pkt):
    try:
        if 'wlan' in dir(pkt) and 'ta' in dir(pkt.wlan):
            mac_src = pkt.wlan.ta

            # Count packets for source IP
            if mac_src in velocity:
                velocity[mac_src][1] = 1 / ((pkt.sniff_time - velocity[mac_src][0]).total_seconds())
                velocity[mac_src][0] = pkt.sniff_time
                print(f"MAC: {mac_src} - Velocity: {velocity[mac_src][1]}")
            else:
                velocity[mac_src] = [pkt.sniff_time, 0]
                
    except ZeroDivisionError:
        subject = "DDOS THREAT DETECTED"
        message = f"A threat has been detected from MAC Address: {pkt.wlan.ta},\n\nopen the following .txt file to view the details:"

        # Attach the message to the email
        msg = MIMEMultipart()
        msg["From"] = email
        msg["To"] = email
        msg["Subject"] = subject

        # Attach the message to the email
        msg.attach(MIMEText(message, "plain"))

        # Use SMTP to send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(email, password)
            server.send_message(msg)
            
        print(f"DDOS DETECTED FROM MAC ADDRESS: {pkt.wlan.ta}") 
            
        sys.exit()


if _name_ == '_main_':
    email = input("Enter your email: ")
    password = getpass("Type your password: ")
    capture = pyshark.LiveCapture(interface='wlan0', display_filter="wlan.ra == cc:32:e5:b4:ea:70")
    capture.apply_on_packets(packet_callback)
    # capture.sniff(timeout=10)
    # print(capture)