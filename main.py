import paramiko
import getpass
import os
import time


# Thank you stack overflow for this one
# https://stackoverflow.com/questions/4409502/directory-transfers-with-paramiko
class MySFTPClient(paramiko.SFTPClient):
    def put_dir(self, source, target):
        ''' Uploads the contents of the source directory to the target path. The
            target directory needs to exists. All subdirectories in source are
            created under target.
        '''
        for item in os.listdir(source):
            if os.path.isfile(os.path.join(source, item)):
                self.put(os.path.join(source, item), '%s/%s' % (target, item))
            else:
                self.mkdir('%s/%s' % (target, item), ignore_existing=True)
                self.put_dir(os.path.join(source, item), '%s/%s' % (target, item))

    def mkdir(self, path, mode=511, ignore_existing=False):
        ''' Augments mkdir by adding an option to not fail if the folder exists  '''
        try:
            super(MySFTPClient, self).mkdir(path, mode)
        except IOError:
            if ignore_existing:
                pass
            else:
                raise


def start():
    mtime = time.ctime(max(os.stat(root).st_mtime for root, _, _ in os.walk(folderpath)))
    while True:
        if mtime != time.ctime(max(os.stat(root).st_mtime for root, _, _ in os.walk(folderpath))):
            mtime = time.ctime(max(os.stat(root).st_mtime for root, _, _ in os.walk(folderpath)))
            print(f'    File updated at: {mtime}...')
            print(f'    Updating directory on server...')
            try:
                transport = paramiko.Transport((hostname, 22))
                transport.connect(username=username, password=password)
                sftp = MySFTPClient.from_transport(transport)
                sftp.mkdir(target_path, ignore_existing=True)
                sftp.put_dir(folderpath, target_path)
                sftp.close()
                print(f'    Successfully updated the contents on the server')
            except:
                print("An error occurred updating the content on the server.")


if __name__ == '__main__':
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    while True:
        folderpath = input("Absolute Folder Path (local):\n")
        if not os.path.isdir(folderpath):
            print("Folder doesn't exist.")
        else:
            target_path = input("Folder Name (server):\n")
            break

    while True:
        hostname = input("Host name:\n")
        username = getpass.getpass("Username:\n")
        password = getpass.getpass("Password:\n")
        try:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("Starting the monitor...")
            start()
        except Exception as e:
            print("An error occurred connecting to SSH. Try again.")
