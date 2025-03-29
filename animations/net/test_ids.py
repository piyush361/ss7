from  ss7_protocol import MTP, TCAP , SCCP ,MAP , ISUP, SS7Packet 
import random 


fsn_list = [1000]  
transaction_ids = [] 
imsi_requests = {}  

gt_map = {"1234567890": 1, "9876543210": 0}  
authorized_gts = {"1112223333", "4445556666"} 
known_vlrs = {"+911234567890", "+919876543210"}  
known_components = {"Invoke", "ReturnResult", "ReturnError", "Reject"}  
call_sessions = {2001, 2002, 2003}  
valid_message_types = {"IAM", "ACM", "ANM", "REL", "RLC"} 


def generate_MTP(fsn_list):
    opc = 124  
    dpc = 457  
    si = random.choice([3, 5, 6, 7])  

    bsn = fsn_list[-1] if fsn_list else 1000  
    fsn = bsn + 1  

    fsn_list.append(fsn)
    if len(fsn_list) > 2:
        fsn_list.pop(0) 

    return MTP(opc, dpc, si, bsn, fsn)

def generate_SCCP(gt_map, authorized_gts):
    calling_party = "1234567890"  
    called_party = random.choice(list(authorized_gts))  

    protocol_class = random.randint(0, 3)
    sequence_control = random.randint(0, 255)

    return SCCP(calling_party, called_party, protocol_class, sequence_control)

def generate_TCAP(transaction_ids, known_components):
    transaction_id = random.randint(1923,7655)
    while transaction_id  in transaction_ids:
        transaction_id=random.randint(1923,7655)

    transaction_ids.append(transaction_id)    

    dialogue_portion = "ValidDialogue" 
    component = random.choice(list(known_components))  # Use only known components

    return TCAP(transaction_id, dialogue_portion, component)

def generate_MAP(imsi_requests, known_vlrs):
    operation_code = 4  # Keep operation valid
    vlr_number = random.choice(list(known_vlrs))  # Use only known VLRs
    imsi = "404209876543210"  # Use a fixed IMSI
    msisdn = f"+91{random.randint(6000000000, 9999999999)}"  # Generate valid MSISDN

    imsi_requests[imsi] = imsi_requests.get(imsi, 0) + 1
    if imsi_requests[imsi] > 5:
        imsi_requests[imsi] = 1  # Reset before detection triggers

    return MAP(operation_code, imsi, msisdn, vlr_number)

def generate_ISUP(call_sessions, valid_message_types):
    cic = random.choice(list(call_sessions))  # Pick a valid CIC
    message_type = random.choice(list(valid_message_types))  # Pick a valid message type

    called_number = f"+91{random.randint(6000000000, 9999999999)}"
    calling_number = f"+91{random.randint(6000000000, 9999999999)}"

    return ISUP(called_number, calling_number, cic, message_type)
