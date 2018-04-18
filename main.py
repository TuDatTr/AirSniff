#!/usr/bin/python
import logging
import sys


import checker
logger=logging.getLogger('AirSniff')





def main():
    if '-i' in sys.argv:
        interface_index = sys.argv.index('-i')+1
        interface = sys.argv[interface_index]
        if checker.valid_interface(interface):
            
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
