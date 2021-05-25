import pathlib
import datetime
from paramiko import SSHClient
from scp import SCPClient


def start():
    mtime = datetime.datetime.fromtimestamp(fname.stat().st_mtime)
    while True:
        if mtime != datetime.datetime.fromtimestamp(fname.stat().st_mtime):
            mtime = datetime.datetime.fromtimestamp(fname.stat().st_mtime)
            print(f'    File updated at: {mtime}...')

            with SCPClient(ssh.get_transport()) as scp:
                scp.put(filepath, filepath)
                print(f'    File successfully transferred to SSH.')


if __name__ == '__main__':
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    while True:
        filepath = input("File path:\n")
        if pathlib.Path(filepath).exists():
            fname = pathlib.Path(filepath)
            break
        else:
            print("File doesn't exist.")

    while True:
        hostname = input("Host name:\n")
        username = input("Username:\n")
        password = input("Password:\n")
        try:
            print("Attempting to connect to SSH client...")
            ssh = SSHClient()
            ssh.load_system_host_keys()
            ssh.connect(
                hostname=hostname,
                username=str(username),
                password=str(password)
            )
            break
        except Exception as e:
            print(e)
            print("An error occurred connecting to SSH. Try again.")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Starting the monitor...")
    start()
