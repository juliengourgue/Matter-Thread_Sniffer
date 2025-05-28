# @author  Julien Gourgue
from .packet import Packet

class Device:
    def __init__(self, pan:str, sources:list):
        
        self.rloc16 = None #=short mac/IEEE
        self.long = None #=long mac/IEEE
        self.mleIpv6 = None #Address use to send MLE      
        self.pan = pan
        self.delta = None
        
        self.sources = sources
        self.packets = [] #List of Packet objects
        
    
    def prettyPrint(self, table):
        s = "Unknown" if self.rloc16 == None else self.rloc16
        l = "Unknown" if self.long == None else self.long
        v6 = "Unknown" if self.mleIpv6 == None else self.mleIpv6
        d = "Unknown" if self.delta == None else self.delta
        table.add_row([s,l,v6,d,len(self.packets)])
        
        
    def compute_packets(self):
        self.packets = []
        for s in self.sources:
            self.packets += s.packets
            
    def __str__(self):
        return f"s={self.rloc16}, l={self.long}, ipv6={self.mleIpv6}"