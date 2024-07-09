import ftplib
import os

def list_files_ftp(ftp):
    """
    List files in the current directory on the FTP server.
    """
    file_list = []
    dir_list = []

    ftp.retrlines('LIST', lambda x: file_list.append(x) if x.startswith('-') else dir_list.append(x.split()[-1] + '/'))

    return [file.split()[-1] for file in file_list], [dir.split()[-1] for dir in dir_list]

def download_files_ftp(ftp, file_list, local_dir):
    """
    Download files from the FTP server to the local directory.
    """
    for filename in file_list:
        local_filename = os.path.join(local_dir, filename)
        with open(local_filename, 'wb') as local_file:
            ftp.retrbinary('RETR ' + filename, local_file.write)

def connect_ftp(ip):
    """
    Connect to the FTP server using anonymous login and return the FTP connection object.
    """
    ftp = ftplib.FTP(ip)
    ftp.login()  # anonymous login
    return ftp

def traverse_and_download(ftp, local_dir):
    """
    Recursively traverse directories on the FTP server and download files.
    """
    original_dir = ftp.pwd()
    
    files, dirs = list_files_ftp(ftp)
    download_files_ftp(ftp, files, local_dir)
    
    for dir in dirs:
        ftp.cwd(dir)
        new_local_dir = os.path.join(local_dir, dir.strip('/'))
        if not os.path.exists(new_local_dir):
            os.makedirs(new_local_dir)
        traverse_and_download(ftp, new_local_dir)
        ftp.cwd('..')

    ftp.cwd(original_dir)

def main():
    ip = os.getenv('ip')
    if not ip:
        raise ValueError("Environment variable 'ip' not set.")
    
    local_dir = os.getcwd()
    ftp = connect_ftp(ip)
    traverse_and_download(ftp, local_dir)
    ftp.quit()

if __name__ == "__main__":
    main()
