import socket
import pygeoip
from struct import unpack
from socket import AF_INET, inet_pton
from ports import getcommonports, portscan
from dbconnect import Dbconnect 

def geo(_file, _ip, _id):
    ''' This function search the geolocation values of an IP address '''
    try:
        geoDb = pygeoip.GeoIP(_file)
        ip_dictionary_values = geoDb.record_by_addr(_ip)
        ip_list_values = ip_dictionary_values.items()
        q = "INSERT INTO t_geo (host, city, region_code, area_code, time_zone, dma_code, metro_code, country_code3, latitude, postal_code, longitude, country_code, country_name, continent) VALUES ('%d', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s') ON DUPLICATE KEY UPDATE city='%s', region_code='%s', area_code='%s', time_zone='%s', dma_code='%s', metro_code='%s', country_code3='%s', latitude='%s', postal_code='%s', longitude='%s', country_code='%s', country_name='%s', continent='%s'" % (_id, ip_list_values[0][1], ip_list_values[1][1], ip_list_values[2][1], ip_list_values[3][1], ip_list_values[4][1], ip_list_values[5][1], ip_list_values[6][1], ip_list_values[7][1], ip_list_values[8][1], ip_list_values[9][1], ip_list_values[10][1], ip_list_values[11][1], ip_list_values[12][1], ip_list_values[0][1], ip_list_values[1][1], ip_list_values[2][1], ip_list_values[3][1], ip_list_values[4][1], ip_list_values[5][1], ip_list_values[6][1], ip_list_values[7][1], ip_list_values[8][1], ip_list_values[9][1], ip_list_values[10][1], ip_list_values[11][1], ip_list_values[12][1])
        dbcon.runquery(q)
    except:
        pass

def hosts(_ip):
    ''' This function search the hostnames '''
    _host = None
    try:
        hosts_values = socket.gethostbyaddr(_ip)
        _host = str(hosts_values[0])
        dbcon.runquery("INSERT INTO t_hosts (ip, host, date) VALUES ('%s', '%s', now()) ON DUPLICATE KEY UPDATE host='%s', date=now()" % (_ip, _host, _host))
        return dbcon.runquery("SELECT id FROM t_hosts WHERE ip='%s'" % _ip)[0][0]
    except:
        dbcon.runquery("INSERT INTO t_hosts (ip, host, date) VALUES ('%s', '%s', now()) ON DUPLICATE KEY UPDATE host='%s', date=now()" % (_ip, _host, _host))
        return dbcon.runquery("SELECT id FROM t_hosts WHERE ip='%s'" % _ip)[0][0]

def ports(_ip, _id):
    ''' This function search open ports '''
    try:
        common_ports = getcommonports()
        for value in common_ports:
            banner_exists, banner = portscan(_ip, value)
            if not banner_exists:
                dbcon.runquery("INSERT INTO t_ports (host, port, service, banner, date) VALUES ('%d', '%d', '%s', '%s', now()) ON DUPLICATE KEY UPDATE service='%s', banner='%s', date=now()" % (_id, value, str(common_ports[value]), str(banner), str(common_ports[value]), str(banner)))
    except:
        pass

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

def main(_ip1,_ip2):
    ''' Main function, launch the main activities '''
    _ip3 = _ip1
    _ip3_prev = ""
    while (_ip3_prev <> _ip2):
        if not ip_private(_ip3):
            print '[ip] '+_ip3
            try:
                _id = hosts(_ip3)
                if _id:
                    geo('GeoIP/GeoLiteCity.dat', _ip3, _id)
                    ports(_ip3, _id)
            except ValueError:
                print 'Error on: %s > %s' % _ip3, ValueError
        _ip3_prev = _ip3
        _ip3 = ip_add(_ip3)

if __name__ == "__main__":
    print '[FluScan], an IPv4 scanner. Created by http://www.flu-project.com\n'
    # ************** ONLY MODIFY HERE **************
    ip1 = '8.8.8.8' #First ip address
    ip2 = '8.8.8.8' #Last ip address
    dbinfo = {
        'dbhost': 'localhost',  #Host
        'dbuser': 'fluscan',    #User
        'dbpass': 'F1u$c4n',    #Pass
        'dbname': 'fluscan'     #Database
    }
    # ************** ONLY MODIFY HERE **************
    dbcon = Dbconnect(dbinfo)
    ip2, ip1 = ip_order(ip1, ip2)
    main(ip1, ip2)