#!/bin/bash
# Bash-script which executes the python-script cal.py, waits for it to finish and then runs screenshot.py


# Execute the python-script cal.py
python3 cal.py

# Wait for the python-script to finish
wait

# Execute the python-script screenshot.py
python3 screenshot.py

convert screenshot.png -set colorspace Gray -define png:color-type=0 PNG24:out2.png