def mtp_check(session_id, opc, dpc, si, bsn, fsn, fsn_list, reports):
    session_opc = set()
    session_dpc = set()
    
    session_opc.add(opc)
    session_dpc.add(dpc)
    
    if session_id not in reports:
        reports[session_id] = []
    
    if len(session_opc) > 1 or len(session_dpc) > 1:
        reports[session_id].append("Suspicious activity detected in MTP.")
    
    if si not in {3, 5, 6, 7}:
        reports[session_id].append("Invalid service indicator in MTP.")
    
    if bsn != fsn_list[-1]:
        reports[session_id].append("Possible acknowledgment manipulation in MTP.")
    
    if fsn_list[-1] - fsn_list[-2] != 1:
        reports[session_id].append("Packet loss, injection, or replay attack detected in MTP.")

def sccp_check(session_id, calling_party, called_party, gt_map, authorized_gts, reports):
    if session_id not in reports:
        reports[session_id] = []
    
    if gt_map.get(calling_party, 0) == 0:
        reports[session_id].append("Unauthorized calling party in SCCP.")
    
    if gt_map.get(called_party) not in authorized_gts:
        reports[session_id].append("Unauthorized called party in SCCP.")

def map_check(session_id, operation_code, vlr_number, imsi, known_vlrs, imsi_requests, reports):
    if session_id not in reports:
        reports[session_id] = []
    
    if operation_code != 4 and vlr_number not in known_vlrs:
        reports[session_id].append("Unknown VLR detected in MAP.")
    
    imsi_requests[imsi] = imsi_requests.get(imsi, 0) + 1
    
    if imsi_requests[imsi] > 5:
        reports[session_id].append("Suspicious high number of IMSI requests detected in MAP.")

def tcap_check(session_id, transaction_id, component, transaction_ids, known_components, reports):
    if session_id not in reports:
        reports[session_id] = []
    
    if transaction_id in transaction_ids:
        reports[session_id].append("Transaction ID reuse detected in TCAP.")
    
    if component not in known_components:
        reports[session_id].append("Unknown TCAP component detected.")
    
    transaction_ids.add(transaction_id)

def isup_check(session_id, cic, message_type, call_sessions, valid_message_types, reports):
    if session_id not in reports:
        reports[session_id] = []
    
    if cic not in call_sessions:
        reports[session_id].append("Invalid Call Circuit detected in ISUP.")
    
    if message_type not in valid_message_types:
        reports[session_id].append("Unexpected ISUP message type detected.")
    
    call_sessions.add(cic)
