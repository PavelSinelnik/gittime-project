import sqlite3
from time import time
import os
import json
start = time()
folder = 'D:\\folder\\main1'
con = sqlite3.connect('C:\\Users\\Pavel\\Desktop\\git-project\\db\\15.db')
cur=con.cursor()

cur.execute(
        'CREATE TABLE  IF NOT EXISTS countries(id INTEGER PRIMARY KEY AUTOINCREMENT,' 
        'CountryName TEXT)')

cur.execute(
        'CREATE TABLE  IF NOT EXISTS TypeOfDocs(Country_Ind INTEGER,'
        'id INTEGER PRIMARY KEY AUTOINCREMENT,' 
        'DocumentName TEXT,'
        'FOREIGN KEY (Country_Ind) REFERENCES countries(id) ON UPDATE CASCADE,'
        'FOREIGN KEY (Country_Ind) REFERENCES countries(id) ON DELETE CASCADE)')


cur.execute(
        'CREATE TABLE  IF NOT EXISTS samples(id INTEGER PRIMARY KEY AUTOINCREMENT ,'
        'Document_Ind INTEGER,'
        'SampleName TEXT,'
        'FOREIGN KEY (Document_Ind) REFERENCES TypeOfDocs(id) ON UPDATE CASCADE,'
        'FOREIGN KEY (Document_Ind) REFERENCES TypeOfDocs(id) ON DELETE CASCADE)')
CountryName=''
DocumentName=''
SampleName=''
Country_id=0
Document_id=0
Sample_id=0
for root,dirs,files in os.walk(folder):
    
    for fil in files:
        if "RFID.txt" in fil:
            
            if CountryName != root.split("\\")[3]:     
                cur.execute("SELECT id FROM countries  WHERE countries.CountryName  ='{}'".format(root.split("\\")[3]))
                data = cur.fetchone()
                if data != None:
                    #cur.execute("SELECT id FROM countries WHERE countries.CountryName='{}'".format(root.split("\\")[3]))
                    Country_id =data[0]
                
                
                else :
                    cur.execute('INSERT INTO countries(id,CountryName)  VALUES(?,?)',(None,root.split("\\")[3]))
                    #cur.execute("SELECT id,CountryName FROM countries WHERE countries.CountryName='{}'".format(root.split("\\")[3]))
                    #CountryInfo = cur.fetchall()
                    Country_id +=1
                    CountryName = root.split("\\")[3]
                    
            if DocumentName != root.split("\\")[4]:
                cur.execute("SELECT id FROM TypeOfDocs  WHERE TypeOfDocs.DocumentName  ='{}' AND Country_Ind = '{}'".format(root.split("\\")[4],Country_id))
                data = cur.fetchone()
                if data != None:
                    #cur.execute("SELECT id FROM TypeOfDocs WHERE TypeOfDocs.DocumentName='{}' AND Country_Ind = '{}'".format(root.split("\\")[4],Country_id))
                    #DocumentInfo = cur.fetchone()
                    Document_id =data[0]
                    
                else:
                    cur.execute('INSERT INTO TypeOfDocs(Country_Ind,id,DocumentName)  VALUES(?,?,?)',(Country_id,None,root.split("\\")[4]))
                    #cur.execute("SELECT id,DocumentName FROM TypeOfDocs WHERE TypeOfDocs.DocumentName='{}' AND Country_Ind = '{}'".format(root.split("\\")[4],Country_id))
                    #DocumentInfo = cur.fetchall()
                    Document_id +=1
                    DocumentName=root.split("\\")[4]
                    
            if SampleName != os.path.basename(root):
                cur.execute("SELECT id FROM samples  WHERE samples.SampleName  ='{}' AND samples.Document_Ind = '{}'".format(os.path.basename(root),Document_id))                          
                data=cur.fetchone()
                if data != None:
                    #cur.execute("SELECT id FROM samples WHERE samples.SampleName='{}' AND samples.Document_Ind = '{}'".format(os.path.basename(root),Document_id))
                    #SampleInfo = cur.fetchone()
                    Sample_id=data[0]
                else:
                    cur.execute('INSERT INTO samples(id,Document_Ind,SampleName)  VALUES(?,?,?)',(None,Document_id,os.path.basename(root)))
                    #cur.execute("SELECT id,SampleName FROM samples WHERE samples.SampleName ='{}' AND Document_Ind = '{}'".format(os.path.basename(root),Document_id))
                    #SampleInfo = cur.fetchall()
                    Sample_id +=1
                    SampleName=os.path.basename(root)
                                

                        

cur.close()
con.commit()
finish = time()
print(finish-start)