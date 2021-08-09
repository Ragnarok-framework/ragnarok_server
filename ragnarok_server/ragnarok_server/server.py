import socketserver
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import json

class ServerSocket(socketserver.BaseRequestHandler):
	""" Generator for server sided secure connections with DH """
	def initDiffieHellman(self):
		if self.request.recv(1024).decode() != "connected":
			print("Error while connecting")

		publicSecret = self.__dh.calcPublicSecret()

		# Share of public secret between server and client
		first_step = "{"
		first_step += "\"dh-keyexchange\":"
		first_step += "{"
		first_step += "\"step\": {},".format(1)
		first_step += "\"base\": {},".format(self.__dh.base)
		first_step += "\"prime\": {},".format(self.__dh.sharedPrime)
		first_step += "\"publicSecret\": {}".format(publicSecret)
		first_step += "}}"
		self.request.send(first_step.encode())

		# Exchange of the new public secret
		second_step = self.request.recv(1024)

		if self.__debugflag:
			print(second_step)

		# Parsing the DH data in json form for better readability
		jsonData = json.loads(second_step.decode())
		jsonData = jsonData["dh-keyexchange"]

		publicSecret = int(jsonData["publicSecret"])

		# calculation of shared secret
		self.__dh.calcSharedSecret(publicSecret)

	# Definition function for client detection
	def handle(self):
		self.__debugflag = self.server.conn
		self.__dh = DiffieHellman.DH()

		# Echo of client IP
		print("[{}] Client connected.".format(self.client_address[0]))

		# Initiation of DH secure transport layer (from the server side)
		self.initDiffieHellman()
		print("> The secret key is {}\n".format(self.__dh.key))

def start_server(debugflag):
	# Start of the server then initiation of the serve forever
	server = socketserver.ThreadingTCPServer(("", 50000), ServerSocket)
	server.conn = debugflag
	server.serve_forever()
