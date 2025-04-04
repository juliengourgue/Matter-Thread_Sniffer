from prettytable import PrettyTable

class PacketExchange:
    def __init__(self, device_A:str, device_B:str, type:str):
        self.type = type
        self.device_A = device_A
        self.device_B = device_B
        self.from_A_to_B = []
        self.from_B_to_A = []
    
    def get_nbr_packets(self) -> int:
        return len(self.from_A_to_B) + len(self.from_B_to_A)
    
    def get_nbr_packets_A_to_B(self) -> int:
        return len(self.from_A_to_B)
    
    def get_nbr_packets_B_to_A(self) -> int:
        return len(self.from_B_to_A)
    
    def get_device_A(self) -> str:
        return self.device_A
    
    def get_device_B(self) -> str:
        return self.device_B
    
    def add_packet(self, packet_obj):
        if packet_obj.ieee.src == self.device_A and packet_obj.ieee.dst == self.device_B:
            self.from_A_to_B.append(packet_obj)
        elif packet_obj.ieee.src == self.device_B and packet_obj.ieee.dst == self.device_A:
            self.from_B_to_A.append(packet_obj)
        else:
            print("Error in PacketExchange.add_packet")
    
    def addToTable(self, x:PrettyTable):
        x.add_row([self.device_A, self.device_B, len(self.from_A_to_B)])
        x.add_row([self.device_B, self.device_A, len(self.from_B_to_A)])
        return str(x)
    
    def prettyPrint(self, table:PrettyTable):        
        table.add_row([self.type, self.device_A, self.device_B, len(self.from_A_to_B), len(self.from_B_to_A)])
        
    
    def __str__(self):
        string = f"Communication between {self.device_A} and {self.device_B}\n"
        string += f"\t communication type: {self.type}\n"
        if self.device_A != "0xffff":
            string += f"\t Communication from {self.device_A} to {self.device_B}\n"
            string += f"\t\t #Packets: {self.get_nbr_packets_A_to_B()}\n"
            
        if self.device_B != "0xffff":
            string += f"\t Communication from {self.device_B} to {self.device_A}\n"
            string += f"\t\t #Packets: {self.get_nbr_packets_B_to_A()}\n"
        return string