def validate(edges,faces,vertices):
    #print edges
    orig_face=vertices[0]
    for face in faces:
        count_i=0
        count_o=0
        lf=len(face)
        for i in range(lf):
            next_i=(i+1)%lf
            v1=face[i]
            v2=face[next_i]
            end=locate_end(v1,v2,orig_face,edges)
            if len(end) != 2:
                #print "no directed end for",v1,v2,"in",face
                return False
            if end[1]=='i':
                count_i+=1
            else:
                count_o+=1
        if not 1 in [count_i,count_o]:
            #print face,"has i/o",count_i,count_o
            return False
    return True
        
def deduce (start_point,edges,faces,vertices,diag):
    if diag:
        print "deduce",start_point
    border_edge=False
    #print 'edge=',start_point
    orig_face=vertices[0]
    lof=len(orig_face)
    #print orig_face
    shadow_edges=vertices[1:]
    sv=start_point[0]
    ev=start_point[1]
    dir=start_point[2]
    if not ((sv+ev in shadow_edges) or (ev+sv in shadow_edges)):
        border_edge=True

    si=orig_face.index(sv)
    if not ev in edges[si]:
        return 0
    ei=edges[si].index(ev)
    orig_edge=edges[si][ei]
    if orig_edge == ev + dir:
        return 0
    if len(orig_edge)==2:
        print 'contradiction'
        return -99 # contradiction
    edges[si][ei]=ev+dir
    if border_edge:
        #print "**",sv+edges[si][ei]
        if len(edges[si]) == 3:
            # the previous edge must have the same direction
            # as this edge
         #   print "deg 3 deduce!!"
            prev_si=(si-1) % lof
            prev_ei=si
            prev_sv=orig_face[prev_si]
            prev_ev=orig_face[prev_ei]
            end=locate_end(prev_sv,prev_ev,orig_face,edges)
            if len(end)==1:
                res=deduce(prev_sv+prev_ev+dir,edges,faces,vertices,diag)
                if res==-99:
                    return res
        ei_o=orig_face.index(ev)
        if len(edges[ei_o]) == 3:
            # the next edge must have the same direction
            # as this edge
         #   print "deg 3 deduce!!"
            next_ei=(ei_o+1) % lof
            next_si=ei_o
            next_sv=orig_face[next_si]
            next_ev=orig_face[next_ei]
            end=locate_end(next_sv,next_ev,orig_face,edges)
            if len(end)==1:
                res=deduce(next_sv+next_ev+dir,edges,faces,vertices,diag)
                if res==-99:
                    return res


    # inverse edge is ..
    rdir='o'
    if dir=='o':
        rdir='i'

 #   print ev    
    rsi=orig_face.index(ev)
    rei=edges[rsi].index(sv)
    edges[rsi][rei]=sv+rdir
    #print edges
    if border_edge:
        return 0
    #print faces
    #print orig_face
    # update edge in edges,
    # return any shadow edge in the same face
    # give such an edge the same direction
    target=sv+ev
    rev_target=ev+sv
    res=0
    for face in faces:
        lf=len(face)
        s_dir=""
        for i in range(lf):
            next_i=(i+1)%lf
            v1=face[i]
            v2=face[next_i]
            if (v1+v2 in shadow_edges) or (v2+v1 in shadow_edges):
                # is it directed?
                end=locate_end(v1,v2,orig_face,edges)
                if len(end)==2:
                    s_dir=end[1]
                    break
            if s_dir != "":
                break
        if s_dir != "":
            #give any non directed shadow edges direction s_dir
            for i in range(lf):
                next_i=(i+1)%lf
                v1 =face[i]
                v2=face[next_i]
                if (v1+v2 in shadow_edges) or (v2+v1 in shadow_edges):
                    end=locate_end(v1,v2,orig_face,edges)
                    if len(end)==1:
                        res=deduce (v1+v2+s_dir,edges,faces,vertices,diag)
    return 0
    # have the same orientation etc

def locate_end(v1,v2,orig_face,edges):
    v1i=orig_face.index(v1)
    ends=edges[v1i]
    for end in ends:
        if end[0]==v2:
            return end
    return []

def deduce2 (edges,faces,vertices,diag): 
    # check for border edges which must be 'special'
    orig_face=vertices[0]
    lof=len(orig_face)
    shadow_edges=vertices[1:]
    #print "deduce2",edges
    res=0
    for face in faces:
        # count unknown border edges
        f_pairs=[]  #oriented pairs
        x_pairs=[] #non-shadow pairs
        lf=len(face)
        dirx=""
        sdirx=""
        for i in range(len(face)):
            next_i=(i+1)%lf
            v1=face[i]
            v2=face[next_i]
            v1i=0
            f_pairs.append(v1+v2)
            end=locate_end(v1,v2,orig_face,edges)
            if (v1+v2 in shadow_edges) or (v2+v1 in shadow_edges):
                #get direction of shadow_edge
#               print "face",face,"shad dir=",end[1]
                sdirx=end[1]
            else:
                if len(end)==2:
                    if end[1] != sdirx:
                        dirx=end[1]
                else:
                    x_pairs.append(v1+v2)
        if len(x_pairs)==1:
            if dirx=="":
                dirx=sdirx
            dir='i'
            if dirx == 'i':
                dir='o'
#           print "special2",x_pairs
            res=deduce (x_pairs[0]+dir,edges,faces,vertices,diag)
            if res==-99:
                return -99
    return 0
    # have the same orientation etc

def deduce3(edges,faces,vertices,diag):
    orig_face=vertices[0]
    shadow_edges=vertices[1:]
    res=0
    for face in faces:
        special_found=False
        lf=len(face)
        special_edge=""
        prev_dir=""
        prev_v1=""
        prev_v2=""
        # look for 2 consecutive edges of a face with opposite directions
        # one of them must be a boundary edge - this is the special edge
        #start from a shadow edge
        disp=0
        # go round the edges starting with a shadow edge
        #check if there are any unoriented edges
        unoriented=False
        for i in range(lf):
            next_i=(i+1)%lf
            v1=face[i]
            v2=face[next_i]
            end=locate_end(v1,v2,orig_face,edges)
            if len(end)==1:
                unoriented=True
            if v1+v2 in shadow_edges or v2+v1 in shadow_edges:
                disp=i
        if not unoriented:
            continue  #next face
        for i in range(lf):
            s=(i+disp)%lf
            e=(s+1)%lf
            v1=face[s]
            v2=face[e]
#            if v1+v2 in shadow_edges or v2+v1 in shadow_edges:
#                continue
            v1i=0
            v1i=orig_face.index(v1)
            ends=edges[v1i]
            for end in ends:
#                if len(end)==1:  # no direction yet
#                    prev_dir=""
                if end[0]!=v2:
                    continue
                if len(end)==2:
                    dir=end[1]
                    if prev_dir != "" and dir !=prev_dir:
                        
                        special_found=True
#                        print "special3",v1+v2+dir
                        process_special(v1+v2,dir,face,edges,faces,vertices,diag)
                        break
                    else:
                        if v1+v2 in shadow_edges or v2+v1 in shadow_edges: 
                            #previous should always be a shadow edge
                            #to decide which edge is definitely special
                            prev_dir=dir
                            prev_v1=v1
                            prev_v2=v2
                break
            if special_found:
                break
                        
def process_special(pair,dir,face,edges,faces,vertices,diag):
    # the orientation of all other edges in the face have the
    # opposite direction to the special edge
    #print pair,dir,"is special"
    shadow_edges=vertices[1:]
    lf=len(face)
    dirx='i'
    if dir=='i':
        dirx='o'
    for i in range(len(face)):
        next_i=(i+1)%lf
        v1=face[i]
        if v1==pair[0]:
            continue
        v2=face[next_i]
        if v1+v2 in shadow_edges or v2+v1 in shadow_edges:
            continue
        end=locate_end(v1,v2,vertices[0],edges)
        if len(end)==1:
            res=deduce(v1+v2+dirx,edges,faces,vertices,diag)

    
def full_up(edges):
    #return True if all edges are now oriented
    undirected=0
    for ends in edges:
        for end in ends:
            if len(end)==1:
                undirected+=1
    return undirected

def get_labels(edges):
    label=[]
#    print "!!!!",edges
    for ends in edges:
        corner=''
        i=0
        last=''
        for end in ends:
            if i != 1:
                corner+=end[1]
            else:
                last=end[1]
            i+=1
        corner+=last
        label.append(corner)
        letters=convert_label(label)
#    print "!!!! label=",letters
    return letters

def convert_label(label):
    
    ll=len(label)
    labelx=[]
    letters=[]
    for i in range(ll):
        labelx.append(remove_ioi_oio(label[i]))
    for i in range(ll):
        prev_i=(i-1)%ll
        next_i=(i+1)%ll
        check_i=next_i
        if labelx[i]=='ii':
            dir='o'
            if label[i].endswith('ioi'):
                letters.append('A')
            elif label[i].startswith('ioi'):
                letters.append('a')
            elif label[next_i][1] == 'i':
                letters.append('A')
            else:
                letters.append('a')

        elif labelx[i]=='oo':
            dir='o'
            if label[i].endswith('oio'):
                letters.append('b')
            elif label[i].startswith('oio'):
                letters.append('B')
            elif label[next_i][1] == 'i':
                letters.append('B')
            else:
                letters.append('b')

        elif labelx[i]=='iio':
            letters.append('X')
        elif labelx[i]=='oii':
            letters.append('x')
        elif labelx[i]=='ooi':
            letters.append('y')
        elif labelx[i]=='ioo':
            letters.append('Y')
        elif labelx[i]=='ooii':
            letters.append('z')
        elif labelx[i]=='iioo':
            letters.append('Z')
        elif labelx[i]=='io':
            letters.append('m')
        elif labelx[i]=='oi':
            letters.append('l')
        else:
            letters.append(label[i])
    return letters
def remove_ioi_oio(label):
    if len(label)<4:
        return label
    replaces=['ioi','IOI','oio','OIO']
    for i in range(len(replaces)):
        keep_checking=True
        replace=replaces[i]
        while keep_checking:
            keep_checking=False
            if replace in label:
                r=label.index(replace)
                label=label[:r]+replace[0]+label[r+3:]
                if len(label)<4:
                    return label
                keep_checking=True
    return label        
def look_for_next_edge_to_try(edges,faces,vertices):
    orig_face=vertices[0]
    shadow_edges=vertices[1:]
    res=0
    for face in faces:
        lf=len(face)
        for i in range(len(face)):
            next_i=(i+1)%lf
            v1=face[i]
            v2=face[next_i]
            v1i=0
            if not (v1+v2 in shadow_edges) or (v2+v1 in shadow_edges):
                v1i=orig_face.index(v1)
                ends=edges[v1i]
                for end in ends:
                    if end == v2:
                        return v1+v2
    return ""
