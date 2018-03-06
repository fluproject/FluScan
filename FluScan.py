import socket
import pygeoip
import json
import requests
from ports import getcommonports, portscan
from ipaddress import ip_private, ip_add, ip_order
from hetrixblacklist import blacklistscan
from mongo import ConexionMongoDB

def geo(_file, _ip):
    ''' This function search the geolocation values of an IP address '''
    try:
        _geo = []
        geoDb = pygeoip.GeoIP(_file)
        ip_dictionary_values = geoDb.record_by_addr(_ip)
        ip_list_values = ip_dictionary_values.items()
        for item in ip_list_values:
            _geo.append({item[0]:item[1]})
        return _geo
    except:
        pass

def hosts(_ip):
    ''' This function search the hostnames '''
    _host = None
    try:
        hosts_values = socket.gethostbyaddr(_ip)
        _host = str(hosts_values[0])
        return _host
    except:
        return _host

def ports(_ip):
    ''' This function search open ports '''
    _ports = []
    try:
        common_ports = getcommonports()
        for value in common_ports:
            banner_exists, banner = portscan(_ip, value)
            if not banner_exists:
                _ports.append({"p":value, "name":str(common_ports[value]), "banner":str(banner)})
    except:
        pass
    return _ports

def main(_ip1, _ip2, _mongocon, _token, _analyzeblacklist):
    ''' Main function, launch the main activities '''
    conexion = ConexionMongoDB(_mongocon)
    conexion.open_conexion()
    _ip3 = _ip1
    _ip3_prev = ""
    while (_ip3_prev <> _ip2):
        if not ip_private(_ip3):
            print '[ip] '+_ip3
            try:
                document = []
                _host = hosts(_ip3)
                ip_list_values = geo('GeoIP/GeoLiteCity.dat', _ip3)
                json_ports = ports(_ip3)
                if _analyzeblacklist:
                    blacklistpages = blacklistscan(_ip3, _token)
                    dictionary = {"host":{_ip3.replace(".","_"):[{"ip":_ip3, "hostname":_host, "geo":ip_list_values, "ports":json_ports, "blacklist":blacklistpages}]}}
                else:
                    dictionary = {"host":{_ip3.replace(".","_"):[{"ip":_ip3, "hostname":_host, "geo":ip_list_values, "ports":json_ports}]}}                 
                document.append(dictionary)
                conexion.insert_doc("hosts",document)
            except ValueError:
                print 'Error on: %s > %s' % _ip3, ValueError
        _ip3_prev = _ip3
        _ip3 = ip_add(_ip3)
    conexion.close_conexion()
    del conexion

if __name__ == "__main__":
    print '[FluScan], an IPv4 scanner. Created by http://www.flu-project.com & https://www.zerolynx.com\n'
    # ************** ONLY MODIFY HERE **************
    # Step 1: Put here the first ip address
    ip1 = 'AAA.BBB.CCC.DDD'
    # Step 2: Put here the last ip address
    ip2 = 'AAA.BBB.CCC.DDD'
    # Step 3: Install MongoDB, and create a database with a named "hosts" collection
    # Step 4: Put here your connection data
    mongocon = 'mongodb://USER:PASS@MONGODB:PORT/DATABASE'
    # Step 5: Put here your Hetrix Blacklist token
    token = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # If you don't want to analyze blacklists, you can put the following flag to 'False', and you don't need to fill the previous "token" field
    analyzeblacklist = True
    # ************** ONLY MODIFY HERE **************
    ip2, ip1 = ip_order(ip1, ip2)
    main(ip1, ip2, mongocon, token, analyzeblacklist)
    