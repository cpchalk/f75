from copy import deepcopy
from f75_shadow3 import *
def check_shape2(vertices,faces,diag):
    #print "check orientation of figure"
    #all shadow edges belonging to a face must have the same direction
    #one edge of a face must be the 'special edge' (diff direction to the others)
    # 2 special edges sharing the same shadow edge must have the same direction
    # 
    orig_face=vertices[0]
    s_edges=vertices[1:]
    if diag:
        print 'labelling face',orig_face,'with edges',s_edges

    lf=len(orig_face)
    edges=[]
    for i in range(len(orig_face)):
      prev_i=(i-1)%lf
      next_i=(i+1)%lf
      edges.append([orig_face[prev_i],orig_face[next_i]])
      label=orig_face[i]
      for se in s_edges:
        if se[0]==label:
          edges[i].append(se[1])
        if se[1]==label:
          edges[i].append(se[0])
    organise_edges_anticlockwise(edges,orig_face,diag)
    labels=orient_edges(vertices,edges,faces[-1],diag)
    labels2=[]
    return labels

def normalize(label):
    to_sort=[]
    lab=""
    start_letter='b'
    if  'a' in label or 'A' in label:
        start_letter='a'
    labelr=[]
    ll=len(label)
    i=ll
    j=0
    while i > 0:
        i-=1
        let=label[i]
        labelr.append(invert_letter(let))
    to_sort+=get_starts(label,start_letter)
    to_sort+=get_starts(labelr,start_letter)
    to_sort.sort()
    return to_sort[0]

def invert_letter (let):
    if let==' ':
        ilet=' '
    elif let=='l':
        ilet='m'
    elif let=='m':
        ilet='l'
    elif let.islower():
        ilet=let.upper()
    else:
        ilet=let.lower()
    return ilet

def get_starts(label,s):
    starts=[]
    ll=len(label)
    for i in range(ll):
        if label[i]==s:
            new_label=''
            j=i
            lim=i+ll
            while j < lim:
                t=j%ll
                new_label+=label[t]
                #print new_label,t,j,lim
                j+=1
            starts.append(new_label)
    #print "!!!",starts,"from",label
    return starts                       

def organise_edges_anticlockwise(edges,orig_face,diag):
    # organise shadowedges anticlockwise about vertex
    if diag:
        print 'organise_edges_anticlockwise'
    lf=len(orig_face)
    v1=0
#    print '***',len(edges)
    for ends in edges:
#        print v1
        if len(ends) <= 3:
            v1+=1
            continue
        to_sort=[]
        shadow_ends=ends[2:]
        for end in shadow_ends:
            endi=orig_face.index(end)
            to_sort.append((v1-endi)%lf)
        to_sort.sort()
 #       print "**!!",to_sort
        for i in range(len(to_sort)):
            si=(v1-to_sort[i])%lf
            v2=orig_face[si]
            ends[2+i]=v2
 #       print ends
 #       print shadow_ends
        v1+=1
            
        
def orient_edges (vertices,edges,faces,diag):
    if diag:
        print 'orient_edges'
    orig_face=vertices[0]
    #print orig_face
    labels=[]
    try_stack = [] # try i then o for edges with unknown orientation
    edges_stack =[]
    edges_stack.append(deepcopy(edges))
    loop=0
    next_edge=""
    while len(edges_stack) > 0:
        if loop==2000:
            print "break loop"
            break
        loop+=1
        edges=edges_stack[-1]
        if next_edge != "":
            try_stack.append(next_edge+'i')
            if diag:
                print 'try',next_edge+'i'
            next_edge=""
        elif try_stack==[]:
            # find first shadow edge and suppose it is inward
            for i in range(len(edges)):
                start_v=orig_face[i]
                end_vs=edges[i]
                if len(end_vs)>2:
                    #first shadow edge
                    end_v=end_vs[2]
                    try_stack.append(start_v+end_v+'i')
                    if diag:
                        print 'try',start_v+end_v+'i'
                    break
        else:
            #we've returned from a contradiction or complete orientation
            last_tried=try_stack[-1]
            try_stack.pop()
            if diag:
                print 'pop',last_tried
            if last_tried.endswith('i'):
                last_tried=last_tried[:2]+'o'
                try_stack.append(last_tried)
                if diag:
                    print 'try',last_tried
            elif last_tried.endswith('o'):
                if try_stack==[]: # we've tried everything
                    if diag:
                        print "finished in orient edges"
#                    print 'finished'
                    break
                edges_stack.pop()
                continue
        #print "try",try_stack
        if len(try_stack) > 0:
            edges_stack.append(deepcopy(edges))
            edges=edges_stack[-1]
            if diag:
                print 'using..'
                print edges
            res=deduce(try_stack[-1],edges,faces,vertices,diag)
            if diag:
                print 'to get...'
            if res==-99:
                if diag:
                    print 'error  pop'
                edges_stack.pop()
                continue
            prev_undirected=1000
            undirected=1000
            while True:
                undirected=full_up(edges)
                if undirected==0:
                    if diag:
                        print "fully directed"
                        print edges
                    break
                if undirected==prev_undirected:
                    if diag:
                        print 'no new directed'
                    break
                prev_undirected=undirected
                if diag:
                    print edges
                # look for border edges which are special
                # and so orient the rest of the border edges
                if diag:
                    print 'deduce3 - determine special border edges',
                res=deduce3(edges,faces,vertices,diag)
                if diag:
                    print 'to get...'
                if res==-99:
                    if diag:
                        print 'error'
                    break
                # deduce that single border edges left over must be special
                if diag:
                    print 'deduce2 - look for single left over border edges..'
                    print 'to get ...'
                res=deduce2(edges,faces,vertices,diag)
                if diag:
                    print 'to get...'
                if res==-99:
                    if diag:
                        print 'error'
                    break

            if res==-99:
                if diag:
                    print 'error - pop'
                edges_stack.pop()
                continue
            undirected=full_up(edges)
            #print "***",edges
            N_label=""
            if undirected==0: # everything is oriented
                              # but might not be reduced
                if diag:
                    print 'validate orientation'
                if validate(edges,faces,vertices): 
                    label=get_labels(edges)
                    if diag:
                        print 'label=',label
                    orig_face=vertices[0]
                    if len(label)!=len(orig_face):
                        continue
                    if 'a' in orig_face and '1' in orig_face:
                        prev="q"
                        i=0
                        for vv in label:
                            if (not orig_face[i].isalpha()) and prev.isalpha():
                                N_label+=' '
                            elif orig_face[i].isalpha() and not prev.isalpha():
                                N_label+=' '
                            N_label+=vv
                            prev=orig_face[i]
                            i+=1
                        if N_label.count(' ') == 2:
                            N_label=normalize_to_ab(N_label)
                    else:
                       N_label=normalize(label)
                    N_labels=[]
                    lines=vertices[1:]
                    for label in labels:
                        N_labels.append(label[0])
                    if N_label not in N_labels:
                        labels.append([N_label,lines])
                    else:
                        #print "***SAME",N_label,lines
                        ix=N_labels.index(N_label)
                        if lines not in labels[ix]:
                            labels[ix].append(lines)
                else:
                    if diag:
                        print 'validation fails on...'
                        print edges
                edges_stack.pop()

                #try_stack.pop()
            else:
                next_edge=look_for_next_edge_to_try(edges,faces,vertices)
    return labels

def normalize_to_ab(N_label):
    # for format ?? ?..? ??....?- try to arrange that ab starts the label
    labelr=""
    if ' BA' in N_label:
        #print "***",N_label
        i=N_label.index(' BA')
        i+=3
        j=i
        while i > 0:
            i-=1
            let=N_label[i]
            labelr+=invert_letter(let)
        i=len(N_label)
        while i>j:
            i-=1
            let=N_label[i]
            labelr+=invert_letter(let)
    else:
        labelr=N_label
    return labelr

            

        
