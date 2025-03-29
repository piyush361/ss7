import socket
import time
import threading
import ast
import requests
from ids import mtp_check, map_check, tcap_check, sccp_check, isup_check

SESSION_TIMEOUT = 10
HOST = '0.0.0.0'
PORT = 9999

sessions = {}
FSNs = [1001, 1002, 1003]
reports = {}
temp_counter = 0

Gt_map = {"1234567890": 1, "9876543210": 0}
authorized_gts = {"1112223333", "4445556666"}
known_vlrs = {"+911234567890", "+919876543210"}
transaction_ids = set()
known_components = {"Invoke", "ReturnResult", "ReturnError", "Reject"}
call_sessions = {2001, 2002, 2003}
valid_message_types = {"IAM", "ACM", "ANM", "REL", "RLC"}
imsi_requests = {}

API_REPORT_URL = "http://localhost:8000/report"

def post_report(report):
    """Send SS7 report to API."""
    try:
        response = requests.post(API_REPORT_URL, json=report)
        if response.status_code == 200:
            print("[+] Report sent successfully")
        else:
            print(f"[-] Failed to send report: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[!] Error sending report: {e}")


def parse_ss7_packet(packet):
    """Parse SS7 packet into a dictionary."""
    ss7_dict = {}
    try:
        layers = packet.split("|")
        for layer in layers:
            if not layer.strip():
                continue  
            key, values = layer.split(":", 1)
            key = key.strip()
            values = values.strip()
            try:
                ss7_dict[key] = ast.literal_eval(values)
            except Exception:
                ss7_dict[key] = values
    except Exception as e:
        print(f"Parsing Error: {e} for packet {packet}")
    return ss7_dict

def IDS_scans():
    """Scan SS7 packets and generate reports."""
    while True:
        for sid, session in sessions.copy().items():
            f = session["packets"]
            report_entry = {}
            for id, packet in f.items():
                ss7_dict = parse_ss7_packet(packet)

                if "MTP" in ss7_dict:
                    mtp_data = ss7_dict["MTP"]
                    mtp_check(id, mtp_data["opc"], mtp_data["dpc"], mtp_data["si"], mtp_data["bsn"], mtp_data["fsn"], FSNs, report_entry)
                
                if "SCCP" in ss7_dict:
                    sccp_data = ss7_dict["SCCP"]
                    sccp_check(id, sccp_data["calling_party"], sccp_data["called_party"], Gt_map, authorized_gts, report_entry)
                
                if "MAP" in ss7_dict:
                    map_data = ss7_dict["MAP"]
                    map_check(id, map_data["operation_code"], map_data["vlr_number"], map_data["imsi"], known_vlrs, imsi_requests, report_entry)
                
                if "TCAP" in ss7_dict:
                    tcap_data = ss7_dict["TCAP"]
                    tcap_check(id, tcap_data["transaction_id"], tcap_data["component"], transaction_ids, known_components, report_entry)
                
                if "ISUP" in ss7_dict:
                    isup_data = ss7_dict["ISUP"]
                    isup_check(id, isup_data["cic"], isup_data["message_type"], call_sessions, valid_message_types, report_entry)
                
            if report_entry:
                post_report(report_entry)
        
        time.sleep(3)

def start_server():
    """Start SS7 server to receive and process packets."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)

    print(f"[*] Listening on {HOST}:{PORT}")

    while True:
        client_socket, addr = server.accept()
        print(f"[*] Connection from {addr}")
        data = client_socket.recv(1024)
        if not data:
            client_socket.close()
            continue

        ss7 = data.decode()
        

        ss7_dict = parse_ss7_packet(ss7)

        sid = ss7_dict.get('Session')
        d = ss7_dict.get('Packet ID')

        if sid and d:
            if sid not in sessions:
                sessions[sid] = {"last_active": time.time(), "packets": {}, "report": []}
            sessions[sid]["last_active"] = time.time()
            sessions[sid]["packets"][d] = ss7
        else:
            print(f"[!] Missing Session or Packet ID in received data: {ss7_dict}")

        client_socket.close()

if __name__ == "__main__":
    threading.Thread(target=IDS_scans, daemon=True).start()
    start_server()
