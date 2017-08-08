#!/bin/sh
tail -F /var/log/switch.log | sh new-classfier.sh
