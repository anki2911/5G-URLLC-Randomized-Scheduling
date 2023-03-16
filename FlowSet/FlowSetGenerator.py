import sys
import random
import math

def main():
    #utilization
    Util_min = int(sys.argv[1])
    Util_max = int(sys.argv[2])
    #no of bands
    n_subbands = int(sys.argv[3])
    #alpha: no of slot allocations per frame
    alpha = int(sys.argv[4])
    #SCS
    SCS = int(sys.argv[5])
    #600 Slots for SCS 1 1200 Slots for SCS 2
    
    hyperperiod = 1000
    #Available Slots per frame 
    #allocated_min = (Util_min*1.0/100) * av
    #allocated_max = (Util_max*1.0/100) * av
    
    #Deadline_Options = [20,30,40,50,60,100,120,150,200,300,600]
    Deadline_Options = [20,50,100,200,500,1000]
    num = 0
    while num < 100:
        util = 0.0
        deadline_1 = []
        deadline_2 = []

        #while (allocate < allocated_max): 
        #while util < alpha*0.1*n_subbands:
        while util < (Util_min + Util_max)*0.5*0.01*n_subbands:
            r = random.randint(1,len(Deadline_Options))                
            p = (Deadline_Options[r-1]*0.5)
            if p%2 == 1:
                util = util + 1/(alpha*0.1*(p-5))
                p = p - 5
            else:
                util = util + 1/(alpha*0.1*p)
            if util < Util_max*0.01*n_subbands:
                deadline_1.append(int(p))
                deadline_2.append(int(Deadline_Options[r-1] - p))
            else:
                util = util - 1/(alpha*0.1*p)
                #allocate = allocate - 2 * hyperperiod/Deadline_Options[r-1]
            #print p
            print util
            #print allocate
        #if allocate < allocated_max:   
        if util < n_subbands * Util_max * 0.01:         
            f = open("Allocation_" + str(alpha) + "/Util_" + str(Util_min) + "_" + str(Util_max) + "_" + str(n_subbands) + "/Flow_" + str(num+1) + ".txt","w")
            for i in range(0,len(deadline_1)):
                f.write("F_"+ str(i+1) + "\n")
                f.write(str(deadline_1[i]) + "\n")
                f.write(str(deadline_2[i]) + "\n")
                f.write("%\n")
            f.close()      
            num = num + 1
    
if __name__ == '__main__':
    main()
