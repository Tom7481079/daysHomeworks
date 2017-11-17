import sys, os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(ROOT_DIR)
from day09.FtpClient.modules.FtpClient import FtpClient

if __name__ == '__main__':
    myclient = FtpClient()
    myclient.start()