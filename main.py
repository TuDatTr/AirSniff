#!/usr/bin/python
import binascii
import logging
import os
import socket
import sys


import checker
logger=logging.getLogger('AirSniff')

def set_monitor_mode(interface):
    os.system('ifconfig {} down'.format(interface))
    os.system('iwconfig {} mode monitor'.format(interface))
    os.system('ifconfig {} up'.format(interface))

def probe_filter(package):
    # 0x40 as the 36th byte is the indicator of the package being a
    # probe request package and we don't want to collect the broadcasts,
    # hence filtering out the packages with an 0x00
    if (package[36:37] == b'\x40') and (package[61:62] != b'\x00'):
        ssidlen = int.from_bytes(package[61:62], byteorder='big')
        ssid = package[62:62 + ssidlen].decode(encoding='utf-8')
        transmitter = str(binascii.hexlify(bytes(package[46:46+6])))[2:-1]
        transmitter = ':'.join([transmitter[i:i+2] for i in range(0,len(transmitter),2)])
        return [transmitter, ssid]
    else:
        return None

    
def start_loop(interface):
    rawSocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
    rawSocket.bind((interface, 0x0004))

    while True:
        pkt = rawSocket.recvfrom(2048)[0]
        filtered_package = probe_filter(pkt)
        if filtered_package:
            print(filtered_package)
        
    
def main():
    if '-i' in sys.argv:
        interface_index = sys.argv.index('-i')+1
        interface = sys.argv[interface_index]
        if checker.valid_interface(interface):
            if not checker.is_interface_mode(interface):
#                    try:
                set_monitor_mode(interface)
#                    except:
#                       logger.error('Try sudo.')
                start_loop(interface)

    else:
        logger.error('Device wasn\'t specified.')

if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    fh=logging.FileHandler('debug.log')
    fh.setLevel(logging.DEBUG)
    ch=logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    logger.addHandler(ch)
    main()
