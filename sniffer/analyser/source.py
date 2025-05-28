# @author  Julien Gourgue
from .packet import Packet

#Class thar represent source at the IEEE Layer (MAC)
class Source:
    def __init__(self, addr:str, pan:str, typ:str):
        self.addr = addr
        self.packet_type = typ
        self.pan = pan
        self.rss = []
        self.lqi = []
        self.packets = [] #List of Packet objects
        self.type = self.getType()
        
    def getType(self):
        if(self.packet_type.startswith("Thread")):
            return "short_address"
        
        else:
            return "long_address"
                
        
    def add_packet(self, packet:Packet):
        self.packets.append(packet)
        self.rss.append(packet.rss)
        self.lqi.append(packet.lqi)
    
    def get_rloc16(self) -> str:
        return self.rloc16
    
    def get_pan(self) -> str:
        return self.pan
    
    def get_rss_mean(self) -> float:
        if len(self.rss) == 0:
            return 0
        return round(sum(self.rss) / len(self.rss), 2)
    
    def get_lqi_mean(self) -> float:
        if len(self.lqi) == 0:
            return 0
        return round(sum(self.lqi) / len(self.lqi), 2)
        
    def prettyPrint(self, table):
        table.add_row([self.addr,self.type ,self.pan, self.get_rss_mean(), self.get_lqi_mean() ,len(self.packets)])