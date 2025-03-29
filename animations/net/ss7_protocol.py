class MTP:
    def __init__(self, opc, dpc, si,bsn,fsn):
        self.opc = opc 
        self.dpc = dpc 
        self.si = si 
        self.bsn = bsn
        self.fsn = fsn 

class SCCP:
    def __init__(self, calling_party, called_party, protocol_class, sequence_control):
        self.calling_party = calling_party  
        self.called_party = called_party  
        self.protocol_class = protocol_class  
        self.sequence_control = sequence_control  

class TCAP:
    def __init__(self, transaction_id, dialogue_portion, component):
        self.transaction_id = transaction_id 
        self.dialogue_portion = dialogue_portion  
        self.component = component 

class MAP:
    def __init__(self, operation_code, imsi, msisdn, vlr_number):
        self.operation_code = operation_code  
        self.imsi = imsi  
        self.msisdn = msisdn  
        self.vlr_number = vlr_number  

class ISUP:
    def __init__(self, called_number, calling_number, cic, message_type):
        self.called_number = called_number  
        self.calling_number = calling_number  
        self.cic = cic  
        self.message_type = message_type  

class SS7Packet:
    def __init__(self, mtp, sccp, tcap=None, map=None, isup=None):
        self.mtp = mtp
        self.sccp = sccp
        self.tcap = tcap
        self.map = map
        self.isup = isup

    def to_dict(self):  # 
        return {
            "MTP": self.mtp.__dict__,
            "SCCP": self.sccp.__dict__,
            "TCAP": self.tcap.__dict__ if self.tcap else None,
            "MAP": self.map.__dict__ if self.map else None,
            "ISUP": self.isup.__dict__ if self.isup else None,
        }  
