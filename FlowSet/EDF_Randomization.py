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
    
    
    hyperperiod = 1000
    n_exp = 100
    n_alloc = 10
    n_flowsets = 100
    
    #hyperperiod = 120
    #n_exp = 100
    #n_alloc = 1
    #n_flowsets = 1
    
    
    #Load Slot Allocation
    for i in range(0,n_alloc):        
        f = open("../SCS_" + str(SCS) + "/Allocation_" + str(alpha) + "/Band_" + str(n_subbands) + "/Allocation_" + str(alpha) + "_" + str(i+1) + ".txt","r")
        #print "Hello World"
        #f = open("Allocation_3_1.txt","r")
        #Stores allocation of slots
        Available = [] 
        for num in range(0,hyperperiod/10):
            Available.append([])
            for j in range(0,n_subbands):
                Available[num].append([])
        count = 0
        t = 0       
        for lines in f:
            lines = lines.strip()
            #lines = lines.split("\t")
            for words in lines:
                words = lines.split("\t")
            if words[0] == '%':
                t = 0
                count = count + 1
            else:
                for v in range(0,len(words)):
                    Available[count][t].append(int(words[v]))
                t = t + 1
        
        #Load Flow Sets
        for num in range(0,n_flowsets):
            g = open("../SCS_" + str(SCS) + "/Allocation_" + str(alpha) + "/Util_" + str(Util_min) + "_" + str(Util_max) + "_" + str(n_subbands) + "/Flow_" + str(num+1) + ".txt","r")
            #g = open("Flow_1.txt","r")
            num_of_flows = 0
            Real_deadline = []
            deadline_1 = []
            deadline_2 = []
            for lines in g:
                lines = lines.strip("\n")
                words = lines.split()
                if words[0][0] == "F":
                    count = 0
                elif count == 0:
                    deadline_1.append(int(words[0]))
                    d1 = int(words[0])
                    count = count + 1
                elif count == 1:
                    deadline_2.append(int(words[0]))
                    d2 = int(words[0])
                    Real_deadline.append(d1+d2)
                    count = count + 1
                    num_of_flows = num_of_flows + 1
                    
            #PreProcessing Steps        
            Real_deadline.sort()
            deadline_1.sort()
            deadline_2.sort()
            
            #Create Schedules and Flows List
            HP_Sched = []
            EDF_Sched = []
            Slot_av = []
            EDF_slots = []
            Prob = []
            for num_of_exp in range(0,n_exp):
                Slot_av.append([])
                HP_Sched.append([])
                EDF_Sched.append([])
                EDF_slots.append([])
                for frame in range(0,hyperperiod/10):
                    Slot_av[num_of_exp].append([]) 
                    HP_Sched[num_of_exp].append([])  
                    EDF_Sched[num_of_exp].append([])  
                    EDF_slots[num_of_exp].append([])         
                    for n_bands in range(0,n_subbands):
                        Slot_av[num_of_exp][frame].append([])
                        HP_Sched[num_of_exp][frame].append([])
                        EDF_Sched[num_of_exp][frame].append([])
                        EDF_slots[num_of_exp][frame].append([])
            
            #print Slot_av          
            for num_of_exp in range(0,n_exp):
                for frame in range(0,hyperperiod/10):
                    for n_bands in range(0,n_subbands):
                        for s in range(0,10*SCS):
                            if Available[frame][n_bands][s] == 1:
                                Slot_av[num_of_exp][frame][n_bands].append(frame*10*SCS + s + 1)
                                HP_Sched[num_of_exp][frame][n_bands].append(0)
                                EDF_Sched[num_of_exp][frame][n_bands].append(0)
                                EDF_slots[num_of_exp][frame][n_bands].append(frame*10*SCS + s + 1)
                            else:
                                HP_Sched[num_of_exp][frame][n_bands].append(-1) 
                                EDF_Sched[num_of_exp][frame][n_bands].append(-1)

            
            for num_of_exp in range(0,n_exp):
                Release_time = []
                Pseudo_deadline = []
                #Early_Release = []
                #Create Release Time List
                for flow in range(0,num_of_flows):
                    Release_time.append([])
                    Pseudo_deadline.append([])
                    #Early_Release.append([])
                
            
                #Update Pseudo Deadline and Release Time    
                for time in range(1,hyperperiod+1):
                    for flow in range(0,num_of_flows):
                        if time%Real_deadline[flow] == 0:
                            #Release_time of first instance
                            Release_time[flow].append((time-Real_deadline[flow])+1) 
                            p = Real_deadline[flow]/2
                         
                            if p%2 == 0:
                                #Release time of second instance
                                Release_time[flow].append((time-p)+1) 
                                #Pseudo deadline of first instance
                                Pseudo_deadline[flow].append(time-p) 
                            else:
                                #Release time of second instance
                                Release_time[flow].append((time-p-5)+1) 
                                #Pseudo deadline of first instance 
                                Pseudo_deadline[flow].append(time-p-5)
                            #Pseudo deadline of second instance
                            Pseudo_deadline[flow].append(time)
                        
            #print Release_time
            #print Pseudo_deadline
            #Generate EDF Schedule
            for num_of_exp in range(0,n_exp):
                for time in range(1,SCS*hyperperiod+1):
                    for flow in range(0,num_of_flows):
                        if time in Pseudo_deadline[flow]:
                            index = Pseudo_deadline[flow].index(time)
                            lb = Release_time[flow][index]
                            ub = Pseudo_deadline[flow][index]
                            #print cur_flow
                            #print str(lb) + " " + str(ub)
                            eligible = []
                            flag = 0
                            for slots in range(lb,ub+1):
                                for freq in range(0,n_subbands):
                                    if slots in EDF_slots[num_of_exp][(slots-1)/(10*SCS)][freq]:
                                        if flag == 0:
                                            EDF_slots[num_of_exp][(slots-1)/(10*SCS)][freq].remove(slots)
                                            EDF_Sched[num_of_exp][(slots-1)/(10*SCS)][freq][(slots-1)%(10*SCS)] = flow + 1
                                            flag = 1
            
                    
            #print EDF_Sched
            #print EDF_slots
            

            #Generate Randomized Schedule
            for num_of_exp in range(0,n_exp):
                for frame in range(0,hyperperiod/10):
                    for n_bands in range(0,n_subbands):
                        for s in range(0,10*SCS):
                            HP_Sched[num_of_exp][frame][n_bands][s] = EDF_Sched[num_of_exp][frame][n_bands][s]
                
                for time_1 in range(1,SCS*hyperperiod+1):
                    g_flag = 0
                    for flow_1 in range(0,num_of_flows):
                        if ((time_1 in Release_time[flow_1]) and (g_flag == 0)):
                            #print Release_time[flow_1]
                            g_flag = 1
                            index_1 = Release_time[flow_1].index(time_1)
                            lb = Release_time[flow_1][index_1]
                            #print "LB " + str(lb)
                            #ub = Pseudo_deadline[flow][index]
                            flag = 0
                            
                            for t in range(time_1+1,SCS*hyperperiod+1):
                                #print t
                                #while ((flag == 0) and (t > time_1) and (t <= SCS*hyperperiod+1)):
                                for flow_2 in range(0,num_of_flows):
                                    if t in Pseudo_deadline[flow_2]:
                                        if flag == 0:
                                            flag = 1
                                            index_2 = Pseudo_deadline[flow_2].index(t)  
                                            ub = Pseudo_deadline[flow_2][index_2]
                                            #print "LB " + str(lb) + " UB " + str(ub)  
                                            Av = []
                                            L_flows = []                            
                                            for slots in range(lb,ub+1):
                                                for freq in range(0,n_subbands):
                                                    if slots in Slot_av[num_of_exp][(slots-1)/(10*SCS)][freq]:
                                                        Av.append(str(slots) + "_" + str(freq))
                                                    #if (EDF_Sched[num_of_exp][(slots-1)/(10*SCS)][freq][(slots-1)%(10*SCS)] > 0):
                                                        L_flows.append(EDF_Sched[num_of_exp][(slots-1)/(10*SCS)][freq][(slots-1)%(10*SCS)])
                                            for f_no in range(0,len(L_flows)):
                                            #print L_flows
                                            #l = 0
                                            #f_no = 0
                                            #while f_no < len(L_flows):                                            
                                                r = random.randint(0,len(Av)-1)
                                                sl_fr = Av[r]
                                                length = len(sl_fr)
                                                freq_band = int(sl_fr[length-1]) 
                                                slot_no = int(sl_fr[0:length-2])
                                                HP_Sched[num_of_exp][(slot_no-1)/(10*SCS)][freq_band][(slot_no-1)%(10*SCS)] = L_flows[f_no]               
                                                Av.remove(sl_fr)
                                                
                                            del Av
                                            del L_flows                                  
                                        
                                       


            #print HP_Sched
            for frames in range(0,hyperperiod/10):
                Prob.append([])
                
            for frames in range(0,hyperperiod/10):
                for q in range(0,n_subbands):
                    Prob[frames].append([])
            
            for frames in range(0,hyperperiod/10):
                for q in range(0,n_subbands):
                    for minislots in range(0,10*SCS):
                        Prob[frames][q].append([]) 
            
            for frames in range(0,hyperperiod/10):
                for subbands in range(0,n_subbands):
                    for minislots in range(0,10*SCS):
                        for flows in range(0,num_of_flows+1):
                            Prob[frames][subbands][minislots].append(0)    
            
            for index in range(0,n_exp):
                c = 0
                for frames in range(0,hyperperiod/10):
                    for s_bands in range(0,n_subbands):
                        for minislot in range(0,10*SCS):
                            if HP_Sched[index][frames][s_bands][minislot] == 0:
                                Prob[frames][s_bands][minislot][num_of_flows] += 1 
                                c = c + 1
                            elif HP_Sched[index][frames][s_bands][minislot] > 0:
                                Prob[frames][s_bands][minislot][(HP_Sched[index][frames][s_bands][minislot])-1] += 1 
                                c = c + 1
            
            sum_1 = 0.0 
                                  
            f = open("../SCS_" + str(SCS) + "/Allocation_" + str(alpha) + "/EDF_" + str(Util_min) + "_" + str(Util_max) + "_" + str(n_subbands) + "/Prob_" + str(i+1) + "_" + str(num+1) + ".txt", "w")
            #f = open("Rough_EDF/Prob_" + str(i+1) + "_" + str(num+1) + ".txt", "w")
            for index in range(0,hyperperiod/10):
                for bands in range(0,n_subbands):
                    for minislots in range(0,10*SCS):
                        for flows in range(0,num_of_flows+1):
                            sum_1 = sum_1 + (Prob[index][bands][minislots][flows]*1.0)/(alpha * 0.1 * SCS * n_exp * n_subbands * hyperperiod)
                            #f.write(str((Prob[index][bands][minislots][flows]*1.0)/(alpha * 0.1 * SCS * n_exp * n_subbands * hyperperiod)))
                            f.write(str(Prob[index][bands][minislots][flows]))
                            #print Prob[index][bands][minislots][flows]
                            f.write("\t")
                        f.write("\n")
                    f.write("%\n")
                f.write("%%\n")
            f.close()
            #print sum_1
            print str(i+1) + "_" + str(num+1)
            
            del Slot_av
            del Prob                                            
            #print HP_Sched                    
            del HP_Sched
            del EDF_Sched
            del EDF_slots                    
                #print HP_Sched[num_of_exp]

if __name__ == '__main__':
    main()
