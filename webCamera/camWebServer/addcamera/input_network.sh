#!/bin/bash 
echo "network={" >> wpa_supplicant.conf
echo -e "\tssid=\"$1\"" >> wpa_supplicant.conf
echo -e "\tkey_mgmt=WPA-PSK" >> wpa_supplicant.conf
echo -e "\tpsk=\"$2\"" >> wpa_supplicant.conf
echo "}" >> wpa_supplicant.conf
