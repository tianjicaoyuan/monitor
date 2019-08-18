#!/bin/bash
mv /etc/network/interfaces /etc/network/interfaces_middle
mv /etc/network/interfaces_wiless /etc/network/interfaces
mv /etc/network/interfaces_middle /etc/network/interfaces_wiless
