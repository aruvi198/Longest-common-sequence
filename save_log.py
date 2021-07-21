import logging
print("*****************************************************************************************")
file = open('log.txt','r')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('/var/log/katib/metrics.log')
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
for i in file.readlines():
    if 'loss =' in i:
        out = i.split(',')[-2]
        print(out)
        logger.info(out)
        
        
        
