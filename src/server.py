import socket
import sys
import threading
import asyncio
import logging


host_address="0.0.0.0"
port=9999
server=None




def handle_client(client_socket, client_address):
    pass


async def main():
    global server
    try:
        server= socket.socket( socket.AF_INET, socket.SOCK_STREAM)
        server.bind( (host_address,port) )
        server.listen()

        while True:
            client, address = server.accept()
            print(f'received connection from {str(address[0])}:{str(address[1])}')

            client.send(' whoami  '.encode('utf-8'))

            client_handler = threading.Thread( target=handle_client, args=(client,address))
            client_handler.start()

    except Exception as error:
        print( f"ERROR: {str(error)}" )
        server.close()
    finally:
        server.close()
    


if __name__=="__main__":
    asyncio.run(main() )