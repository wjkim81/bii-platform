import sys
print(sys.path)
sys.path.insert(0,'/home/vcvr/platform/')
from app import app as application
