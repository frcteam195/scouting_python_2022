#! /bin/bash

echo "Running table copy"
python3 copyTable-mark.py -dbs aws-dev -dbd pi-10 -table Computers
python3 copyTable-mark.py -dbs aws-dev -dbd pi-10 -table Users
echo "thats all folks"

