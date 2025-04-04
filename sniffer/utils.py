import time
import pyshark
import random
import os
from .nrf802154_sniffer import Nrf802154Sniffer


def channel_founder(sniffer:Nrf802154Sniffer,dev:str, stop:bool, duration:int=10)->int:
    """
    Found witch channel is used in the Thread Network.
    Listen to each channel(from 11 to 26) until receiving enough packet to conclude that the current channel is the good one.
    Suppose that there is only one channel used in the House and that it is a Thread channel (not a Zigbee one)

    :param sniffer: Nrf802154Sniffer object
    :param dev: str path to the dongle (e.g.: /dev/ttyACM0)
    :param duration: int maximum duration of capture in seconds for each channel
    :return: int the channel where we capture data (0 if no channel found)
    """
    print(f"Channel founder start ! It will takes maximum {duration * 16} seconds to complete")
    print(f"Stop is set to {stop}")
    threshold = 1
    for i in range(11,27):
        print(f"Listen channel:{i} ...")
        fileName = str(i) + ".pcap"
        sniffer.extcap_capture(fifo=fileName, dev=dev, channel=i)
        time.sleep(duration)
        sniffer.stop_sig_handler()
        
        cap = pyshark.FileCapture(fileName)
        cap.load_packets()
        nbr_packets = len(cap)
        print(f"\tReceive {nbr_packets} packet(s)")
        isZigbee = zigbee_detector(cap, nbr_packets)
        cap.close()
        os.remove(fileName)
        
        if nbr_packets > threshold:
            if isZigbee :
                print(f"Zigbee communication found on the channel:{i}")
            else:
                print(f"Thread communication found on the channel:{i}")
                if stop : return i
    
    print(f'Cannot found any channel where received more than {threshold} packets in {duration} seconds')
    return 0


def zigbee_detector(cap, length):
    """Return true if one of the packet has a zigbee layer
    Args:
        cap : Pyshark object with all the packet already loaded
        length : Nbr of packets in the cap
    """
    if length == 0 : return False
    for i in range(length) :
        p = cap[i]
        for l in p.layers :
            l_name = l.layer_name
            if l_name.startswith("zbee") :
                return True
    return False