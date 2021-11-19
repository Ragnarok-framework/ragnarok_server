import argparse
from threading import Thread, Lock
import socket
from queue import Queue

queue = Queue()

class PortFinder:
    def pscan(self, port):
        """ Port scanner made to discover services and addresses (optimised with multithreading) """
        try:
            starter = socket.socket()
            starter.connect((target_ip, port))
        except:
            with Lock():
                skippable = True
        else:
            with Lock():
                protocol = 'tcp'
                print("Port: %s => %s" %(port, socket.getservbyport(port, protocol)))
        finally:
            starter.close()

    def scan_thread(self):
        """ Initiation of the scanner """
        global queue
        while True:
            num = queue.get()
            PortFinder().pscan(num)
            queue.task_done()

    def main(self, target_ip, ports):
        """ Definiton of the ip to be scanned using a priority queue """
        global queue
        N_THREADS = 100
        for thread in range (N_THREADS):
            thread = Thread(target = PortFinder().scan_thread)
            thread.daemon = True
            thread.start()
        for num in ports:
            queue.put(num)
        queue.join()

#if __name__ == "__main__":
#    parser = argparse.ArgumentParser(description="Simple port scanner")
#    parser.add_argument("target_ip", help="target_ip to scan.")
#    parser.add_argument("--ports", "-p", dest="port_range", default="1-65535", help="Port range to scan, default is 1-65535 (all ports)")
#    args = parser.parse_args()
#    target_ip, port_range = args.target_ip, args.port_range
#
#    start_port, end_port = port_range.split("-")
#    start_port, end_port = int(start_port), int(end_port)
#
#    ports = [ p for p in range(start_port, end_port)]
#    PortFinder().main(target_ip, ports)
