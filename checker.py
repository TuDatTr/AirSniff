import os
import subprocess


def valid_interface(iface):
    'Checks if the chosen interface exists.'
    return iface in os.listdir('/sys/class/net/')


def is_interface_mode(iface):
    'Returns the wireless mode of the wireless interface'
    terminalOutput = subprocess.Popen(['iwconfig', iface], stdout=subprocess.PIPE).communicate()[0]
    mode = terminalOutput.decode('utf-8').partition('Mode:')[2].partition('  ')[0]
    return mode == 'monitor'
