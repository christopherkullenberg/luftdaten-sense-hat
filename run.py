import luftdata
import sys

luftdata.startup(10136)

try:
    while True:
        luftdata.runPIR(10136)

except KeyboardInterrupt:
    luftdata.cleardisplay()
    sys.exit()
