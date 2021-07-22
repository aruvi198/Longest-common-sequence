# Have to add logic to read Validation loss and mAP

import logging
import tensorflow as tf

logger = tf.get_logger()
logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%SZ",
    level=logging.INFO)

print("*****************************************************************************************")
file = open('/workspace/tlt-experiments/experiment_dir_unpruned/status.json','r')
print("file : ",file)
print("checking logs .................................................................")

for i in file.readlines():
    if 'loss' in i:
        out = i.split(',')[0]
        name = "loss="
        val = str(out.split(":")[-1].strip())
        log = name+val
        logging.info(log)
        print(log)
        
        log2 = "metricName: {}, metricValue: {}".format("loss",val)
        logging.info(log2)
        print(log2)
    else:
        pass
        
        
        
