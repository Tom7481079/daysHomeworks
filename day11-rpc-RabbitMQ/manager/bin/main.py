import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(ROOT)
from day11.manager.module.manager import Manager

if __name__ == '__main__':
    manager = Manager("RPC", ["fromNodes", ])
    manager.run()