import time
import sys
import os
import subprocess
import shutil
from os import path
space="' '"
pushpath = "/home/pi/audioProject/Livetext/"
while True:
    pushdirs = os.listdir( pushpath )
    for file in pushdirs:
        text=os.path.splitext(file)[0]
        ext=os.path.splitext(file)[1]
        with open(pushpath+text+ext,'r') as file:
            # reading each line     
            for line in file:
                for word in line.split():
                    os.system('sudo python send_string.py '+word)
                    os.system('sudo python send_string.py '+space)
        
        file.close()
        os.remove('/home/pi/audioProject/Livetext/'+text+ext)
        
    
            




