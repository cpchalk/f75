from copy import deepcopy
from operator import itemgetter, attrgetter, methodcaller

ngon_hash={}    # stores valid divisions for various n-gons
def manage_drawing_sets(keyx):
    # add reflections - normalise - remove duplicates
    drawing_sets=ngon_hash[keyx]
    new_drawing_sets=[]
    vertices=drawing_sets[0]
    new_drawing_sets.append(vertices)
    for d in drawing_sets[1:]:
        dr=reflect(d,vertices)
        pair=(normalise(d,vertices),normalise(dr,vertices))
        for p in pair:
            if not p in new_drawing_sets:
                new_drawing_sets.append(p)
    ngon_hash[keyx]=new_drawing_sets

def normalise(d,vertices):
    #rotate and choose the smallest value
    nn=len(vertices)
    lowest=['zz']
    for i in range(nn):
        rotated=[]
        for line in d:
            i1=vertices.index(line[0])
            i2=vertices.index(line[1])
            i1=(i1+i)%nn
            i2=(i2+i)%nn
            a=vertices[i1]
            b=vertices[i2]
            if a>b:
                (a,b)=(b,a)
            rotated.append(a+b)
        rotated.sort()
        if rotated<lowest:
            lowest=rotated
    return lowest       

def reflect(d,vertices):
    # reflect about 1->n/2 line
    nn=len(vertices)
    rd=[]
    for line in d:
        i=vertices.index(line[0])
        j=vertices.index(line[1])
        ri=(nn-i)%nn
        rj=(nn-j)%nn
        rd.append(vertices[ri]+vertices[rj])
    #print d,"***",rd    
    return rd

def show_ngon (keyx):
    #print "hash!!=",ngon_hash
    if ngon_hash.has_key(keyx):
        return ngon_hash[keyx]
    return ""

def update_ngon (keyx,valuex):
    if keyx=="":
        return
    if ngon_hash.has_key(keyx):
        old_values=ngon_hash[keyx]
    else:
        old_values=[]
    if len(old_values)==0 or not (valuex in old_values):
        old_values.append(valuex)
        ngon_hash[keyx]=deepcopy(old_values)

def create_ngon(keyx):
    ngon_hash[keyx]=[]
def check_single_xy_seq(label):
    # return true if no of letters not in single xy sequence >=9/10
    drawing=label[1]
    label=label[0]
    ll=len(label)
    in_seq=False
    xy=['x','y','X','Y']
    xy_count=0
    curr3=0
    max3=0
    exceptions_1=['abY','ABX']
    exceptions_2=['YZA','Xma']
    exceptions_1r=['yBA','xba']
    exceptions_2r=['azy','Alx']
    exception1=False
    max_exception1=False
    exception2=False
    max_exception2=False
    exception1r=False
    max_exception1r=False
    exception2r=False
    max_exception2r=False

    # look for longest xy sequence
    for j in range(ll):
        h=(j-2) % ll
        i=(j-1)% ll
        k=(j+1)  % ll
        l=(j+2) % ll
        xy_ind=[1,3]
 
        curr_is_max=False
        hx=label[h]
        ix=label[i]
        jx=label[j]
        kx=label[k]
        lx=label[l]
        hijx=hx+ix+jx
        jklx=jx+kx+lx
        if  hijx in exceptions_1:
     #       print hijx
            exception1=True
        if  hijx in exceptions_1r:
      #      print hijx
            exception1r=True
        if  jklx in exceptions_2:
       #     print jklx
            exception2=True
        if  jklx in exceptions_2r:
        #    print jklx
            exception2r=True

        if jx in xy:
            if (ix not in xy) and (kx not in xy):
                curr3=0
                curr_is_max=False
            else:
                curr3+=1
                if max3<curr3:
                    curr_is_max=True
                    max_exception1=exception1
                    max_exception2=exception2
                    max_exception1r=exception1r
                    max_exception2r=exception2r
                    max3=curr3
        else:
            curr_is_max=False
            curr3=0
            exception1=False
            exception2=False
            exception1r=False
            exception2r=False

    n2=ll-max3+1
    if n2>9:
        #print "n2=",n2,"not an exception"
        return True # not an exception 
    if n2==9:
        #print "n2=9",max_exception1,max_exception2,max_exception1r,max_exception2r
        if (max_exception1,max_exception2)==(True,True):
            return False
        if (max_exception1r,max_exception2r)==(True,True):
            return False
        #print "1)n2=",n2,"not an exception"
        return True # unless prefix and suffix = am etc
    #print "2)n2=",n2,"not an exception"
    return True
    
            
    return ll-max3>=n2 #not_this criterion

def get_counts(ll,drawing):
    #print "get counts"
    counts=[0]*ll
    max3=0
    curr3=0
    for line in drawing:
        l0s=line[0]
        l1s=line[1]
        l0=convert(l0s)
        l1=convert(l1s)
        if (l0 >= ll) or (l1 > ll):
            return counts
        counts[l0]+=1
        counts[l1]+=1
    # filter disconnect double xy sequences
    seqs,xy_count=count_seqs(counts)
    if seqs==2:
        # decide if 2 disconnected xy sequences exist
        counts1=[]
        counts2=[]
        prev1=-1
        prev2=-1
        indx=1
        xy_ind=[1,3]
        xy_seq1=[]
        xy_seq2=[]
        ll=len(counts)
        s=0
        for i in range(ll):
            if counts[i] not in xy_ind:
                s=i
                break
        
        for i in range(ll):
            j=(i+s)%ll
            countsj=counts[j]
            counts1.append(countsj)
            counts2.append(countsj)
            if i==0:
                continue
            if indx==1:
                jmin1=(j-1)%ll
                jmin2=(j-2)%ll
                if countsj in xy_ind:
                    if counts[jmin1] in xy_ind:
                        xy_seq1.append(jmin1)
                elif counts[jmin1] in xy_ind and counts[jmin2] in xy_ind:
                    xy_seq1.append(jmin1)
                    indx+=1

        for line in drawing:
            l0s=line[0]
            l1s=line[1]
            l0=convert(l0s)
            l1=convert(l1s)
            if (counts[l0] in xy_ind) and (counts[l1] in xy_ind):
                if 10 in xy_seq1:
                    counts1[l0]=0
                    counts2[l1]=0
                else:
                    counts1[l1]=0
                    counts2[l0]=0
        #check if there are still 2 seqs
        seqs1,xy_count1=count_seqs(counts1)
        seqs2,xy_count2=count_seqs(counts2)
        xy_count=-99
        if seqs1==2 and seqs2==2:
            xy_count=max(xy_count1,xy_count2)
            #print "&*()_",xy_count
        elif seqs1==2:
            xy_count=xy_count1
        elif seqs2==2:
            xy_count=xy_count2
        if xy_count>0:
            if ll-xy_count < 9:
                return xy_count * -1
    #all other cases look for longest xy sequence
    for j in range(ll):
        i=(j-1)% ll
        k=(j+1) % ll
        xy_ind=[1,3]
        if counts[j] in xy_ind:
            if (counts[i] not in xy_ind) and (counts[k] not in xy_ind):
                curr3=0
            else:
                curr3+=1
                if max3<curr3:
                    max3=curr3
        else:
            curr3=0
    return max3 - 1  # return number of xy edges

def count_seqs(counts):
    xy_ind=[1,3]
    in_seq=False
    seqs=0
    ll=len(counts)
    xy_count=0
    for i in range(ll):
        let1=counts[i]
        j=(i+1)%ll
        let2=counts[j]
        if let1 in xy_ind:
            if let2 in xy_ind:
                if in_seq==False:
                    in_seq=True
                    seqs+=1
                xy_count+=1
            else:
                in_seq=False
    return seqs,xy_count

def convert(s):
    lets=['A','B','C','D','E','F','G','H','I']
    si=0
    if s in lets:
        si=9+lets.index(s)
    else:
        si=int(s)-1
    return si
        
def generate_draw_commands(akey,avertices,vertices,minskip):
    #print akey,
    #print show_ngon(akey)
    #print "applied to",avertices
    #print "extending",vertices[1:]
    must_hit=[]
    lines=show_ngon(akey)
   # print "avertices=",avertices
    shape=vertices[0]
    #print "shape=",shape
    lshape=len(shape)
    averticesx=avertices.split(',')

    include=True
    if lshape>8:
        # looking to extend an xy sequence
        # drawing lines must include a hit on the 3rd or last of avertices
        ix=1
        while averticesx[ix]=='Q':
            ix+=1
        ix+=1
        must_hit.append(averticesx[ix])
        must_hit.append(averticesx[-1])
        #print 'must hit',must_hit
    #print lines
    # generate all possible moves
    ll=len(averticesx)
    ngon_vertices=vertices[0][:ll]
    poss=[]
    drawing_sets=[]
    printit=False
    
    for line_set in lines[1:]:
 
        for i in range(ll):
            drawing_set=[]
            if len(must_hit) > 0:
                include=False
            skip_drawing_set=False
            for line in line_set:
                    
                line0=line[0]
                line1=line[1]
                i1=ngon_vertices.index(line0)
                i2=ngon_vertices.index(line1)
 
                i1=(i1+i) % ll
                i2=(i2+i) % ll
                a1=averticesx[i1]
                a2=averticesx[i2]
                if a1=='Q' or a2=='Q':
                    # dont draw edges to 'internal' vertices
                    drawing_set=[]
                    skip_drawing_set=True
                    break
                if a2<a1:
                    (a1,a2)=(a2,a1)
                if (a1+a2 in vertices[1:]) or (a2+a1 in vertices[1:]):
                    # dont draw duplicate edges
                    skip_drawing_set=True
                    break
                j1=shape.index(a1)
                j2=shape.index(a2)
                skip = abs(j2-j1)
                if skip > lshape/2:
                    skip=lshape-skip
                if skip < (minskip+1):
                    skip_drawing_set=True
                    break
                if include==False:
                    if (a1 in must_hit) or (a2 in must_hit):
                        include=True
                drawing_set.append(a1+a2)
            #print "include=",include
            if skip_drawing_set or not include:
                #if not include:
                #   print "NOT",drawing_set
                continue
            if len(drawing_set) != len(line_set):
                print "wrong!!!"
                continue
            drawing_set.sort()
            
            if not drawing_set in drawing_sets:
                drawing_sets.append(drawing_set)
    
    return drawing_sets
