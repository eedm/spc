import socket

def fetchGammaPressure(host, pumpindex):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(2)

	try:
		s.connect((host, 23))
	except:
		print('Failed to connect to Gamma QPC')
		return False

	# First fetch prompt
	while True:
		chunk = s.recv(1)
		if chunk == b'':
			print('Failed to receive')
			s.close()
			return False
		if chunk.decode("utf-8") == ">":
			break

	# Received prompt, transmit our command
	s.send(('spc 0B '+str(pumpindex)+"\r\n").encode())

	# Wait for reply and read till end of line marker
	repl = ''
	while True:
		chunk = s.recv(1)
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

	if(repl[3] != 'MBAR\r\r\n'):
		print("Gamma QPC not set to MBAR")
		return False

	pressure = float(repl[2])
	return pressure

if __name__ == "__main__":
  import sys

  if(len(sys.argv) < 3):
    print("Usage: "+sys.argv[0]+" HOSTNAME PORT")
  else:
    try:
      host = sys.argv[1]
      index = int(sys.argv[2])

      if((index < 1) or (index > 4)):
        print("Invalid index, for QPC index has to be in range 1 to 4 inclusive")
        sys.exit()

      pressure = fetchGammaPressure(host, index)

      if(pressure == 1.3e-11):
        print("Result is 1.3e-11 mbar, this is also signalled if the QPC has no pump attached ...")
        sys.exit()

      print(str(pressure)+" mbar")
    except:
        print("Failed to query host "+host+" for pump "+str(index))