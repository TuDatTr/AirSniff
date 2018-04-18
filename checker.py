import os

def valid_interface(iface):
    'Checks if the chosen interface exists.'
    return iface in os.listdir('/sys/class/net/')



        
        
