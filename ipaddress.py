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

def ip_order(_ip1, _ip2):
    try:
        _ip1_split = _ip1.split('.')
        _ip2_split = _ip2.split('.')
        for i in range(0, 4):
            if _ip2_split[i] < _ip1_split[i]:
                return _ip1, _ip2
            elif _ip2_split[i] > _ip1_split[i]:
                return _ip2, _ip1
        return _ip2, _ip1
    except:
        return _ip1, _ip2

def ip_add(_ip):
    try:
        _ip_split = _ip.split('.')
        if int(_ip_split[3]) < 255:
            return "%s.%s.%s.%d" % (_ip_split[0], _ip_split[1], _ip_split[2], int(_ip_split[3])+1)
        elif int(_ip_split[2]) < 255:
            return "%s.%s.%d.%d" % (_ip_split[0], _ip_split[1], int(_ip_split[2])+1, 0)
        elif int(_ip_split[1]) < 255:
            return "%s.%d.%d.%d" % (_ip_split[0], int(_ip_split[1])+1, 0, 0)
        elif int(_ip_split[0]) < 255:
            return "%d.%d.%d.%d" % (int(_ip_split[0])+1, 0, 0, 0)
        else:
            return _ip
    except:
        return _ip