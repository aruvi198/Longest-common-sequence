import logging
print("*****************************************************************************************")
file = open('log.txt','r')
print("file : ",file)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('/var/log/katib/metrics.log')
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
for i in file.readlines():
    print("checking logs .................................................................")
    print(i)
    if 'loss =' in i:
        print("loss ------------------------------------------------------- ",i)
        out = i.split(',')[-2]
        print(out)
        logger.info(out)
    else:
        print("not found ------------------------------------------------------------------")
        
        
        
