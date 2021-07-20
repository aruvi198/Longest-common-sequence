file = open('log.txt','r')
for i in file.readlines():
    if 'loss =' in i:
        print(i.split(',')[-2])
        
        
