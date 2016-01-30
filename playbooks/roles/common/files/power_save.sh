#!/bin/dash
find /sys/devices/pci* -path "*power/control" -exec bash -c "echo auto > '{}'" \;