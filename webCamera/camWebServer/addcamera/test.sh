#!/bin/bash
echo "network={" >> test.txt
echo -e "\tssid=\"$1\"" >> test.txt
echo -e "\tkey_mgmt=WPA-PSK" >> test.txt
echo -e "\tpsk=\"$2\"" >> test.txt
echo "}" >> test.txt
