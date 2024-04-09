import urllib
import ssl
import urllib.request

# url = ("https://www.normanok.gov/sites/default/files/documents/"
#        "2024-01/2024-01-01_daily_incident_summary.pdf")


def fetchincidents(url):
    '''This function takes the url and gets the binary data from the url'''
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"                          
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    context.verify_mode = ssl.CERT_NONE

    data = urllib.request.urlopen(urllib.request.Request(url, headers=headers), context=context).read() 
    return data



