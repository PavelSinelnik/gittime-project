import sqlite3

import os
import json
folder = 'D:\\folder\\main1'
con = sqlite3.connect('15.db')
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
for root,dirs,files in os.walk(folder):
    
    for fil in files:
        if "RFID.txt" in fil:
            
            if CountryName != root.split("\\")[3]:
                cur.execute("SELECT CAST(CASE WHEN EXISTS ( SELECT CountryName FROM countries  WHERE countries.CountryName  ='{}') THEN 1 ELSE 0 END AS BIT) AS Result".format(root.split("\\")[3]))
                data = cur.fetchone()
                if data[0] == 1:
                    cur.execute("SELECT id FROM countries WHERE countries.CountryName='{}'".format(root.split("\\")[3]))
                    CountryInfo = cur.fetchone()
                    Country_id =CountryInfo[0]
                
                
                else :
                    cur.execute('INSERT INTO countries(id,CountryName)  VALUES(?,?)',(None,root.split("\\")[3]))
                    cur.execute("SELECT id,CountryName FROM countries WHERE countries.CountryName='{}'".format(root.split("\\")[3]))
                    CountryInfo = cur.fetchall()
                    
                    Country_id =CountryInfo[0][0]
                    CountryName = CountryInfo[0][1]
                    
            if DocumentName != root.split("\\")[4]:
                cur.execute("SELECT CAST(CASE WHEN EXISTS ( SELECT DocumentName FROM TypeOfDocs  WHERE TypeOfDocs.DocumentName  ='{}' AND Country_Ind = '{}') THEN 1 ELSE 0 END AS BIT) AS Result".format(root.split("\\")[4],Country_id))
                data = cur.fetchone()
                if data[0] == 1:
                    cur.execute("SELECT id FROM TypeOfDocs WHERE TypeOfDocs.DocumentName='{}' AND Country_Ind = '{}'".format(root.split("\\")[4],Country_id))
                    DocumentInfo = cur.fetchone()
                    Document_id =DocumentInfo[0]
                    
                else:
                    cur.execute('INSERT INTO TypeOfDocs(Country_Ind,id,DocumentName)  VALUES(?,?,?)',(Country_id,None,root.split("\\")[4]))
                    cur.execute("SELECT id,DocumentName FROM TypeOfDocs WHERE TypeOfDocs.DocumentName='{}' AND Country_Ind = '{}'".format(root.split("\\")[4],Country_id))
                    DocumentInfo = cur.fetchall()
                    Document_id =DocumentInfo[0][0]
                    DocumentName=DocumentInfo[0][1]
                    
            if SampleName != os.path.basename(root):
                cur.execute("SELECT CAST(CASE WHEN EXISTS ( SELECT SampleName FROM samples  WHERE samples.SampleName  ='{}' AND samples.Document_Ind = '{}') THEN 1 ELSE 0 END AS BIT) AS Result".format(os.path.basename(root),Document_id))                          
                data=cur.fetchone()
                if data[0] == 1:
                    cur.execute("SELECT id FROM samples WHERE samples.SampleName='{}' AND Document_Ind = '{}'".format(os.path.basename(root),Document_id))
                    SampleInfo = cur.fetchone()
                    Sample_id=SampleInfo[0]
                else:
                    cur.execute('INSERT INTO samples(id,Document_Ind,SampleName)  VALUES(?,?,?)',(None,Document_id,os.path.basename(root)))
                    cur.execute("SELECT id,SampleName FROM samples WHERE samples.SampleName ='{}' AND Document_Ind = '{}'".format(os.path.basename(root),Document_id))
                    SampleInfo = cur.fetchall()
                    Sample_id =SampleInfo[0][0]
                    SampleName=SampleInfo[0][1]
                                

                        

cur.close()
con.commit()
