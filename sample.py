import gammaqpc

import sys

if(len(sys.argv) < 3):
  print("Usage: "+sys.argv[0]+" HOSTNAME PORT")
  sys.exit()

try:
  host = sys.argv[1]
  index = int(sys.argv[2])

  if((index < 1) or (index > 4)):
    print("Invalid index, for QPC index has to be in range 1 to 4 inclusive")
    sys.exit()

  pressure = gammaqpc.fetchGammaPressure(host, index)

  if(pressure == 1.3e-11):
    print("Result is 1.3e-11 mbar, this is also signalled if the QPC has no pump attached ...")
    sys.exit()

  print(str(pressure)+" mbar")
except:
  print("Failed to query host "+host+" for pump "+str(index))