import sys
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
    
    hyperperiod = 1000
    n_exp = 100
    n_alloc = 10
    n_flowsets = 100
    
    #hyperperiod = 120
    #n_exp = 100
    #n_alloc = 1
    #n_flowsets = 1
    
    div = open("Divergence_ER_" + str(Util_min) + "_" + str(Util_max) + "_" + str(n_subbands) + "_" + str(alpha) + "_" + str(SCS) + ".txt","w")
    
    for i in range(0,n_alloc):
        Prob = []
        sum_2 = 0
        
        for j in range(0,n_flowsets):
            Prob.append([])
            
        for j in range(0,n_flowsets):
            for k in range(0,hyperperiod/10):
                Prob[j].append([])
                #Br_Pr[j].append([])
                
        for j in range(0,n_flowsets):
            for k in range(0,hyperperiod/10):
                for l in range(0,n_subbands):
                    Prob[j][k].append([])
                    #Br_Pr[j][k].append([])    
        
        for j in range(0,n_flowsets):
            for k in range(0,hyperperiod/10):
                for l in range(0,n_subbands):
                    for m in range(0,10*SCS):
                        Prob[j][k][l].append([])
                        #Br_Pr[j][k][l].append([])  
            
        
            Brut = []
            b = open("../SCS_" + str(SCS) + "/Allocation_" + str(alpha) + "/Brute_Prob_" + str(Util_min) + "_" + str(Util_max) + "_" + str(n_subbands) + "/Brute_Prob_" + str(j+1) + ".txt","r")
            #b = open("Brute_1.txt","r")
            for lines in b:
                lines = lines.strip()
                lines = lines.split("\t")
                for words in lines:
                    Brut.append(float(words))
                    #print words
            #print Brut
            num_of_flows = len(lines)
            #print "Len " + str(num_of_flows)
            sum_2 = 0.0
            for k in range(0,len(Brut)):
                sum_2 += Brut[k]
            #print sum_2
            
            c = open("../SCS_" + str(SCS) + "/Allocation_" + str(alpha) + "/Random_ER_" + str(Util_min) + "_" + str(Util_max) + "_" + str(n_subbands) + "/Prob_" + str(i+1) + "_" + str(j+1) + ".txt","r")
            #c = open("Rough_EDF/Prob_ER_New_1_1.txt","r")
            
            frame_no = 0
            subband_no = 0
            mini_slot = 0
            sum_1 = 0.0
            for lines in c:
                lines = lines.strip()
                for words in lines:
                    words = lines.split("\t")
                if words[0] == '%%':
                    frame_no += 1
                    subband_no = 0
                    mini_slot = 0
                elif words[0] == '%':
                    subband_no += 1
                    mini_slot = 0
                else:
                    for v in range(0,len(words)):
                        #print words[v]
                        #Prob[j][frame_no][subband_no][mini_slot].append(float(words[v])/(alpha*1.0/(10*SCS) * hyperperiod))
                        Prob[j][frame_no][subband_no][mini_slot].append(float(words[v]))
                        if v < num_of_flows-1:
                            sum_1 = sum_1 + float(words[v]) 
                        else:
                            sum_1 = sum_1 + float(words[v])
                    mini_slot += 1
            c.close()
            
            #print Prob[j]
            
            #print sum_1
            sum_br = 0
            sum_dive = 0
            Div = 0.0
            for frames in range(0,hyperperiod/10):
                for n_bands in range(0,n_subbands):
                    for minislots in range(0,10*SCS):
                        for flows in range(0,num_of_flows):
                            if Prob[j][frames][n_bands][minislots][flows] > 0.0:
                                a = float(Brut[flows]*1.0)/float(alpha*0.1*SCS*hyperperiod*n_subbands)
                                sum_br += a
                                #a = float((Brut[flows]*1.0)/(alpha*0.1*hyperperiod*n_subbands))*1.0
                                #d = float(Prob[j][frames][n_bands][minislots][flows]*1.0)/float(n_exp*alpha*0.1*SCS*hyperperiod*n_subbands)
                                d = float(Prob[j][frames][n_bands][minislots][flows]*1.0)/(sum_1)
                                sum_dive += d 
                                #b = float((Prob[j][frames][n_bands][minislots][flows]*1.0)/(alpha*0.1*hyperperiod*n_subbands))*1.0
                                #print a
                                #print b
                                Div = Div + d*math.log(d/a,10)
            print Div
            #print sum_br
            #print sum_dive
            div.write(str(Div))
            div.write("\n")
            del Brut
        del Prob    
    div.close()
               



if __name__ == '__main__':
    main()
