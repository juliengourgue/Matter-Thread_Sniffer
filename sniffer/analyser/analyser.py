# @author  Julien Gourgue

#Module imports
import pyshark
import ipaddress
from prettytable import PrettyTable
#Local imports
from .packet import Packet
from .packetExchange import PacketExchange
from .device import Device
from .source import Source

class Analyser:
    def __init__(self, path:str):
        self.path = path
        self.MLE_packets = []
        self.Thread_packets = []
        self.nbr_packets = 0
        self.sources = {}
        self.packet_exchange = {} #Key is tuple(sorted(src, dst)) and value is PacketExchange object
        self.channel = -1
        self.cap = None
        self.devices = []

        self._pcap_reader()
        self._ipV6_to_device()

    def _pcap_reader(self):
        self.cap = pyshark.FileCapture(self.path)
        self.cap.load_packets()

        for packet in self.cap:
            packet_obj = Packet(packet)
            self.nbr_packets += 1
            if(self.channel == -1 and packet_obj.channel!=None):
                self.channel = packet_obj.channel
            #Thread packet
            if(packet_obj.type.startswith("Thread")):
                self._thread_packet(packet_obj)
            #Mle packet
            elif(packet_obj.type.startswith("MLE")):
                self._mle_packet(packet_obj)
            

    def _thread_packet(self, packet_obj):
            self.Thread_packets.append(packet_obj)
            if(packet_obj.ieee.type == "Data"):
                    self._add_to_source(packet_obj)

            self._packet_exchange(packet_obj)


    def _mle_packet(self, packet_obj):
        self.MLE_packets.append(packet_obj)
        self._packet_exchange(packet_obj)     
        self._add_to_source(packet_obj)   
    
            
    def _packet_exchange(self, packet_obj):
        if(packet_obj.ieee.src == None or packet_obj.ieee.dst == None):
            return None
        key = tuple(sorted([packet_obj.ieee.src, packet_obj.ieee.dst]))
        if key not in self.packet_exchange:
            self.packet_exchange[key] = PacketExchange(packet_obj.ieee.src, packet_obj.ieee.dst, packet_obj.type)
        self.packet_exchange[key].add_packet(packet_obj)

    def _add_to_source(self, packet_obj):
        if(packet_obj.ieee.src == None): return None
        if packet_obj.ieee.src not in self.sources:
            self.sources[packet_obj.ieee.src] = Source(packet_obj.ieee.src, packet_obj.pan, packet_obj.type)
        self.sources[packet_obj.ieee.src].add_packet(packet_obj)

    def _ipV6_to_device(self) :
        self.devices = []
        
        # Create a device for each long address
        for s in self.sources.values():
            if s.type == "long_address":
                d = Device(s.pan, [s])
                d.long = s.addr
                d.mleIpv6 = s.packets[0].mle.src
                self.devices.append(d)
        rloc_device_rss = []   #[(rloc16, bestDelta, Source, Device)]
        
        #Iterate over each devices for each short address
        # Each short address choose its best long address device
        for s in self.sources.values():
            if s.type == "short_address":
                current_min = (1000, None) #(delta, device)
                for d in self.devices:
                    lqi_rloc = s.get_rss_mean()
                    lqi_device = d.sources[0].get_rss_mean()
                    delta = abs(lqi_rloc - lqi_device)
                    if delta < current_min[0] : current_min = (delta, d)
                rloc_device_rss.append((s.addr, current_min[0], s, current_min[1]))
        
        #Iterate through the choose made to verify which one should be link with each device
        for i in range(0, len(rloc_device_rss)):
            if rloc_device_rss[i][1] == -1 : continue
            alone = True
            for j in range(i+1, len(rloc_device_rss)):
                #Two short address choose the same better device and J is better than i
                if rloc_device_rss[i][3].long == rloc_device_rss[j][3].long and not (rloc_device_rss[i][1] <= rloc_device_rss[j][1]) :
                    alone = False
                    break
            #No one choose the same
            if alone:
                rloc_device_rss[i][3].rloc16 = rloc_device_rss[i][0]
                rloc_device_rss[i][3].delta = round(rloc_device_rss[i][1], 3)
                rloc_device_rss[i][3].sources.append(rloc_device_rss[i][2])
                
                    
    def printer(self):
        print("========================================")
        print(f"Number of packets: {self.nbr_packets}")
        print(f"Thread packets: {len(self.Thread_packets)}")
        print(f"MLE packets: {len(self.MLE_packets)}")
        for key in self.packet_exchange:
            print(self.packet_exchange[key])
        
        for key in self.rloc_devices:
            print(self.rloc_devices[key])
         
            
    def _is_valid_ipv6(self, ip):
        try:
            ipaddress.IPv6Address(ip)
            return True
        except ipaddress.AddressValueError:
            return False


    def close(self):
        self.cap.close()
        self.cap = None
