from configparser import ConfigParser
import os
folder ='C:\\RD'
config = ConfigParser()
numbers=[4,5]
for root,dirs,files in os.walk(folder):
    for file in files:
        if "VisualOCR.txt" in file:
            config.read(os.path.join(root,"VisualOCR.txt"))



#config.read("VisualOCR.txt")
#print(config.has_option('Data', '9'))
