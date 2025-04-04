import click
import time
from prettytable import PrettyTable
from .nrf802154_sniffer import Nrf802154Sniffer
from .utils import channel_founder as cf
from .analyser.analyser_cli import CliAnalyser

@click.group
def sniff():
    pass

@click.command(help="Sniff IEEE802.15.4 packets over the air on a specified channel and save them in a pcap file at [PATH]")
@click.argument("path")
@click.option("--dev", type=click.Path(exists=True), required=True, help="The path of the NRF dongle. Use `ls dev/tty*` to list available serial devices")
@click.option("-c", "--channel",type=click.IntRange(11, 26), prompt="Enter the channel number", help="Enter the channel to capture", required=True)
@click.option("-f","--pcap_file", type=str ,help="Name of the pcap file in witch the captured data will be store")
@click.option("--duration", type=int, help="Stop the capture after [duration] seconds", default=5)
def capture(path, channel, pcap_file, duration, dev) :
    if path[-1] != '/': path += '/'
    filename = path + pcap_file+'.pcap' if pcap_file is not None else f"{path}sniff_{int(time.time() * 1000)}.pcap"
    sniffer = Nrf802154Sniffer()
    if channel is None :
        channel = channel_founder(sniffer, dev, duration=5)
        pass 
    
    print(f"Start capturing IEEE802.15.4 packet on the channel:{channel} during {duration} seconds ...")
    sniffer.extcap_capture(fifo=filename, dev=dev, channel=channel, metadata="ieee802154-tap")
    time.sleep(duration)
    sniffer.stop_sig_handler()
    print(f"Capture finished and saved in {filename}")



@click.command(help="Determine if there is communication on one of the channels (from 11 to 26) and returns the first channel where it captures packets.")
@click.option("--dev", type=click.Path(exists=True), required=True, help="The path of the NRF dongle. Use `ls dev/tty*` to list available serial devices")
@click.option("--stop", required=False, help="By default set to True if set to False, the channel founder will listen every channel doesn't stop until the end" )
def channel_founder(dev, stop):
    sniffer = Nrf802154Sniffer()
    stop = bool(stop)
    if stop == False:
        cf(sniffer, dev, False)
    else:
        cf(sniffer, dev, True)

@click.command(help="Start the analyser CLI on the pcap file specified by PATH")
@click.argument("path", type=click.Path(exists=True))
def analyser_cli(path):
    CliAnalyser(path)

sniff.add_command(capture)
sniff.add_command(channel_founder)
sniff.add_command(analyser_cli)


if __name__ == "__main__":
    sniff()