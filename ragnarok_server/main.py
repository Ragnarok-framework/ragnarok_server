from server import ServerSocket
from argparse import ArgumentParser


class Main:


	def main(self):
		""" Executing parse data """
		parser = ArgumentParser()
		parser.add_argument("-d", "--debug", dest="debug", required=False,
	                    help="to print debug messages, enable this option",
	                    action="store_true"
						)
		args = parser.parse_args()

		if args.debug:
		   print(args)
	def start_server(debugflag):
		# Start of the server then initiation of the serve forever
		server = socketserver.ThreadingTCPServer(("", 50000), ServerSocket)
		server.conn = debugflag
		server.serve_forever()
		Server.start_server(args.debug)

if __name__ == '__main__':
   Main().main()
