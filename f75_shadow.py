from copy import deepcopy
from f75_shadow2 import *
from f75_shadow4 import *

labtofig_hash={}
check_ok=False
# project = automate shadow edge checking
# for octagon calculate all shadow edges and corner labelling
# for 3 b-segments show that no possible shadowing for n2<8
lr=8  # change to 9 for F(8,5) proof??

def make_labfig_hash(f3):
    f3list=f3.readlines()
    for xx in f3list:
        if ',' in xx:
            kv=xx.split(',')
            labtofig_hash[kv[0]]=kv[1][:-1]

def shadow_edge_logic_script (script):
    diag=False
    vertices=[]
    faces=[]
    print script
    f1=open(script,'r')
    labels=[]
    filterit=False
    filter_xy=False
    showit=False
    ckey=""
    for line in f1:
        line=line.rstrip()
        if line.startswith("?"):
            keyx=line[1:]
            manage_drawing_sets(keyx)
            if diag:
                print keyx
                print show_ngon(keyx)
        elif line.startswith("="):
            keyx=line[1:]
            create_ngon(keyx)
            ckey=keyx
        elif line.startswith("apply"):
            tokens=line.split(' ')
            if len(tokens) != 5:
                print "syntax error in",line
                continue
            akey=tokens[1]
            avertices=tokens[3]
            minskip=tokens[4]
            base_vertices=vertices[1:]
            lb=len(base_vertices)
            bv=""
            for b in base_vertices:
                bv+=b+','
            bv=bv[:-1]
            bvx=bv.split(',')
            draw_command_set=generate_draw_commands(akey,avertices,vertices,int(minskip))
 
#            print draw_command_set,"generated"
            minuses=''
            for draw_commands in draw_command_set:
                print_it=False
                #if draw_commands == ['5A','68','69','XX']:
                #    print "*****",vertices[1:],minuses,draw_commands
                #    print_it=True

                if minuses != "":
                    #print minuses[:-1]
                    mx=minuses.split(',')
                    for m in mx:
                        do_shape_command(m,vertices,faces,labels,diag,ckey)
                    minuses=''
                for b in bvx:
                    do_shape_command('+'+b,vertices,faces,labels,diag,ckey)
                wrong=False
                for draw_command in draw_commands:
                    #print '+'+draw_command
                    xxx=do_shape_command('+'+draw_command,vertices,faces,labels,diag,ckey)
                    if xxx != "":
                        print xxx
                        wrong=True
               # print vertices[1:],'ch2'
                if not wrong:
                    #print "doing ch2"
                    global check_ok
                    check_ok=True
                    do_shape_command('ch2',vertices,faces,labels,diag,ckey)
                    check_ok=False
                    if print_it:
                        print "++++++++",vertices[1:]
                for i in range(len(vertices[1:])):
                    minuses+='-,'
                minuses=minuses[:-1]
        elif line.startswith("diag"):
            diag=True
        elif line.startswith("filter_xy"):
            filter_xy=True
        elif line.startswith("nofilter_xy"):
            filter_xy=False
        elif line.startswith("filter"):
            filterit=True
        elif line.startswith("nofilter"):
            filterit=False
        elif line.startswith("show"):
            showit=True
        elif line.startswith("noshow"):
            showit=False
        elif line.startswith("nodiag"):
            diag=False
        elif line.startswith("quit"):
            if len(labels)>0:
                show_labels(labels,diag,filterit,filter_xy,vertices)
            return
        if line.startswith("#"):
            #print ""
            print line
            continue

        if showit:
            print line
            
        if line.startswith('*'):
            show_labels(labels,diag,filterit,filter_xy,vertices)
            labels=[]
            vertices=[]
            faces=[]
            vertices0=line[1:].split(',')
            vertices.append(vertices0)
            faces.append([vertices[0]])
            labels=[]
            update_ngon(ckey,vertices[0])

           # print ""
            #print vertices[0]
        else:
            #commands to be actioned
           # print line
            comms=line.split(',')
            if len(comms[0])==2:
                # an implicit removal of all shadow edges
                # generate the right number of '-''s
                if len(vertices)>1:
                    no_minuses=len(vertices[1:])
                    pre_com=""
                    while no_minuses>0:
                        pre_com+='-,'
                        no_minuses-=1
                    line=pre_com+line
                    comms=line.split(',')
                    if diag:
                        print "generated line"
                        print line
            for comm in comms:
                if len(comm)==1 and comm.isdigit():
                    if 'a' in vertices[0]:
                        # rebuild face by inserting 'comm' vertices
                        vertices=rebuild_face(vertices,int(comm))
                        faces=[]
                        faces.append([vertices[0]])
                        #print vertices
                else:
                    if len(comm)==2:
                        # adding an edge
                        comm='+'+comm
                    do_shape_command(comm,vertices,faces,labels,diag,ckey)
    if len(labels)>0:                
        show_labels(labels,diag,filterit,filter_xy,vertices)
    f1.close()
def rebuild_face(vertices,no_inserted):
    new_vertices=[]
    base_face=vertices[0]
    if len(base_face) < 3:
        return vertices
    new_face=[]
    new_face+=base_face[:2]
    r=2
    while base_face[r].isdigit():
        r+=1
    for i in range(1,no_inserted+1):
        new_face.append(str(i))
    new_face+=base_face[r:]
    new_vertices.append(new_face)
    return new_vertices
    
    
def show_labels (labels,diag,filter_it,filter_xy,shape):
   if len(labels) < 1:
       return
   print "labels associated with shape",shape[0]
   if filter_xy:
        print 'xy exceptions'
   xys=['xy','yx','XY','YX']
 
   for label in labels:
        if filter_it:
            Apresent=False
            Bpresent=False
            #filter results according to Fig 7.2
            filterA=['ab Y','AB X','y BA','x ba']
            filterB=['Y ZA','X ma','az y','Al x']
            for filtA in filterA:
                if filtA in label[0]:
                    Apresent=True
                    break
            for filtB in filterB:
                if filtB in label[0]:
                    Bpresent=True
                    break
            if not (Apresent and Bpresent):
                continue
        if filter_xy:
            #print label,"to be xy filtered"
            not_this=True
            if len(label)>=3:
                #print "label[2]=",label[2]
                #if label[2]==33:
                    #print "double disconnected xy sequences"
                not_this=False
            else:
                #print "check single"
                not_this=check_single_xy_seq(label)
            #print "not this=",not_this
            if len(label) == 2:
                labx=label[0]
                xys=['xyx','XYX','yxy','YXY']
                if len(labx)==12:
                    xys=['xyxyx','XYXYX','yxyxy','YXYXY']
                if len(labx)<14:
                    for xy in xys:
                        if xy in labx:
                            not_this=False
                            break
                if not_this:
                    # look for 'abY...Yma or Xma'
                    if 'abY' in labx:
                        if ('Yma' in labx) or ('Xma' in labx):
                            not_this=False
                            
            
            #not_this=False
            
            if not_this:
                continue
        if diag:
            print label[0]
            print label[1:]
            continue
        labx=label[0]
        if not (('i' in label[0]) or ('I' in label[0])):
            print label[:2],
            if labtofig_hash.has_key(label[0]):
                print labtofig_hash[label[0]] 
            elif labx[2]==' ':
                #print labx,"!!!!!"
                
                if ' ' in labx[3:]:
                    i=labx[3:].index(' ')
                keyx = labx[3:3+i]
                if labtofig_hash.has_key(keyx):
                    print labtofig_hash[keyx]
                else:
                    print ""
            else:
                print ""
     

def do_shape_command(inpl,vertices,faces,labels,diag,ckey):
        global check_ok
        if inpl.startswith("ch"):
            if inpl.startswith("ch2"):
                if not check_ok:
                    return
                drawing=vertices[1:]
#                print "ch2 on",drawing

                ll=len(vertices[0])
                store_and_return=False
                double_disco=False
                max_xy=0
                if ll > 8 and ckey != "":
                    max_xy=get_counts(ll,drawing)
 #                   print 'max_xy=',max_xy
                    if max_xy < 0:
                        n2=ll+max_xy
                        #print "disconnected double_sequence,n2=",n2
                        double_disco=True
                        # if not disconnected
                        if n2>8:
                            store_and_return=True
                    else:
                        # max_xy >0 => single xy-sequence
                        n2=ll-max_xy
                        if n2>9:
                        #    return
                            store_and_return=True
 #               print 'store_and_return=',store_and_return,drawing            
                if store_and_return:
                    if ll < 16:
                        update_ngon(ckey,drawing)
                    return
                labelsx = check_shape2(vertices,faces,diag)
                #print 'labelsx=',labelsx
                if len(labelsx)==0:
                    if diag:
                        print "NAC shape could not be labelled"
                        return "NAC! shape could not be labelled"
                else:
                    update_ngon(ckey,drawing)
 
                    #print labelsx[0][0]
                    if diag:
                        print "**",labelsx
                    N_labels=[]
                    for label in labels:
                        N_labels.append(label[0])
                     
                    for label in labelsx:
                        if not ('i' in label[0] or 'I' in label[0]):
                            if diag:
                                print label[0]
                        if not label[0] in N_labels:
                            if double_disco:
                                #record double disco by max_xy
                                label.append(max_xy)
                            labels.append(label)
            elif inpl.startswith("ch1"):
                check_shape(vertices,faces,diag)

        if inpl.startswith("+"):
            if len(inpl) == 3:
                s=inpl[1]
                e=inpl[2]
                if s+e in vertices[1:] or e+s in vertices[1:]:
                    return "dup"
                face=vertices[0]
                si=face.index(s)
                ei=face.index(e)
                if si>ei:
                    (si,ei)=(ei,si)
                    (s,e)=(e,s)

                if check_valid_line(vertices,s,e) and \
                   check_no_crossing(vertices,s,e):
                    vertices.append(s+e)
                    update_faces(faces,s,e)
                   # print vertices
                   # print faces[-1]
        if inpl.startswith("-"):
            if len(vertices)>1:
                vertices.pop()
                faces.pop()
                #print vertices
                #print faces[-1]
        return ""    
def process_shape(vertices,faces):
#    print type(vertices)
    while type(vertices) != int:
        inpl=raw_input("operation? ")
        if inpl.startswith("q"):
            break
        do_shape_command(inpl,vertices,faces)
    return vertices

def update_faces(faces,s,e):
    #print "**",faces,s,e
    facesx=deepcopy(faces[-1])
    face_len=len(faces[0][0])
    new_faces=[]
    for face in facesx:
        if not (s in face and  e  in face):
            new_faces.append(face)
        else: # split the face in two
            lf=len(face)
            si=face.index(s)
            ei=face.index(e)
            if si>ei:
                (si,ei)=(ei,si)
                (s,e)=(e,s)
            i=s
            face1=[s]
            i=si+1
            while i<=ei:
                face1.append(face[i])
                i+=1
            
            face2=[e]
            i=(ei+1)% lf
            while i!=si:
                face2.append(face[i])
                i=(i+1) % lf
            face2.append(s)

            new_faces.append(face1)
            new_faces.append(face2)
    facesx=new_faces
    faces.append(facesx)

def check_no_crossing(vertices,s,e):
    # for each existing line determine the two sets of points separated
    # by its end points. s and e must then be in the same set for there
    # to be no crossing
    vv=vertices[0]
    lvv=len(vv)
    for exl in vertices[1:]:
#        print exl[0],exl[1]
        exl0i=vv.index(exl[0])
        exl1i=vv.index(exl[1])
        si=vv.index(s)
        ei=vv.index(e)

        if exl0i > exl1i:
            (exl0i,exl1i)=(exl1i,exl0i)
        set1=range(exl0i+1,exl1i+1)
        set2=[exl[0],exl[1]]
  #      print set1,set2,s,e,si,ei
        if si in set1 and ei in set1:
            continue
        if s in set2 or e in set2:
            continue
        if si not in set1 and ei not in set1:
            continue
        print s+e+" crosses with "+exl[0]+exl[1]
        return False
    return True

def check_valid_line(vertices,s,e):
    vv=vertices[0]
    lvv=len(vv)
    if s in vv and e in vv:
        si=vv.index(s)
        ei=vv.index(e)
        diff=abs(si-ei)
        if not (diff==1 or diff==lvv-1):
            return True
        return False

def check_shape(vertices,faces,diag):
    global check_ok
    check_ok=False
    if diag:
        print vertices
        print faces[-1]
    orig_face=vertices[0]
    ll=len(orig_face)
    no_s_edges=len(vertices)-1
    total_unknowns = no_s_edges
    numbers=[]
    #work out the lengths of the shadow edges
    for i in range(no_s_edges):
        numbers.append(0)
    while total_unknowns>=0:
    # calculate shadow edge lengths for faces
        if total_unknowns==0:
            total_unknowns=-1
        # order faces so that triangles are done first
        facesx=[]
        for face in faces[-1]:
            if len(face)==3:
                facesx.append(face)
        for face in faces[-1]:
            if len(face)>3:
                facesx.append(face)
        for face in facesx:
            skip_for_now=False
            length_known=True
            if diag:
                print "face",face
            i=0
            s_edges=0
            s=""
            unknown_s=-1
            total=0
            lf=len(face)
            while i<lf:
                v1=face[i]
                v2=face[(i+1)%lf]
                #if unknowns<0:
                #    print v1,v2,
                i1 = vertices[0].index(v1)
                i2 = vertices[0].index(v2)
                if abs(i2-i1) ==1 or abs(i2-i1) == ll-1:
                    # periphery edges
                    #if unknowns<0:
                     #   print 1
                    total+=1
                else:
                    if i1>i2:
                        (v1,v2)=(v2,v1)
                    sei=vertices[1:].index(v1+v2)
                    if numbers[sei]>0:
                        #if unknowns<0:
                          #  print v1,v2,"=",numbers[sei]
                        total+=numbers[sei]
                    else:
                        length_known=False
                        if unknown_s>=0:
                            #already 1 unknown - come back later
                            unknown_s=-2
                            skip_for_now=True
                            break
                        else:
                            unknown_s=sei
                i+=1
            if skip_for_now:
                continue
            if length_known: #?????#
               #print face,"has length,",total
               if total!=lr:
                    if diag:
                       print "NEC! face",face,"has length",total
                    return "not ok"
 
            if unknown_s>=0:
                s_len=lr-total
                if s_len <= 0:
                    if diag:
                        print "NEC! face",face,"has length >",lr
                    return "not ok"
 
                numbers[unknown_s]=lr-total
                if diag:
                    print "deduce",vertices[1:][unknown_s], "is",numbers[unknown_s]
                
                total_unknowns-=1
    check_ok=True
    if diag:
        print "lengths ok"
    return "lengths ok"








