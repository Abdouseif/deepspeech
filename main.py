import RPi.GPIO as GPIO
import time
import sys
import os
import subprocess
import shutil
import moviepy.editor as mp
from os import path
from pydub import AudioSegment
from datetime import date, datetime
ctr0=0
ctr1=0
ctr2=0
off=4
batch=17
live=27
GPIO.setmode(GPIO.BCM)
GPIO.setup(off, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(batch, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(live, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

# Checking for new model
file = open("/home/pi/audioProject/Models/modelname.txt","r")
model = file.read().splitlines()
modeltflite= model[0]
modelscorrer=model[1]
file.close()
modelpath = "/home/pi/audioProject/Models"
modeldirs = os.listdir( modelpath )
counter=0
print(modeltflite)
print(modelscorrer)
# This would print all the files and directories
for file in modeldirs:
    if file==modeltflite:
        print("Model Tflite found")
    elif file==modelscorrer:
        print("Model Scorrer found")
    else:
        counter=counter+1
if counter==3:
    #new model added
    print("new model found testing it...")
    try:
        backuppath = "/home/pi/audioProject/modelbackup"
        backupdirs = os.listdir( backuppath )
        for file in backupdirs:
            os.remove("/home/pi/audioProject/modelbackup/"+file)
            
        shutil.move('/home/pi/audioProject/Models/'+modeltflite, "/home/pi/audioProject/modelbackup/"+modeltflite)
        shutil.move('/home/pi/audioProject/Models/'+modelscorrer, "/home/pi/audioProject/modelbackup/"+modelscorrer)
        modelpath = "/home/pi/audioProject/Models"
        modeldirs = os.listdir( modelpath )
        for file in modeldirs:
            text=os.path.splitext(file)[0]
            ext=os.path.splitext(file)[1]
            if ext==".tflite":
                newmodel_tflite=file
            elif ext==".scorer":
                newmodel_scorer=file
        os.system('deepspeech --model Models/'+newmodel_tflite+ ' --scorer Models/'+newmodel_scorer+' --audio 2830-3980-0043.wav>> 2830-3980-0043_text.txt')
        
    except:
        for file in dirs:
            text=os.path.splitext(file)[0]
            ext=os.path.splitext(file)[1]
            if ext!=".txt":
                os.remove("/home/pi/audioProject/Models/"+file)
        shutil.move("/home/pi/audioProject/modelbackup/"+modeltflite,'/home/pi/audioProject/Models/'+modeltflite)
        shutil.move('/home/pi/audioProject/modelbackup/'+modelscorrer,'/home/pi/audioProject/Models/'+modelscorrer)
            
    else:
        file = open("/home/pi/audioProject/Models/modelname.txt","w")
        file.write(newmodel_tflite+"\n")
        file.write(newmodel_scorer+"\n")
        file.close()
        modeltflite=newmodel_tflite
        modelscorrer=newmodel_scorer
        
        
else:
    print("No New Model")

while True:
    if GPIO.input(off) == True:
        if ctr0==0:
            file = open("/home/pi/audioProject/apimode.txt","w")
            file.write("OFF Mode"+"\n")
            file.close()
            ctr0=1
        pass
        
    elif GPIO.input(batch) == True:
        if ctr1==0:
            file = open("/home/pi/audioProject/apimode.txt","w")
            file.write("Batch Mode"+"\n")
            file.close()
            ctr1=1
        today = date.today()
        now = datetime.now()
        # Open a file
        path = "/home/pi/audioProject/Work"
        dirs = os.listdir( path )
        # This would print all the files and directories
        for file in dirs:
            text=os.path.splitext(file)[0]
            ext=os.path.splitext(file)[1]
            print(ext)
            if ext==".mp4":
                clip = mp.VideoFileClip('/home/pi/audioProject/Work/'+file)
                clip.audio.write_audiofile('/home/pi/audioProject/Work/'+text+'.mp3')
                sound = AudioSegment.from_mp3('/home/pi/audioProject/Work/'+text+'.mp3')
                sound.export('/home/pi/audioProject/Work/'+text+'.wav', format="wav",parameters=["-ar", "16000"])
                shutil.move('/home/pi/audioProject/Work/'+file, "/home/pi/audioProject/Processed/"+file)
                shutil.move('/home/pi/audioProject/Work/'+text+'.mp3', "/home/pi/audioProject/Processed/"+text+'.mp3')
                file=text+'.wav'
            
            os.system('deepspeech --model Models/'+modeltflite+' --scorer Models/'+modelscorrer+' --audio Work/'+file+ '>> Transcripts/'+text+'_text.txt')
            shutil.move('/home/pi/audioProject/Work/'+file, "/home/pi/audioProject/Processed/"+file)
            file = open("/home/pi/audioProject/api.txt","w")
            today = date.today()
            now1 = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            current_time1 = now1.strftime("%H:%M:%S")
            file.write(str(today)+" " + str(current_time)+"\n")
            file.write(text+ext+"\n")
            file.write(str(today)+" " + str(current_time1)+"\n")
            file.write(modeltflite+"\n")
            file.close()
    elif GPIO.input(live) == False:
        if ctr2==0:
            file = open("/home/pi/audioProject/apimode.txt","w")
            file.write("Live Mode"+"\n")
            file.close()
            ctr2=1
        from_file = open("/home/pi/audioProject/api.txt") 
        line = from_file.readline()
        today = date.today()
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        line=str(today) +" " + str(current_time)+"\n"
        to_file = open("/home/pi/audioProject/api.txt",mode="w")
        to_file.write(line)
        shutil.copyfileobj(from_file, to_file)
        path = "/home/pi/audioProject/Live"
       
        os.system('./boot.sh')
        os.system('./bash1.sh')
        os.system('./bash2.sh')
        while True:
            dirs = os.listdir( path )
            for file in dirs:
                text=os.path.splitext(file)[0]
                ext=os.path.splitext(file)[1]
                sound = AudioSegment.from_mp3(path+'/'+text+'.wav')
                sound.export(path+'/'+text+'.wav', format="wav",parameters=["-ar", "16000"])
                file=text+'.wav'
                os.system('deepspeech --model Models/'+modeltflite+' --scorer Models/'+modelscorrer+' --audio Live/'+file+ '>> Livetext/'+text+'.txt')
                os.remove('/home/pi/audioProject/Live/'+file)
                #shutil.move('/home/pi/audioProject/Live/'+file, "/home/pi/audioProject/Processed/"+file)
                if GPIO.input(live) == True:
                    break
    else:        
        pass
    