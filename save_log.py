import logging
print("*****************************************************************************************")
file = open('/workspace/tlt-experiments/experiment_dir_unpruned/status.json','r')
print("file : ",file)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('/var/log/katib/metrics.log')
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
for i in file.readlines():
    print("checking logs .................................................................")
    print(i)
    if 'loss' in i:
        print("loss ------------------------------------------------------- ",i)
        out = i.split(',')[0]
        name = "loss="
        val = str(out[9:])
        final = name+val
        print(final)
        logger.info(final)
    else:
        print("not found ------------------------------------------------------------------")
        
        
        
