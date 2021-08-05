import os
import argparse

def convert_mnist_experiment_result(experiment_result) -> str:
    import json
    print("\n Best trial values : ",experiment_result)
    # new  = json.dumps(experiment_result)
    # print(type(new))
    r = json.loads(experiment_result)
    # print(type(r))
    best_trial = r["currentOptimalTrial"]["bestTrialName"]
    max_metrics_val = r["currentOptimalTrial"]["observation"]["metrics"][0]["max"]
    metrics = r["currentOptimalTrial"]["observation"]["metrics"][0]["name"]
    parameters = r["currentOptimalTrial"]["parameterAssignments"]
    print("\n Best Trial Name : ",best_trial)
    print("\n Metrics : ",metrics)
    print("\n Best value achieved for metrics %s : %s"%(metrics,max_metrics_val))
    print("\n Best Hyperparameters achieved : ")
    args = []
    for hp in parameters:
        print(hp)
        args.append("%s=%s" % (hp["name"], hp["value"]))

    return " ".join(args)

def print_pred(mount_path,output_file):
    out = open(mount_path+output_file,"r")
    
    res = convert_mnist_experiment_result(out.read())
    print("\n Result : \n ",res)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="print out the predictions")
    parser.add_argument(
        "--mount-path",
        type=str,
        help="Path PVC",
    )
    parser.add_argument(
        "--output-file",
        type=str,
        help="output text file where hp result is stored",
    )
args,_ = parser.parse_known_args()
print_pred(args.mount_path,args.output_file)
