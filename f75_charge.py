from f75_processes2 import *
from f75_hexagons import *
from f75_5_lemmas import *
from f75_charge2 import *

def set_up_hexagon_charges(configs):
    # set up charges for 6-gons
    print "find hexagons with +ve curvature not in configs A,B,C or D"
    show_hex_fig()
    print "find hexagons with +ve curvature in configs A and B"
    show_hex_figAB()
    print "find hexagons with +ve curvature in configs C and D"
    show_hex_figCD()
    prove5_6(configs)
    prove5_7(configs) 

def charge_logic_script (script,configs,multi_edge_charges):
    #print multi_edge_charges
    diag=False
    vertices=[]
    faces=[]
    print script
    f1=open(script,'r')
    labels=[]
    filterit=False
    cc=0
#    multi_edge_charges=[]
    prev_line=""
    prev_len=0
    err=False
    for linex in f1:
        #while '|*' in linex:
            # expand test to two tests.
            # test for exactly 4 degree followed by test for >= 4 degree with
            # any difference justifying a -6 from charges
        if linex.startswith('quit'):
            break
        lines=linex.split(';')
        if err:
            break
        #print len(lines)
        for line in lines:
            #print line
            line=line.rstrip()
            if line.startswith("deficit"):
                calc_deficit(line,multi_edge_charges)
            if line.startswith("diag"):
                diag=True
            if line.startswith("filter"):
                filterit=True
            if line.startswith("nofilter"):
                filterit=False
            if line.startswith("nodiag"):
                diag=False
            if line.startswith("hexagons"):
                # set up charges for 6-gons
                set_up_hexagon_charges(configs)
            linexx=line
            if len(line)==0:
                continue
            if line[0].isdigit():
                #print 'expanding'
                line1=line
                line2=""
                if  '{' in line:
                    ii=line.index('{')
                    line1=line[:ii]
                    line2=line[ii:]
                deg2=line1.split('|')
                no_4=len(deg2)
                if deg2[-1]=='*':
                    no_4-=1
                no_3=prev_len-no_4
                new_line1='X['+str(no_3)+','+str(no_4)+'('+line1+')]'
                line=new_line1+line2
                #print line
            linexx=line
            if line.startswith('X'):
                line1=prev_line
                line2=line[1:]
                linexx=line1+line2
            #print "????",linexx
            if linexx.startswith('*') or linexx.startswith('+'):
                print linexx
                prev_line=linexx[0]
                prev_len=0
                for let in linexx[1:]:
                    if let=='(' or let=='*':
                        prev_line+=let
                    elif let.isalpha():
                        prev_line+=let
                        prev_len+=1
                    else:
                        break
                lim=9
                if linexx.startswith('+'):
                    lim=100
                qual=""
                if '{' in linexx:
                    s=linexx.index('{')
                    e=linexx.index('}')
                    qual=linexx[s+1:e]
                    linexx=linexx[:s]
     #               print qual,line
                #print "!!!!",linexx    
                if '[' in linexx:
                    err=calc_curvature(linexx[1:],multi_edge_charges,lim,qual)
                    if err:
                        break
                all_alpha=False
                if len(linexx)>2:
                    all_alpha=True
                    for xx in linexx[1:]:
                        if not xx.isalpha():
                            all_alpha=False
                            break
                if all_alpha:
                   filt=[0,0,'?','?']
                   disp_max_charges(linexx[1:],multi_edge_charges,lim,filt)
            elif linexx.startswith('='):
                multi_edge_charges.append(linexx[1:].split(','))
                # mult-line charges
            else:
                #commands to be actioned
               # print line
                if linexx.startswith("#"):
                    print ""
                    print linexx

                comms=linexx.split(',')
                for comm in comms:
                    cc+=1
    #print cc,'commands!'
    #show_labels(labels,diag,filterit)
    f1.close()
def calc_curvature(line,multi_edge_charges,lim,qual):
    pos_charge=False
    forced_charges_m=[]
    add_min_6=False
    quals=qual.split('|')
    for qualx in quals:
        if qualx=='-6':
            add_min_6=True
            continue
        forced_chargesx=get_forced_charges(multi_edge_charges,qualx)
        forced_charges_m.append(forced_chargesx)
 #       if len(forced_charges_m)>1:
 #           print "***",forced_charges_m
    charges=0
    #print line
    s=line.index('[')+1
    e=line.index(']')
    degs_s=line[s:e]
    degs=degs_s.split(',')
    degsx=set_up_degs(degs)
    #print degsx
    i=0
    for deg in degs:
        if "(" in deg:
            ii=deg.index('(')
            degs[i]=deg[:ii]
        i+=1
            
    line=line[:s-1]
#    print line
    lenl=len(line)
#    print degs
    ll=0
    i=0
    let=-1
    if line[-2]=='(':
        # the first character is the middle of a triple
        i=1
        let=0
    elif line[-1]=='(':
        # the first and 2nd character are part of a triple
        i=2
        let=1
    while i < lenl:
        if line[i]=='*':
            lim=9
            i+=1
            continue
        if line[i]=='+':
            lim=100
            i+=1
            continue

        if line[i].isalpha():
            j=(i+1)%lenl
            while not line[j].isalpha():
                j=(j+1) %lenl
            edge=line[i]+line[j]
            let+=1
            degl=len(degsx)
            nlet=(let+1) %degl
            prevlet,nextlet=get_prev_next(line,i,j)
            forced=False
            mx=0
            filt=[degsx[let],degsx[nlet],'?','?']
#            print filt,edge
            for forced_charges in forced_charges_m:
                if len(forced_charges)>0:
                    multis=[prevlet+edge,edge+nextlet]
                    pattern1,dir1=normalize_edges(prevlet+edge)
                    pattern0,dir2=normalize_edges(edge+nextlet)

                    if pattern1==forced_charges[0]:
                        #print edge,"in1",forced_charges
                        mx=int(forced_charges[1][1])
                        if dir1=='-':
                            mx=int(forced_charges[1][0])
                        forced=True
                    if pattern0==forced_charges[0]:
                        #print edge,"in0",forced_charges
                        mx=int(forced_charges[1][0])
                        if dir2=='-':
                            mx=int(forced_charges[1][1])
                        forced=True
            if forced == False:
 #               if filt[0]>0:
 #                   print "***",edge,filt
                m4,m3=disp_max_charges(edge,multi_edge_charges,lim,filt)
                mx=max(m4,m3)
                if len(degs)==1:
                    # all deg 3
                    mx=m3
            pre=""
            post=""
            if filt[0]>0 or filt[1]>0:
                pre= str(filt[0])
                if pre=='44':
                    pre='=4'
                post= str(filt[1])
                if post=='44':
                    post='=4'
 
            print pre+edge+post,
            print mx,
            charges+=mx
            i+=1
            ll+=1
        else:
            # must be '(' - feed in next 2 edges
            j1=(i+1)%lenl
            let+=1
            j2=(j1+1)%lenl
            let+=1
            j3=(j2+1)%lenl
            ll+=2
            if j3 > i:
                i=j3
            else:
                i=lenl
            while not line[j3].isalpha():
                let+=1
                j3=(j3+1) %lenl
            edges=line[j1]+line[j2]+line[j3]
            # filter not used for combined charge
            mx=disp_max_combined_charge(edges)
            print edges,mx,
            
            #print edges,mx,"*****",charges,"***"
            charges+=mx
    print
    denominator=3
    curv=60*(2-ll)
    print "curv=",curv,
    for deg in degs:
        if deg.isdigit():
            #print "denominator=",denominator
            more_curv=int(deg)*2*60/denominator
            curv+=more_curv
            print "+",more_curv,
        denominator+=1

    #print "curvature before charges applied",curv
    print "+",charges*2,
    curv+=(charges*2)
    print "=",curv,
    if add_min_6:
        print "(-6)",
        curv-=6
    print ""
    if curv>0:
        print "FAILURE in curvature calculation!!!!"
        pos_charge=True
    return pos_charge

def get_prev_next(line,i,j):
    
    ll=len(line)
    i=(i-1)%ll
    while not line[i].isalpha():
        i=(i-1)%ll
    prevlet=line[i]
    j=(j+1)%ll
    while not line[j].isalpha():
        j=(j+1)%ll
    nextlet=line[j]
    return prevlet,nextlet

def get_forced_charges(multi_edge_charges,qual):
    forced_charges=[]
    for mm in multi_edge_charges:
        if mm[-2]==qual:
            ll=len(mm[0])
            return [mm[0],mm[1+ll:1+ll+ll - 1]]
    return []
    
def set_up_degs(degs):
    # degrees are 0 (filter specifies everything)
    # unless specific degrees are specified in () notation
    # in which case degrees are at least 3.n practise all 0's
    # or a mixtures of 3's and 4's
    degree=0
    degsx=[]
    total=0
    i=0
    total3=0
    total4=0
    for deg in degs:
        i+=1
        if deg.isdigit():
            total+=int(deg)
            if i==1:
                total3=total
        elif '(' in deg:
            if i==2:
                #setting deg 4 and the rest 3
                #degree=3
                degree=0
            s=deg.index('(')+1
            e=deg.index(')')
            total+=int(deg[:s-1])
            if i==2:
                posns=deg[s:e]
                posnsx=posns.split('|')
                total4=len(posnsx)
                if total4> 1:
                    if posnsx[-1]=='*':
                        total4-=1

    if total3+total4==total:
        degree=3
    for i in range(total):
        degsx.append(degree)  # base line
    degree=3
    factor4=1
    for deg in degs:    # override base line entries
        i+=1
        if '(' in deg:
#            print deg
            s=deg.index('(')+1
            e=deg.index(')')
            posns=deg[s:e]
            posnsx=posns.split('|')
            if posnsx[-1] == '*':
                factor4=11
                #force only deg 4 vertices
                posnsx.pop()
            for pos in posnsx:
                posi=int(pos)-1
                degsx[posi]=degree
                if degree==4:
                    degsx[posi]=degree*factor4
        if degree > 0:
            degree+=1
    return degsx
    
 
