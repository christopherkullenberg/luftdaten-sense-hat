import luftdata
import sys

luftdata.startup(10803)

try:
    while True:
        luftdata.runPIR(10803)

except KeyboardInterrupt:
    luftdata.cleardisplay()
    sys.exit()
