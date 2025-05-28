# @author  Julien Gourgue
from .ieee_layer import IEEE_layer
from .mle_layer import MLE_layer

class Packet:
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.ieee = self.mle = None #Protocol we can see without decrypt
        self.pan = self.type = self.size = self.rss = self.channel = self.lqi = None
        self.extract_layers()
        self.extract_size()
        self.extract_TAP()

    def extract_layers(self):
        # Extract the IEEE layer
        if "WPAN" in self.raw_data :
            self.ieee = IEEE_layer(self.raw_data.wpan, self)
            self.type = "Thread_" + self.ieee.type 
            
            # Extract the MLE layer
            if "MLE" in self.raw_data :
                self.type = "MLE_" + self.ieee.type 
                self.mle = MLE_layer(self.raw_data, self)
                pass
        else:
            print("Reader Unknown packet no IEEE802.15.4 layer found")
            
    def extract_size(self):        
        d = dir(self.raw_data)
        if "__len__" in d:
            self.size = len(self.raw_data)
        elif "size" in d:
            self.size = self.raw_data.size
        else:
            print("Unknown packet size")
            print(dir(self.raw_data))
            self.size = -1
    
    def extract_TAP(self):
        self.rss = float(self.raw_data["WPAN-TAP"].rss)        
        self.lqi = float(self.raw_data["WPAN-TAP"].lqi)
        self.channel = self.raw_data["WPAN-TAP"].ch_num
        
            
