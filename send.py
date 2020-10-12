import cv2
from PIL import Image
import numpy
import time
from ftplib import FTP
import os
import fileinput
from datetime import datetime
from pymongo import MongoClient
import yaml
import sys

vidcap = cv2.VideoCapture(0)
success,image = vidcap.read()
count = 0
success = True
numA = 0

while success:
  
  ret, frame = vidcap.read()
  success,image = vidcap.read()
  cv2.imwrite("frame%d.png" % count, image)
  print("capture picture %d" %count)
  if count >= 1:
      count1 = count-1
      count2 = count
      im1 = Image.open('frame%d.png' % count1)
      im2 = Image.open('frame%d.png' % count2)
      pixels1 = list(im1.getdata())
      pixels2 = list(im2.getdata())
      array1 = numpy.array(pixels1)
      array2 = numpy.array(pixels2)
      x = array1 - array2
      y = x.tolist()
      z = len(y)
      check = 0
      
      error = z/ 20
      print(z)
      print(error)
      while(check < z):
          if [-20,-20,-20]<= y[check] <=[20,20,20]:
              check += 1
          else:
              numA += 1
              check += 1
            
      print(numA)
      if numA >= error:
          print("new picture")
          
          ftp = FTP()
          ftp.set_debuglevel(2)
          ftp.connect('192.168.43.155', 21)
          ftp.login('davis','davis')

          datetime = datetime.now()
          datetime_ = datetime.strftime("%d.%m.%Y %H:%M:%S")
          namedir = datetime.strftime("Y%YM%m")
          namepic = datetime.strftime("%Y-%m-%d-T%H.%M.%S-" + "U01" + "-" + "P01")
          print(datetime_)
          print(namepic)

          path = "/home/vsa01/FTP/" + namedir
          path2 = "/home/vsa01/FTP/" + namedir + "/" + "P01"


          isdir = os.path.isdir(path)
          print(isdir)

          isdir2 = os.path.isdir(path2)
          print(isdir2)

          try:
            conn = MongoClient("192.168.43.155", 27017)
            print("Connected successfully!!!")
          except:
            print("Could not connect to MongoDB")

          db = conn.Project
          collection = db.Project


          ftp.cwd(path2)

          fp = open('frame%d.png' % count, 'rb')
          ftp.storbinary('STOR %s' % os.path.basename(str(namepic) +".png"), fp, 1024)
          fp.close()
          ftp.sendcmd("SITE CHMOD 777 " + path2 + "/" + str(namepic) + ".png") #permission
          print(ftp.dir())
          ftp.quit()

          project = {
                      "Image_Path": str(namepic) + ".png"
          }

          collection.insert_one(project)

          print("Data inserted successfully")
          count += 1
      else:
          print("same picture")

  else:
      print(' first picture')
      ftp = FTP()
      ftp.set_debuglevel(2)
      ftp.connect('192.168.43.155', 21)
      ftp.login('davis','davis')

      datetime = datetime.now()
      datetime_ = datetime.strftime("%d.%m.%Y %H:%M:%S")
      namedir = datetime.strftime("Y%YM%m")
      namepic = datetime.strftime("%Y-%m-%d-T%H.%M.%S-" + "U01" + "-" + "P01")
      print(datetime_)
      print(namepic)

      path = "/home/vsa01/FTP/" + namedir
      path2 = "/home/vsa01/FTP/" + namedir + "/" + "P01"


      isdir = os.path.isdir(path)
      print(isdir)

      isdir2 = os.path.isdir(path2)
      print(isdir2)

      try:
        conn = MongoClient("192.168.43.155", 27017)
        print("Connected successfully!!!")
      except:
        print("Could not connect to MongoDB")

      db = conn.Project
      collection = db.Project


      ftp.cwd(path2)

      fp = open('frame%d.png' % count, 'rb')
      ftp.storbinary('STOR %s' % os.path.basename(str(namepic) +".png"), fp, 1024)
      fp.close()
      ftp.sendcmd("SITE CHMOD 777 " + path2 + "/" + str(namepic) + ".png") #permission
      print(ftp.dir())
      ftp.quit()

      project = {
                  "Image_Path": str(namepic) + ".png"
      }

      collection.insert_one(project)

      print("Data inserted successfully")
      count += 1
  time.sleep(5)
  if cv2.waitKey(1) & 0xFF == ord('q'):
      print("End program")
      break
  

cv2.destroyAllWindows()
