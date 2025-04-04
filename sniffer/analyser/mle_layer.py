#Class to represent layer in MLE packet under the IEEE802.15.4
#6LoWPAN + IPv6 + UDP + MLE
multicast_ipv6 = ["ff02::1", "ff02::2", "ff03::1", "ff03::2"]

class MLE_layer():
    def __init__(self, wpan_raw_data, packet_obj):
        self.raw_data = wpan_raw_data
        self.packet_obj = packet_obj
        self.type = None
        self.data_length=None #TODO
        self.src = self.dst = None #IPv6
        self.extract_data()
        
    def extract_data(self):
        if "6LOWPAN" in self.raw_data :
            data = self.raw_data["6LOWPAN"]
            if(data.has_field("src")) : self.src = data.src
            if(data.has_field("dst")) : self.dst = data.dst
        else :
            print("MLE unknown")
           
    def compute_type(self):
        if self.dst in multicast_ipv6 :
            self.type = "Multicast"
        else:
            self.type = "MLE unknown ?" 