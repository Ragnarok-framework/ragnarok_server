from server import server_socket
from argparse import ArgumentParser

class Main:

	def main(self):
		""" Step 1: executing parse data """
		parser = ArgumentParser()
		parser.add_argument("-m", "--mode", dest="mode", type=str, required=True,
	                    help="SERVER to start a server"
	                    )

		parser.add_argument("-d", "--debug", dest="debug", required=False,
	                    help="to print debug messages, enable this option",
	                    action="store_true"
	                    )

		args = parser.parse_args()

		if args.debug:
		   print(args)
		   """ Step 2: Getting input for socket data and API definiton """
		if args.mode.lower() == "server":
	       Server.start_server(args.debug)
def run():
	if __name__ == '__main__':
		Main().main()
