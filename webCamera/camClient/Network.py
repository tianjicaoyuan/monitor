import netifaces as ni

ni.ifaddresses('wlan0')

ip = ni.ifaddresses('wlan0')[2][0]['addr']

print (ip)
