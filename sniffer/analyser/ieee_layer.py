class IEEE_layer():
    def __init__(self, wpan_raw_data, packet_obj):
        self.wpan_raw_data = wpan_raw_data
        self.packet_obj = packet_obj
        self.type = None
        self.data_length=None
        self.src = self.dst = None #Src and Dst of the IEEE layer / MAC
        self.extract_data()

    def __str__(self):
        return f"Packet type: {self.type}, Source: {self.src}, Destination: {self.dst}, Size: {self.size}"
    
    def extract_data(self):
        wpan_layer = self.wpan_raw_data
        
        #ack packet
        if wpan_layer.frame_type.int_value == 2 :
            self.type = "Ack"
            return
        
        #data packet   
        elif wpan_layer.frame_type.int_value == 1:
            self.type = "Data"
            self.packet_obj.pan = wpan_layer.dst_pan
                 
            if(wpan_layer.has_field('src16') and wpan_layer.has_field('dst16')):
                self.src = wpan_layer.src16
                self.dst = wpan_layer.dst16
                if self.dst == '0xffff': self.type+="_Broadcast"
        
            elif(wpan_layer.has_field('dst16') and wpan_layer.has_field('src64')):
                self.src = wpan_layer.src64
                self.dst = wpan_layer.dst16
                self.type+="_Broadcast_IPv6"
            
            elif(wpan_layer.has_field('dst64') and wpan_layer.has_field('src64')):
                self.src = wpan_layer.src64
                self.dst = wpan_layer.dst64
                self.type += "_IPv6"
        