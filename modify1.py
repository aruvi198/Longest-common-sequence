import argparse,os,json
parser = argparse.ArgumentParser('Modify')
# parser.add_argument('--num-epochs',default=None,type=int)
# parser.add_argument('--batch-size-per-gpu',default=None,type=int)
# parser.add_argument('--regularizer',default=None,type=str)
parser.add_argument('--spec-path',default=None,type=str)
parser.add_argument('--new-spec-path',default=None,type=str)
args = parser.parse_args()
flag = 0
# def modify(num_epochs=args.num_epochs,batch_size_per_gpu=args.batch_size_per_gpu,regularizer=args.regularizer,spec_path=args.spec_path,new_spec_path=args.new_spec_path):
def modify(spec_path=args.spec_path,new_spec_path=args.new_spec_path):
    home_path,filename = os.path.split(spec_path)
    path = "/workspace/tlt-experiments/output_tlt.txt"
    output_file = open(path,"r")
    hp = json.load(output_file)
    parameters = hp['currentOptimalTrial']['parameterAssignments']
    num_epochs_val,batch_size_per_gpu_val,regularizer = None, None, None
    for i in range(len(parameters)):
        name = parameters[i]['name']
        val = parameters[i]['value']
        if name == "num_epochs":
            num_epochs_val = val
        elif name == "batch_size_per_gpu":
            batch_size_per_gpu_val = val
        elif name == "regularizer":
            regularizer_val = val
    print(num_epochs_val,batch_size_per_gpu_val,regularizer)
    f = open(spec_path,'r')
    global flag
#     new_path = home_path+"/new_spec.txt"
    new_path = new_spec_path
    print("***************************new path : ",new_path,spec_path)
    f2 = open(new_path,'w')
    for i in f.readlines():
        if 'training_config' in i:flag = 1
        if flag == "regularizer_set":
            i = ' '*i.index('t') + 'type: ' + str(regularizer) + '\n'
            flag = 0
        if flag == 1:
            if 'num_epochs' in i and num_epochs != None:
                    i = ' '*i.index('n') + 'num_epochs: ' + str(num_epochs) + '\n'
            elif 'batch_size_per_gpu' in i and batch_size_per_gpu != None:
                    i = ' '*i.index('b') + 'batch_size_per_gpu: ' + str(batch_size_per_gpu) + '\n'
            elif 'regularizer' in i and regularizer != None:
                    flag = "regularizer_set"
        f2.write(i)
    f.close()
    f2.close()
# modify(num_epochs=args.num_epochs,batch_size_per_gpu=args.batch_size_per_gpu,regularizer=args.regularizer,spec_path=args.spec_path,new_spec_path=args.new_spec_path)
modify(spec_path=args.spec_path,new_spec_path=args.new_spec_path)
