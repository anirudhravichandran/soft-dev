#!/usr/bin/python
from PIL import Image
import urllib
from bs4 import BeautifulSoup
import re
import getpass
import MySQLdb

#global vars
testVar = []

#Function to convert small case roll number to capital case
def convert(roll):
 for a in roll:
  a = a.upper()
  testVar.append(a)
 roll = "".join(testVar)
 return roll

# Open database connection
db = MySQLdb.connect("localhost","root","sincostan","rollnum" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

rollnum = raw_input("Enter Roll Number of student: ")
rollnum = convert(rollnum)
path = "/home/" + getpass.getuser() + "/Pictures/" + rollnum
checkroll = "select * from studentdata where RollNo=('%s')" %(rollnum)

try:
 # Execute the SQL command
 print "here"
 cursor.execute(checkroll)
 db.commit()
 results = cursor.fetchall()
 if results==():
  #extracting data
  dataURL = "https://ccw.iitm.ac.in/IITMHostels/sinfo/" + rollnum
  photoURL = "https://photos.iitm.ac.in/byroll.php?roll=" + rollnum
  datasrc = urllib.urlopen(dataURL).read()
  soup = BeautifulSoup(datasrc,"lxml")
  
  td = soup.findAll("td")
  name = re.search("<strong><h2>(.*)</h2></strong>",str(td[0])).groups()[0]
  gender = re.search("<td>(.*)</td>",str(td[3])).groups()[0]
  prog = re.search("<td>(.*)</td>",str(td[5])).groups()[0]
  department = re.search("<td>(.*)</td>",str(td[11])).groups()[0]
  DOJ = re.search("<td>(.*)</td>",str(td[9])).groups()[0]
  currentsem = re.search("<td>(.*)</td>",str(td[15])).groups()[0]
  facad = re.search("<td>(.*)</td>",str(td[17])).groups()[0]
  urllib.urlretrieve("https://photos.iitm.ac.in/byroll.php?roll="+rollnum,path)
   #print type(currentsem)
  print "Name : %s\nRoll Number : %s\nGender : %s\nProgram : %s\nDepartment : %s\nDate of Joining : %s\nCurrent Semester : %s\nFaculty Advisor : %s\n" %(name,rollnum,gender,prog,department,DOJ,currentsem,facad)
  print "Picture can be found at /home/" + getpass.getuser() + "/Pictures/"  

  option = raw_input("Do you want to save this data?(Y/N) ")
  if option=="Y" or option=="y" or option=="Yes" or option=="yes":
   sql = "INSERT INTO studentdata(RollNo,Name,Department,Course,DOJ,FacultyAdvisor,currentsem,Gender) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')" %(rollnum,name,department,prog,DOJ,facad,currentsem,gender)
   cursor.execute(sql)
   db.commit()
 else:
  print "Name : %s\nRoll Number : %s\nGender : %s\nProgram : %s\nDepartment : %s\nDate of Joining : %s\nCurrent Semester : %s\nFaculty Advisor : %s\n" %(str(results[0][1]),rollnum,str(results[0][7]),str(results[0][3]),str(results[0][2]),str(results[0][4]),str(results[0][6]),str(results[0][5]))
  img = Image.open(path)
  img.show()
 
 
except:
 db.rollback()
   # Rollback in case there is any error




 



   


# disconnect from server
db.close()


