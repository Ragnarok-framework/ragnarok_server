import socketserver
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

class ServerSocket(socketserver.BaseRequestHandler):

	""" Generator for server sided secure connections with DH """

	def init_diffie_hellman(self):

		""" Initiation of the DH key exchange """

		if self.request.recv(1024).decode() != "connected":
		   print("Error while connecting")
		parameters = dh.generate_private_key()
		self.private_key = parameters.generate_private_key()
		self.peer_public_key = parameters.generate_private_key().public_key()

		# Share of public secret between server and client

		first_step = "{"
		first_step += "\"dh-keyexchange\":"
		first_step += "{"
		first_step += "\"step\": {},".format(1)
		first_step += "\"base\": {},".format(self.private_key)
		first_step += "\"publicSecret\": {}".format(self.peer_public_ke)
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
		""" Making a handle for the server for debugging and understanding """
		self.__debugflag = self.server.conn
		self.__dh = DiffieHellman.DH()

		# Echo of client IP
		print("[{}] Client connected.".format(self.client_address[0]))

		# Initiation of DH secure transport layer (from the server side)
		self.init_diffie_hellman()
		print("> The secret key is {}\n".format(self.__dh.key))
