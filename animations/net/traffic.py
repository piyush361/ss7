import socket
import time
import random
import requests
from test_ids import generate_MTP, generate_MAP, generate_ISUP, generate_TCAP, generate_SCCP

SERVER_IP = "127.0.0.1"
PORT = 9999
SESSION_TIMEOUT = 10  

fsn_list = [1000]  
transaction_ids = []  
imsi_requests = {}  

gt_map = {"1234567890": 1, "9876543210": 0}  
authorized_gts = {"1112223333", "4445556666"} 
known_vlrs = {"+911234567890", "+919876543210"}  
known_components = {"Invoke", "ReturnResult", "ReturnError", "Reject"}  
call_sessions = {2001, 2002, 2003}  
valid_message_types = {"IAM", "ACM", "ANM", "REL", "RLC"}  

API_REPORT_URL = "http://localhost:8000/report"
API_COUNT_URL = "http://localhost:8000/count"

def post_count():
    """Increment packet count in API."""
    try:
        response = requests.post(API_COUNT_URL)  # Fixed incorrect API URL
        if response.status_code == 200:
            print("[+] Count sent successfully")
        else:
            print(f"[-] Failed to send count: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[!] Error sending count: {e}")

def post_per_sess(temp_counter):
    """Send per-session count to API."""
    try:
        response = requests.post(API_COUNT_URL, json={"temp_counter": temp_counter})  # Fixed JSON format
        if response.status_code == 200:
            print("[+] Per-session packet count sent successfully")
        else:
            print(f"[-] Failed to send per-session count: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[!] Error sending per-session count: {e}")


def generate_ss7_packet(b,id):
    """Generate an SS7 packet with a unique MTP OPC as the Session ID."""
    mtp = generate_MTP(fsn_list)
    sccp = generate_SCCP(gt_map, authorized_gts)
    tcap = generate_TCAP(transaction_ids, known_components)
    map = generate_MAP(imsi_requests, known_vlrs)
    isup = generate_ISUP(call_sessions, valid_message_types)


    ss7_packet = [
    f"MTP:{{'opc':{mtp.opc}, 'dpc':{mtp.dpc}, 'si':{mtp.si}, 'bsn':{mtp.bsn}, 'fsn':{mtp.fsn}}}|"
    f"SCCP:{{'calling_party':'{sccp.calling_party}', 'called_party':'{sccp.called_party}', 'sequence_control':{sccp.sequence_control}, 'protocol_class':'{sccp.protocol_class}'}}|"
    f"TCAP:{{'transaction_id':{tcap.transaction_id}, 'component':'{tcap.component}'}}|"
    f"MAP:{{'operation_code':{map.operation_code}, 'imsi':'{map.imsi}', 'vlr_number':'{map.vlr_number}','msisdn':'{map.msisdn}'}}|"
    f"ISUP:{{'cic':{isup.cic}, 'message_type':'{isup.message_type}'}}|"
    f"Session:{b}|"
    f"Packet ID:{id}"
    ]

    return ss7_packet 

while True:
   # sid = f"{c}"

    print("[+] Starting new session...")
    b=random.randint(0,155)
    session_start_time = time.time()

    while time.time() - session_start_time < SESSION_TIMEOUT:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((SERVER_IP, PORT))

            id = random.randint(0,842)
            ss7_packet = generate_ss7_packet(b,id)
           # ss7_packet.append(c)
            for pkt in ss7_packet:
              #print(pkt[len(pkt)-1])
              #print(len(pkt))
              client.send(pkt.encode())
              post_count()
            print(f"[+] Sent SS7 packet (ID: {id} )")
            #c+=1

            client.close()
        except Exception as e:
            print(f"[!] Connection error: {e}")

        time.sleep(0.49)  

    print(f"[!] Session {b} expired. Starting new session...\n")
