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
# logger = logging.getLogger()
# logger.setLevel(logging.INFO)
# file_handler = logging.FileHandler('/var/log/katib/metrics.log')
# file_handler.setLevel(logging.DEBUG)
# logger.addHandler(file_handler)
print("checking logs .................................................................")
for i in file.readlines():
    if 'loss' in i:
        out = i.split(',')[0]
        name = "loss="
        val = str(out.split(":")[-1].strip())
        logging.info('loss={}'.format(val))
#         final = name+val
# metricName: ([\\w|-]+), metricValue: ((-?\\d+)(\\.\\d+)?)
        final = "metricName: {}, metricValue: {}".format("loss",val)
        logging.info(final)
        print(final)
        #logger.info(final)
    else:
#         print("not found ------------------------------------------------------------------")
        pass
        
        
        
