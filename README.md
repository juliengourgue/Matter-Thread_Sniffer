# IEEE802.15.4 Packet Sniffer 

## Introduction

This sniffer capture IEEE802.15.4 packets to analyze them.
This project is focus on the **Matter/Thread** protocol.
The sniffer is a CLI tool made in Python using the Click library.

To capture packet over the NRF52840 Dongle the sniffer use the Python module developed by  Nordic Semiconductor ASA : 
[nrf802154_sniffer.py](https://github.com/NordicSemiconductor/nRF-Sniffer-for-802.15.4/blob/master/nrf802154_sniffer/nrf802154_sniffer.py)


## Usage

Start by enabling the venv :
```
source venv/bin/activate  
```

### capture

```
Usage: sniff capture [OPTIONS] PATH

  Sniff IEEE802.15.4 packets over the air on a specified channel and
  save them in a pcap file at [PATH]

Options:
  --dev PATH                   The path of the NRF dongle. Use `ls dev/tty*`
                               to list available serial devices  [required]
  -c, --channel INTEGER RANGE  Enter the channel to capture  [11<=x<=26;
                               required]
  -f, --pcap_file PATH         Path for the pcap file in witch the captured
                               data will be store
  --duration INTEGER           Stop the capture after [duration] seconds
  --help                       Show this message and exit.
```



#### Example utilization :

- `-c 15` listens for communication on channel 15.
- `--dev` pecifies the path to the NRF52840 Dongle (which can be found using `ls /dev/tty*`).
- `-f` specifies the filename where the capture will be saved.
- `--duration 15` specifies that we want to capture packets for 15 seconds.
- `.` specifies that we want to save the pcap file in the current directory.

```bash
sniff start-capture -c 15 --dev /dev/ttyACM0 -f test --duration 15 .
```

The output will be :

```
Start capturing IEEE802.15.4 packets on the channel:15 during 15 seconds ...
Capture finished and saved in ./test.pcap
```

### channel-founder

```
Usage: sniff channel-founder [OPTIONS]

  Determine if there is communication on one of the channels (from 11 to 26) and
  returns the first channel where it captures packets.

Options:
  --dev PATH  The path of the NRF dongle. Use `ls dev/tty*` to list available
              serial devices  [required]
  --help      Show this message and exit.

```

### analyser-cli
```
Usage: sniff analyser-cli [OPTIONS] PATH

  Start the analyser CLI on the pcap file specified by PATH

Options:
  --help  Show this message and exit.
```


## Requirements

- `Python3` the code is tested on Python 3.12.3

- `Tyshark` can be install like that :
   ``` bash
   sudo apt install tshark
   ```

## Installation

Clone the repository:

```bash
git clone https://github.com/juliengourgue/Matter-Thread_Sniffer.git
cd MaThPot/sniffer
```
## Configuration

First of all, you need hardware capable to capture IEEE 802.15.4 packets. In this project, we used the NRF52840 Dongle.


### NRF52840 Sniffer Configuration

To be able to capture packets, you have to flash the NRF dongle with the sniffer tool. To do so you can follow the steps described here : [nRF-Sniffer-for-802.15.4](https://github.com/NordicSemiconductor/nRF-Sniffer-for-802.15.4)


### Sniffer configuration
1. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  
   ```
2. Install the project dependencies:
   ```bash
   pip install -r requirements.txt
   pip install --editable .
   ```

