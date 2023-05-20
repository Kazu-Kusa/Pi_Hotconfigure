import fcntl
import os
import socket
import struct


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24])


def getCPUuse():
    return str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip())


def getCPUtemperature():
    res = os.popen('sudo cat /sys/class/thermal/thermal_zone0/temp').readline()
    tempfloat = float(res) / 1000
    temp = '%.1f' % tempfloat  # str(tempfloat)
    return temp + "'C"
