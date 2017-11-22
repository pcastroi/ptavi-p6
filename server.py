#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import os
import socketserver
import sys


class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        while 1:
            line = self.rfile.read()
            dcline = line.decode('utf-8')
            try:
                if dcline.split()[0] == 'INVITE':
                    self.wfile.write(bytes("SIP/2.0 100 Trying\r\n\r\n", 'utf-8') +
                                     bytes("SIP/2.0 180 Ringing\r\n\r\n", 'utf-8') +
                                     bytes("SIP/2.0 200 OK\r\n\r\n", 'utf-8'))
                    
                elif dcline.split()[0] == 'ACK':
                    os.system('./mp32rtp -i 127.0.0.1 -p 23032 < ' + sys.argv[3])
                        
                elif dcline.split()[0] == 'BYE':
                    self.wfile.write(b"SIP/2.0 200 OK\r\n")
                        
                else:
                    self.wfile.write(b"SIP/2.0 405 Method Not Allowed\r\n")
                
                print("El cliente nos manda " + dcline)
            except IndexError:
            # Para las líneas que sean tan solo \r\n
                pass
            
            
            
            
            
            
            

            

            if not line:
                break

if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit("Usage: Usage: python3 server.py IP port audio_file")
    # Creamos servidor de eco y escuchamos
    serv = socketserver.UDPServer(('', int(sys.argv[2])), EchoHandler)
    print("Listening...")
    serv.serve_forever()
