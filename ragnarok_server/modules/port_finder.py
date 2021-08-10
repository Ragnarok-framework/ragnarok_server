import argparse
from threading import Thread, Lock
import socket
from queue import Queue

class PortFinder:
    N_THREADS = 100
    queue = Queue()
    protocol = 'tcp'
    def pscan(port):
        """ Port scanner made to discover services and addresses optimised with multithreading """
        try:
            starter = socket.socket()
            starter.connect((target_ip, port))
        except:
            with Lock():
                skippable = True
        else:
            with Lock():
                print("Port: %s => %s" %(port, socket.getservbyport(port, pro)))
        finally:
            starter.close()

    def scan_thread():
        global queue
        while True:
            num = queue.get()
            pscan(num)
            queue.task_done()

    def main(target_ip, ports):
        global queue
        for thread in range (N_THREADS):
            thread = Thread(target = scan_thread)
            thread.daemon = True
            thread.start()
        for num in ports:
            queue.put(num)
            queue.join()

#if __name__ == "__main__":
#    parser = argparse.ArgumentParser(description = "Scanner")
#    parser.add_argument("target_ip")
#    parser.add_argument("--ports","-p", dest = "port_range", default = "1-2500")
#    args = parser.parse_args()
#    target_ip, port_range = args.target_ip, args.port_range
##    start_port, end_port = port_range.split("-")
#    start_port, end_port = int(start_port), int(end_port)
#    ports = [p for p in range (start_port, end_port)]
#
#    main(target_ip, ports)
