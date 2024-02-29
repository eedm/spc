#
# Read and print ion pump presures for Gamma Small Pump Controller - SPCe
# Interface uses socket library to open a telnet connection to the pump controllers 1-4.
# CT 2-17-24
from datetime import datetime
import socket
import traceback

def fetchGammaPressure(host, pumpindex):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(4)

	try:
		s.connect((host, 23))
	except:
		print('Failed to connect to Gamma QPC')
		return False

	# First fetch prompt
	while True:
		try:
			chunk = s.recv(1)
		except socket.error as e:
			print(f"socket error: {e} trying to fetch prompt")
			s.close()
		if chunk == b'':
			print('Failed to receive')
			s.close()
			return False
		if chunk.decode("utf-8") == ">":
			break

	# Received prompt, transmit our command
	try:
		s.send(('spc 0B '+str(pumpindex)+"\r\n").encode())
	except socket.error as e:
		print(f"socket error: {e} trying to send query")
		s.close()
		return False
	# Wait for reply and read till end of line marker
	repl = ''
	while True:
		try:
			chunk = s.recv(1)
		except socket.error as e:
                        print(f"socket error: {e} trying to read from controller")
		if chunk == b'':
			print('Failed to receive')
			s.close()
			return False
		if chunk.decode("utf-8") == ">":
			break
		repl = repl + chunk.decode("utf-8")

	s.close()

	# Parse

	repl = repl.split(" ")

	if(len(repl) < 4):
		print("Failed to read response from GammaQPC")
		return False

	if(repl[0] != "OK"):
		print("Failed to read response from GammaQPC")
		return False

	if(repl[3] != 'TORR\r\r\n'):
		print("Gamma QPC not set to TORR")
		print(repl[3])
		return False

	pressure = float(repl[2])
	return pressure

if __name__ == "__main__":
  import sys

  if(len(sys.argv) < 3):
    print("Usage: "+sys.argv[0]+" HOSTNAME INDEX[1-4]")
  else:
    try:
      host = sys.argv[1]
      index = int(sys.argv[2])

      if((index < 1) or (index > 4)):
        print("Invalid index, for QPC index has to be in range 1 to 4 inclusive")
        sys.exit()

      pressure = fetchGammaPressure(host, index)

      if(pressure == 1.3e-11):
        print("Result is 1.3e-11 torr, this is also signalled if the QPC has no pump attached ...")
        sys.exit()

      if(pressure == 0.1e-10):
        print("Reading 0.1e-10 torr means HV OFF ...")
        sys.exit()

      now = datetime.now()
      print(now.strftime('%Y-%m-%d %H:%M:%S')+"  "+str(pressure)+" torr")
    except:
        print("Failed to query host "+host+" for pump "+str(index))
        traceback.print_exc()

