import sys


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
    
    
    hyperperiod = 1000
    n_exp = 100
    n_flowset = 100
    
    Allocations = []
    Prob = []
    
    for i in range(1,n_flowset+1):
        g = open("../SCS_" + str(SCS) + "/Allocation_" + str(alpha) + "/Util_" + str(Util_min) + "_" + str(Util_max) + "_" + str(n_subbands) + "/Flow_" + str(i) + ".txt","r")
        count = 0
        deadline_1 = []
        deadline_2 = []
        exec_time = []
        j = 0
        for lines in g:
            lines = lines.strip("\n")
            lines = lines.split("\t")
            #print lines[0]
            if lines[0][0] == "F":
                j = 1
            elif j == 1:
                deadline_1.append(int(lines[0]))
                j = 2
            elif j == 2:
                deadline_2.append(int(lines[0]))
                j = 0
            elif lines[0] == "%":
                count = count + 1                
        g.close()
        num_of_flows = count
        #print count
        sum_1 = 0.0
        Pr = []
        f = open("../SCS_" + str(SCS) + "/Allocation_" + str(alpha) + "/Brute_Prob_" + str(Util_min) + "_" + str(Util_max) + "_" + str(n_subbands) + "/Brute_Prob_" + str(i) + ".txt","w")
        #f = open("Brute_1.txt","w")
        #print num_of_flows
        total_exec = 0
        for j in range(0,num_of_flows):
            deadline = deadline_1[j] + deadline_2[j]
            #Per slot Probability
            n_inst = hyperperiod/deadline
            hops = 2
            Prob = (n_inst * hops)/(alpha*0.1*SCS*hyperperiod*n_subbands)
            #Prob = (2.0 * hyperperiod)/(alpha * 0.1 * SCS * deadline * deadline * n_subbands)
            Pr.append(Prob)
            sum_1 = sum_1 + Prob   
            f.write(str(Prob))
            f.write("\t")
            total_exec = total_exec + (2*hyperperiod*1.0)/deadline
            #print total_exec
            #print alpha * 0.1  * SCS * hyperperiod * n_subbands
            #Prob = ((alpha*0.1*SCS * hyperperiod * n_subbands) - total_exec)/(alpha*0.1*SCS * hyperperiod * n_subbands)
            #Prob = ((alpha * 0.1  * SCS * hyperperiod * n_subbands) - total_exec)/(alpha * 0.1 * SCS * hyperperiod * n_subbands)
        Prob = ((alpha * 0.1  * SCS * hyperperiod * n_subbands) - total_exec)/(alpha * 0.1 * SCS * hyperperiod * n_subbands)
        #print Prob
        sum_1 = sum_1 + Prob 
        Pr.append(Prob)
        f.write(str(Prob))
        f.write("\n")
        f.close()
        print Pr   
        print sum_1
        del Pr
        
        
        
        
                    
    

    


if __name__ == '__main__':
    main()
