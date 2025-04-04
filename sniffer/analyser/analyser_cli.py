from prettytable import PrettyTable
from .analyser import Analyser


class CliAnalyser :
    def __init__(self, path):
        self.path = path
        intro = f"""
            Welcome to the analyser CLI ! \n
            This CLI will help you to analyse the pcap file: {path} \n
            Type 'help' to see the available commands. \n
            Type 'exit' to exit the CLI. \n
            Loading the pcap file...
        """
        print(intro)
        self.analyser = Analyser(path)
        print("File loaded !")
        self.run()

        
    def help(self):
        print("Available commands:")
        print("\tchannel: print the channel used to capture the pcap file")
        print("\tnbr_packets: print the number of packets in the pcap file")
        print("\tcommunications [x]: print the communication between each src and dst pair\n\t\tsort the table by the xth columns (0 by default)")
        print("\tsources [x]: print informations for each source address of the IEEE layer\n\t\tsort the table by the xth columns (0 by default)")
        print("\tdevices [x]: link Thread packet and MLE packet to get all device information based on their LQI = !extrapolation  \n\t\tsort the table by the xth columns (0 by default)")    
        print("\tpacket [x]:  print the xth packet of the pcap file")
        print("\texit: exit the CLI")
        print("\thelp: print this message")

        
    def nbr_packets(self):
        pretty = PrettyTable()
        pretty.field_names = ["Number of packets", "Thread packets", "MLE packets"]
        pretty.add_row([self.analyser.nbr_packets, len(self.analyser.Thread_packets), len(self.analyser.MLE_packets)])
        print(pretty)

    def communication(self, sortID=0):
        table = PrettyTable()
        table.field_names = ["Communication type", "Address IEEE802.15.4 A", "Address IEEE802.15.4 B", "#Packets A->B", "#Packets B->A"]
        for key in self.analyser.packet_exchange:
            self.analyser.packet_exchange[key].prettyPrint(table)
        table.sortby = table.field_names[sortID]
        print(table)
    
    def devices(self, sortID=0):
        table = PrettyTable()
        table.field_names=["Short IEEE 802.15.4 address", "Long IEEE 802.15.4 address", "IPv6", "LQI delta between IEEE802.15.4 and MLE" ,"#Packets"]
        for d in self.analyser.devices :
            d.compute_packets()
            d.prettyPrint(table)
        table.sortby = table.field_names[sortID]
        print("/!\ MLE packets and Thread packet are used to extrapolate the result of this table. The result may be false")  
        print(table) 
    
    def sources(self, sortID=0):
        table = PrettyTable()
        table.field_names = ["IEEE802.15.4 Address", "Address type", "PAN", "Mean RSS(dBm)", "Mean LQI", "#Packets sent"]
        for key in self.analyser.sources:
            self.analyser.sources[key].prettyPrint(table)
        table.sortby = table.field_names[sortID]
        print(table)
        
    def exit(self):
        print("Exiting the CLI...")
        self.analyser.close()   
        
    def run(self):
        while True:
        
            
            command = input("> ")

            commands = {
                "help": self.help,
                "exit": self.exit,
                "nbr_packets": self.nbr_packets,
                "communications": self.communication,
                "sources": self.sources,
                "channel": lambda: print(f"Channel: {self.analyser.channel}"),
                "devices" : self.devices,
            }

            if command in commands:
                if command == "exit":
                    commands[command]()
                    break
                else:
                    commands[command]()
            elif command.startswith("packet"):
                try:
                    index = int(command.split(" ")[1])
                    print(self.analyser.cap[index])
                except ValueError:
                    print("Invalid index")
                    
            elif command.startswith("sources"):
                try:
                    sortID = int(command.split(" ")[1])
                    self.sources(sortID)
                except :
                    print(f"Unable to sort the table by the column {sortID}")
                    
            elif command.startswith("communications"):
                try:
                    sortID = int(command.split(" ")[1])
                    self.communication(sortID)
                except :
                    print(f"Unable to sort the table by the column {sortID}")
                    
            elif command.startswith("devices"):
                try:
                    sortID = int(command.split(" ")[1])
                    self.devices(sortID)
                except :
                    print(f"Unable to sort the table by the column {sortID}")        
                    
            else:
                print("Unknown command type `help` to show available commands")