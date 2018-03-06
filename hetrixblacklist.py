import requests
import json

def blacklistscan(_host, _token):
    ''' This function execute a blacklist scan '''
    n = 0
    url = 'https://api.hetrixtools.com/v2/'+_token+'/blacklist-check/ipv4/'+_host+'/'
    try:
        resp=requests.get(url, verify=False)
        data = json.loads(resp.text)
        n = data["blacklisted_count"]
    except:
        pass
    return n