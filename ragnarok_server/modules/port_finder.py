from threading import Thread, Lock
import socket
from queue import Queue

class PortFinder:
    global queue
    queue = Queue()
    global output
    output = []
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
                output.append('Port: %s => %s' %(port, socket.getservbyport(port, protocol)))

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
        return output
