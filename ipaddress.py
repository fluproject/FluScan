from struct import unpack
from socket import AF_INET, inet_pton

def ip_private(_ip):
    ip = unpack('!I',inet_pton(AF_INET,_ip))[0]
    l = (
        [2130706432, 4278190080],
        [3232235520, 4294901760],
        [2886729728, 4293918720],
        [167772160, 4278190080]
    )
    for addr in l:
        if (ip & addr[1]) == addr[0]:
            return True
    return False