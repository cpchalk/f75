from f75_processes import *

def normalize_edges(edges):
    dir='+'
    ll=len(edges)
    n_edges=edges
    n_edgesx=""
    if edges[0].upper()>edges[-1].upper():
        dir='-'
        n_edges=""
        i=ll
        while i>0:
            i-=1
            n_edges+=edges[i]
    swap_case=False
    n_edge0=n_edges[0]
    if n_edge0.isupper():
        swap_case=True
        n_edgesx+=n_edge0.lower()
    elif n_edge0=='m':
        swap_case=True
        n_edgesx+='l'
    if swap_case:
        i=1
        while i<ll:
            n_edgei=n_edges[i]
            if n_edgei.isupper():
                n_edgesx+=n_edgei.lower()
            elif n_edgei=='l':
                n_edgesx+='m'
            elif n_edgei=='m':
                n_edgesx+='l'
            else:
                n_edgesx+=n_edgei.upper()
            i+=1
    else:
        n_edgesx=n_edges
    return n_edgesx,dir

def get_max_charges (resx,lim):
    max4=0
    max3=0
    for item in resx:
        if item[2]>lim:
            continue
        if item[0]==3 and item[1]==3:
            if item[2]>max3:
                max3=item[2]
        else:
            if item[2]>max4:
                max4=item[2]
    if max4<max3:
        max4=max3
    return max4,max3

def disp_max_charges(label,multi_edge_charges,lim,filt):
    ll=len(label)
    i=0
    while i < ll:
        previ=(i-1) % ll
        edge1=label[i]
        j=(i+1)%ll
        edge2=label[j]
        s_edge=edge1+edge2
        nextj=(j+1) % ll
        
        edge,dir=normalize_edges(s_edge)
        filtx=[filt[0],filt[1],'?','?',edge]
        if dir=='-':
            filtx=[filt[1],filt[0],'?','?',edge]
        #print edge
        # single charges
        resx=print_charge_hash(filtx,False)
        max4,max3=get_max_charges(resx,lim)
        #check multi edges
        if len(multi_edge_charges) > 0 and ll>2:
            multi1=s_edge+label[nextj]
            multi2=label[previ] + s_edge
            multis=[multi1,multi2]
           # print "checking",multis
            max4,max3=check_multi_edge_charges(multis,multi_edge_charges,max4,max3)
            #print "**",multi_edge_charges[0][0]
        if ll > 2:
            print edge1+edge2,str(max4)+"("+str(max3)+")"
        else:
            return max4,max3
        i+=1

def check_multi_edge_charges(multis,multi_edge_charges,max4,max3):
    #estabkish max charge total of two consecutive edges
    for j in range(len(multis)):
        start_i=j
        label=multis[j]
        ll=len(label)
        #check_lab=multis[j][j:j+2]
        lab_n,dir=normalize_edges(multis[j])
        if dir=='-':
           #normalization has reversed the label
            start_i=ll-1 - ((start_i + 1))  #!!!!
        
        for mm in multi_edge_charges:
            if not mm[0] == lab_n:
                continue
            # not relevant if mm[-2] is a qual
            if not mm[-2].isdigit(): 
                    continue
            degs=mm[1+start_i:3+start_i]
            charge=int(mm[1+ll+start_i])
            charged_edge=lab_n[start_i:start_i+2]
            if degs==['3','3']:
                if charge>max3:
                    max3=charge
            else:
                if charge>max4:
                    max4=charge
    return max4,max3

def disp_max_combined_charge(pqr):
    # find the max combined charges of pq and qr
    edge1=pqr[0:2]
    # read 2nd edge the opposite way so that filters affect the
    # vertex that joins the two edges
    edge2=pqr[2]+pqr[1]
    # last_vertex of edge1 = first vertex of edge2
    # keep track of this when normalizing
    filt3_1,filt4_1,filt5_1=get_filters(edge1)
    filt3_2,filt4_2,filt5_2=get_filters(edge2)
    #print filt3_1,filt3_2
    max3_1=get_max_charge(filt3_1)
    max3_2=get_max_charge(filt3_2)
    max3=max3_1+max3_2
    #print max3
    #print filt4_1,filt4_2
    max4_1=get_max_charge(filt4_1)
    max4_2=get_max_charge(filt4_2)
    max4=max4_1+max4_2
    #print "??",max4
    max5_1=get_max_charge(filt5_1)
    max5_2=get_max_charge(filt5_2)
    max5=max5_1+max5_2
    #print max5
    return max(max3,max4,max5)

def get_max_charge(filt):
    mx=0
    resx=print_charge_hash(filt,False)
    for item in resx:
        if item[2] > 10:
            continue
        if item[2]>mx:
                mx=item[2]
    return mx

def get_filters (edge):
    edge_n,dir=normalize_edges(edge)
    filt3=[0,3,'?','?',edge_n]
    filt4=[0,44,'?','?',edge_n]
    filt5=[0,55,'?','?',edge_n]

    if dir=='-':
        filt3=[3,0,'?','?',edge_n]
        filt4=[44,0,'?','?',edge_n]
        filt5=[55,0,'?','?',edge_n]

    return filt3,filt4,filt5
