#!/bin/bash
echo "running rescueorg.py"
cd /home/ubuntu/pawsforalarm
source secrets.sh
source env/bin/activate
#https://stackoverflow.com/a/876242
python3 rescueorg.py >> /home/ubuntu/pawsforalarm.log 2>&1
echo "completed running rescueorg.py"