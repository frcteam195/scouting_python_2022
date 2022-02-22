#! /bin/bash

cd ~
python3 /Users/markmaciejewski/python-scouting/AnalysisIR.py -db $1
sleep 1
python3 /Users/markmaciejewski/python-scouting/GraphIR.py -db $1