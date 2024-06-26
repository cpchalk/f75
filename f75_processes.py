IF_hash={}
charge_hash={}
next_hash = {}
neighbour_hash = {}
post_pre_rules = [['a','axz','amY'],['b','bmX','byz'],
                  ['x','BYZ','amY'],['y','bmx','AXZ'],
                  ['z','bmX','amY'],['l','BYZ','AXZ'],
                  ['A','Aly','AXZ'],['B','BYZ','Blx'],
                  ['X','Aly','byz'],['Y','axz','Blx'],
                  ['Z','Aly','Blx'],['m','axz','byz']]
vertex_labels = [['a',['axY','aazm','azma','aaaaa','azXym']],
                 ['b',['bmz','bbXy','bXyb','bbbbb','bXlZy']],
                 ['x',['xYa','xBBY','xZAlY','xBYzm']],
                 ['y',['yXA','ybbX','ymazX','ybXlZ']],
                 ['z',['zbm','zmaa','zXyma','zmxBY']],
                 ['l',['lBZ','lZAA','lYxZA','lZybX']],
                 ['A',['AyX','AlZA' ,'AAlZ','AAAAA','AlYxZ']],
                 ['B',['BZl','BYxB','BBYx','BBBBB','BYzmx']],
                 ['X',['XAy','Xybb','XymAZ','XlZyb']],
                 ['Y',['Yax','YxBB','YxZAl','YzmxB']],
                 ['Z',['ZlB','ZAAl','ZAlYx','ZybXl']],
                 ['m',['mzb','maaz','mazXy','mxBYz']]]

def find_next(res):
    keyx=res[5]
    valx=res[-1]
    if next_hash.has_key(keyx):
        vals=next_hash[keyx]
        for val in vals:
            if val[:2]==valx:
                valx=val
                break
            if val[1:3]==valx:
                valx=val
                break
    return valx 

def pcd2(chargexx):
    chargex=chargexx
    not_edge=''
    if len(chargexx)>3:
        (chargex1,chargex2,not_edge)=chargexx.split(' ')
    charge1=0
    charge2=0
    
    print "pcd2",chargex
    if chargex1.isdigit():
        charge1=int(chargex1)
    if chargex2.isdigit():
        charge2=int(chargex2)
 
        
    filterx=[0,0,'?','?','??']
    resx=print_charge_hash(filterx,False)
    #print len(resx),"results"
    resxx=[]
    for res in resx:
        if (res[2]>=charge1) and (res[2]<=charge2):
            if not_edge !='':
                if res[-1] == not_edge:
                    #print res[-1],not_edge
                    continue
            valx=find_next(res)
            resxx.append(res[:2]+res[3:5]+[valx]+[res[2]]+res[5:6])
    resxx.sort()
    prev=[]
    for res in resxx:
        if res[:6] != prev:
            print res
        prev=res[:6]
        
def pcd3(chargexx):
    chargex=chargexx
    edge=''
    if len(chargexx)>3:
        (chargex1,chargex2,edge)=chargexx.split(' ')
    charge1=0
    charge2=0
    
    print "pcd3",chargex
    if chargex1.isdigit():
        charge1=int(chargex1)
    if chargex2.isdigit():
        charge2=int(chargex2)
 
        
    filterx=[0,0,'?','?','??']
    resx=print_charge_hash(filterx,False)
    #print len(resx),"results"
    resxx=[]
    for res in resx:
        if (res[2]>=charge1) and (res[2]<=charge2):
            if edge !='':
                if res[-1] != edge:
                    continue
            valx=find_next(res)
            resxx.append(res[:2]+res[3:5]+[valx]+[res[2]]+res[5:6])

    resxx.sort()
    prev=[]
    for res in resxx:
        if res[:6] != prev:
            print res
        prev=res[:6]
    
def print_highest_charge(edge,deg1,use_all_deg):
    factor=0.5
    if use_all_deg:
        factor=1.0
    surplus_row=[0,0,0,0,5,8,10]
    filterx=[deg1[0],deg1[1],'?','?',edge]
    resx=print_charge_hash(filterx,False)
    hc=-100
    hdegs=12
    hh=[]
    if len(resx)>0:
        hh=resx[0]
    for res in resx:
        if res[2]>1000:
            continue
        d1=abs(res[0])
        d1=min(d1,6)
        d2=abs(res[1])
        d2=min(d2,6)
        s1=surplus_row[d1]
        s2=surplus_row[d2]
        s=factor*s1+0.5*s2
        charge=res[2]
        if deg1 != [0,0]:
            charge=res[2]-s
#        print res[2],d1,d2,s1,s2,s,charge
        if charge>hc:
            hc=charge
            hh=res
    return hh,hc

def print_charge_hash(filterx,display_it):
    if display_it:
        print 'v1,v2,charge,s1,s2,config,charge_key(t1+t2)'
    resx=[]
    keysx=charge_hash.keys()
    datax=[]
    for keyx in keysx:
        valx=charge_hash[keyx]
        displayx=[]
        for val1 in valx:
            displayx=[]
            for items in val1:
                displayx.append(items)
                
            displayx.append(keyx)
            datax.append(displayx)
    datax.sort(key=lambda datax:datax[5])
    prev_val=[]
    for dat1 in datax:
        if dat1[:5] == prev_val:
            continue
        prev_val=dat1[:5]
        display=False
        if len(filterx)==5:
            display=True
            #if filterx[0] != 0:
             #   if filterx[0] != dat1[0]:
             #       display=False
             # 3 means 3, but 4 means anything from 4 and above
             # 44, 55  means must match 4, 5
            if filterx[0] != 3 and filterx[0] != 0:
                if dat1[0] == 3:
                    display=False
            if filterx[1] != 3 and filterx[1] != 0 :
                if dat1[1] == 3:
                    display=False
            if filterx[1] != 3 and filterx[1] != 0 :
                if dat1[1] == 3:
                    display=False
            if filterx[0] == 3:
                if dat1[0] != 3:
                    display=False
            if filterx[1] == 3:
                if dat1[1] != 3:
                    display=False

            if filterx[0] > 40:
                if dat1[0]*11 != filterx[0]:
                    display=False
            if filterx[1] > 40:
                if dat1[1] *11!= filterx[1]:
                    display=False
            #if filterx[1] != 0:
            #    if filterx[1] != dat1[1]:
            #        display=False
            if filterx[2] != '?':
                if filterx[2] != dat1[3]:
                    display=False
            if filterx[3] != '?':
                if filterx[3] != dat1[4]:
                    display=False
            if filterx[4][0] != '?':
                if filterx[4][0] != dat1[-1][0]:
                    display=False
            if filterx[4][1] != '?':
                if filterx[4][1] != dat1[-1][1]:
                    display=False
             
            if (display and display_it):
                print dat1
            elif display:
                resx.append(dat1)
        else:
            if filterx==[]:
                print dat1
    return resx

def get_vertex_edge_charges(degv1,degv2,edge):
    results=[]
    hk=make_charge_hk(edge[0],edge[1])
    if not charge_hash.has_key(hk):
        return results
    values=[]
    valuesx=charge_hash[hk]
    e0=edge[0]
    e1=edge[1]
    swap01_34=False
    changecase=False
    if e0.lower() > e1.lower():
        #swap the degs and source values!!!
        (e0,e1)=(e1,e0)
        swap01_34=True
    if e0.isupper() or e0=='m':
        changecase=True
    for valx in valuesx:
        v3=valx[3]
        v4=valx[4]
        v0=valx[0]
        v1=valx[1]
        if swap01_34:
            (v0,v1,v3,v4)=(v1,v0,v4,v3)
        if changecase:
            v3=swap_case(v3)
            v4=swap_case(v4)
        values+=[[v0,v1,valx[2],v3,v4,valx[5],valx[6]]]
 
 
    prev_value=[0,0,0]
    for value in values:
        d1=abs(value[0])
        d2=abs(value[1])
        if (((d1 >= degv1) and (d2 >= degv2) or (d1 >= degv2) and (d2 >= degv1))):
            if value[:5] !=prev_value:
                results.append(value)
            prev_value=value[:5]
    return results

def get_v_label(letter,length):
    results=[]
    if length > 5:
        print "6!!"
        length=5
    for vl in vertex_labels: 
        if vl[0]==letter:
            for ans in vl[1]:
                if len(ans) == length:
                    results.append(ans)
    return results

def update_neighbour_hash(keyx,neighbour):
    if len(neighbour)>=2:
        if neighbour[0].isdigit():
            neighbour_hash[keyx]=neighbour
            #print "****",keyx,neighbour
    
def get_neighbour(keyx):
    valx ="?"
    if neighbour_hash.has_key(keyx):
        valx=neighbour_hash[keyx]
    return valx

def make_next_hash(f2):
    f2list=f2.readlines()
    key1=""
    for xx in f2list:
        if len(xx) >= 3:
            if xx[1]=='.':
                if xx[:2]=='5.':
                    key1=xx[:3]
                else:
                    key1=xx[:4]
                if key1 in ['4.27','4.28','4.29']:
                    key1=""
            elif key1 != "":
                zz=xx.split(',')
                if len(zz)>1:
                    keyx=key1+zz[0]
                    valx=zz[1:-1]
                    next_hash[keyx]=valx
    
def load_file(f1,configs):
    val1=""
    f1list=f1.readlines()
    for xx in f1list:
        if xx.startswith('#'):
            # comment
            continue
        elif  xx.startswith('4'):
            val1=xx.rstrip()
        elif xx.rfind(',')>0:
            ss=xx.split(',')
            if len(ss)>0:
                val=val1+ss[0]
                #print val
            config=[]
            config.append(val)
            regions=(','.join(ss[1:])).rstrip().split(';')
            i=0
            next_vv=1
            for region in regions:
                regionx=[]
                #config.append(region)
                first_vv=next_vv    
                vertices=region.split(',')
                if len(vertices) != 4:
                    if len(vertices)==1:
                        # assume this defines a neighbour
                        update_neighbour_hash(val,vertices[0])
                    continue
                rkey=[]
                i=0
                while i < 4:
                    vertex=vertices[i]
                    if len(vertex)==0:
                        print val,region
                        i+=1
                        continue
                    # extract charge
                    c=0
                    while vertex[c].isdigit():
                        if c==len(vertex) - 1:
                            break
                        c+=1
                    while c < len(vertex):
                        if vertex[c].isdigit():
                            if c < len(vertex)-1:
                                if vertex[c+1]=='.' or vertex[c+1] == '=':
                                    c+=2
                                    continue
                            break
                        c+=1
                    vertex_s=vertex
                    charge=0
                    if c < len(vertex):
                        vertex_s=vertex[:c]
                        charge=int(vertex[c:])
                    if not vertex_s[0].isdigit():
                        regionx.append([next_vv,vertex_s,charge])
                        next_vv+=1
                        i+=1
                        continue
                    k=0
                    vv=0
                    while vertex_s[k].isdigit():
                        vv=vv*10 + int(vertex_s[k])
                        k+=1
                    regionx.append([vv,vertex_s[k:],charge])
                    i+=1
                config.append(regionx)                   
            configs.append(config)
    return f1list
  
def strip_trailing_non_alpha (name):
    if not name[-1].isdigit():
        # strip off trailing non alpha
        e=-1
        while not name[e].isalpha():
            e-=1
            if len(name)+e == 0:
                return name
        return name[:e+1]
    return name

def make_hk(source_edge,target_edge):
    hk1=source_edge[0]
    hk2=target_edge[0]
    hk3=source_edge[1]
    hk4=target_edge[1]
    hk_list=[hk1,hk2,hk3,hk4]
    for i in range(4):
        if not hk_list[i].isalpha():
            return ""
    if hk1.lower() > hk3.lower():
        (hk_list[2],hk_list[0])= (hk_list[0],hk_list[2])
        (hk_list[3],hk_list[1])= (hk_list[1],hk_list[3])
    if hk_list[0].isupper():
        for i in range(4):
            if hk_list[i].isupper():
                hk_list[i] = hk_list[i].lower()
            else:
                hk_list[i] = hk_list[i].upper()


    hk=hk_list[0]+hk_list[1]+hk_list[2]+hk_list[3]
    return hk

def make_4IF_entry(config,source_edge,target_edge,labels):
    # form hash key
    hk=make_hk(source_edge,target_edge)
    hk+=","+labels
    val=[]
    update=True
    if IF_hash.has_key(hk):
        val=IF_hash[hk]
        last_val=val[-1]
        len=3
        if last_val[3].isdigit():
            len=4
        if last_val[:len]==config[:len]:
            update=False
    if update:
        val.append(config)
        IF_hash[hk]=val
        
def find_overlaps (configs):
    prev_group="0.0"
    for config in configs:
        this_group=config[:3]
        if config[0][3].isdigit():
            this_group=config[0][:4]
        regions = config[1:]
        
        if len(regions) == 1:
            continue
        regions=regions[1:]
        region_id=1
        for vertices in regions:
            region_id+=1
            relevant=False
            for v in range(len(vertices)):
                if vertices[v][2] != 0:
                    relevant=True
                    break
            if not relevant:
                continue
            for v in range(len(vertices)):
                sv=vertices[v][0]
                next_v=v+1
                if next_v==4:
                    next_v=0
                ev=vertices[next_v][0]
                if vertices[next_v][2]==0:
                    slab=vertices[v][1]
                    elab=vertices[next_v][1]
                    target_edge = slab[0] + elab[0]
                    source_edge = slab[-1] + elab[1]
                    labels=makelabels(vertices)
                    hk=make_hk(source_edge,target_edge)
                    hk+=","+labels
                    if IF_hash.has_key(hk):
                        print config[0],"region",region_id, "might overlap with",IF_hash[hk]
                        print sv,ev,source_edge,target_edge,hk
        prev_group=this_group

def makelabels(vertices):
  # make a standard label for the region given by vertices
  # concatenation of vertex labels beginning in order x..,b..,Y.. and A..
  # changing case throughout if necessary
  labels=""
  starti=0
  makelower=False
  decrement=False 
  for i in range(4):
    if vertices[i][1][0]=='x':
      startx=i
      next_i=(i+1)%4
      if vertices[next_i][1][0]=='A':
        decrement=True
      break
    elif vertices[i][1][0]=='X':
      startx=i
      makelower=True
      next_i=(i+1)%4
      if vertices[next_i][1][0]=='a':
        decrement=True
      break

  for i in range(4):
    if decrement:
      j=(startx-i)%4
    else:
      j=(starti+i)%4
    lab=vertices[j][1]
    for k in range(len(lab)):
      if not lab[k].isalpha():
        continue
      if makelower:
        if lab[k].isupper():
          labels+=lab[k].lower()
        else:
          if lab[k]=='l':
            labels+='m'
          elif lab[k]=='m':
            labels+='l'
          else:
            labels+=lab[k].upper()
      
  return labels

def calc_curvature(config,tracex):
    curv=0
    charges=0
    factor=0
    plus_curv=0
    if config[0].endswith('*'):
        factor=0.5
    elif config[0].endswith('@@'):
        plus_curv=32.0/7
    elif config[0].endswith('@'):
        plus_curv=18.0/7
    elif config[0].endswith('++'):
        plus_curv=4
    elif config[0].endswith('+\''):
        plus_curv=3
    elif config[0].endswith('+'):
        plus_curv=2

    regions = config[1:]
    target=-1
    for region in regions:
        ignore = True
        deg_charge=0
        for vertices in region:
            deg=get_degree(vertices[1])
            charge=int(vertices[2])
            if charge<>0:
                ignore = False
            if charge < 0:
                charge=0
                
            if charge>1000:
                charge=(charge/1000 * 30) / (1.0 * charge%1000)
            if tracex:    
                print deg,
            deg_charge+=2.0/deg
            charges+=charge
        if not ignore:
            curv+=2-len(region) + deg_charge
        if target<0:
            target=(curv*30) * factor
        if tracex:
            print curv,deg_charge,target,plus_curv
    #targeti=int(target)
        if curv<0.00000001 and curv > -0.0000001:
            curv=0
    curv= curv*30 + plus_curv
    return curv,charges*1.0,target

    # update config with existing edge sv, ev traversed in opp direction
def expand_config(configs):
    for config in configs:
        regions = config[1:]
        history=[]
        
        for vertices in regions:
            # check if we are retracing an edge.
            # if so, recalculate vertex label
            # and overwrite
            v=0
            for v in range(len(vertices)):
                sv=vertices[v][0]
                next_v=v+1
                if next_v==4:
                    next_v=0
                ev=vertices[next_v][0]
                # go through edges recorded in history
                for hvertices in history:
                    h=0
                    for h in range(len(hvertices)):
                        hsv=hvertices[h][0]
                        next_h=h+1
                        if next_h==4:
                            next_h=0
                        hev=hvertices[next_h][0]
                        if hsv==ev and hev == sv:
                            # reversing an edge - expand vertex label
                            oldl=hvertices[next_h][1]
                            newl=oldl[1:]+oldl[0]
                            vertices[v][1]=newl
                            #make any charge across interior edges -1
                            #to indicate that the region is to be used
                            #in the calculation of curvature
                            oldl=hvertices[h][1]
                            newl=oldl[-1]+oldl[:-1]
                            vertices[next_v][1]=newl

                            if hvertices[next_h][2] > 0:
                                #interface to a 4gon
                                source_edge=hvertices[h][1][0]+hvertices[next_h][1][0]
                                target_edge=vertices[next_v][1][0]+vertices[v][1][0]
                                labels=makelabels(vertices)
                                if len(labels)>0:
                                  make_4IF_entry(config[0],source_edge,target_edge,labels)
                                vertices[next_v][2]=-1
                                hvertices[next_h][2]=-1

                              
            
            history.append(vertices)        
            if config[0]=='4.23xi':
                # indicate that delta3 has degree 4
                vertices[3][2]=-1
            if config[0]=='4.23xii':
                # indicate that delta4 has degree 4
                vertices[0][2]=-1
                
def get_degree(vs):
    deg=0
    i=0
    if len(vs) == 2 and vs[1]=='.':
        # assume this represents deg >= 4
        return 4
        
    for i in range(len(vs)):
        if vs[i].isdigit():  # num of extra edges => num+1 more letters
            deg+=int(vs[i])+1
        elif vs[i].isalpha():
            deg+=1
    return deg

def swap_case(val1):
    val1x=val1
    if val1.isupper():
        val1=val1.lower()
    else:
        val1=val1.upper()
    if val1x=='l':
        val1='m'
    if val1x=='m':
        val1='l'
    return val1

def update_charge_hash(edge,sdeg,edeg,charge,orig_s,orig_e,fig,square):
    # filter out multi edge charges - these can be defined in a script??
    multi_edge_figs=["4.8","4.9","4.27","4.28","4.29","4.30","5.3","5.4"]
    ignore=False
    if len(fig)>2:
        if fig[:3] in multi_edge_figs:
            ignore=True
    if len(fig)>3:
        if fig[:4] in multi_edge_figs:
            ignore=True
    if ignore:
        return
    hk1=edge[0]
    hk2=edge[1]
    val1=[]
    if hk1.lower() > hk2.lower():
        (hk1,hk2) = (hk2,hk1)
        val1=[edeg,sdeg,charge,orig_e,orig_s,fig,square]
    else:
        val1=[sdeg,edeg,charge,orig_s,orig_e,fig,square]

    if hk1.isupper() or hk1=='m':
        #need to swap orig labels case!!
        val1[3]=swap_case(val1[3])
        val1[4]=swap_case(val1[4])
    # prepare the hask key
    hk=make_charge_hk(hk1,hk2)
    if charge_hash.has_key(hk):
        vals=charge_hash[hk]
        if not val1 in vals:
            vals.append(val1)
            charge_hash[hk]=vals
    else:
        charge_hash[hk]=[val1]


def make_charge_hash(configs):
    cc=-1
    for config in configs:
        cc+=1
        regions = config[1:]
        vv=-1
        for vertices in regions:
            # if and edge has a charge record this and the vertex degrees
            #  store in charge_hash using edge labels as key
            vv+=1
            for v in range(4):
                charge=vertices[v][2]
                if charge <= 0:
                    continue
                if (config[0]=="4.30i") or (config[0] == "4.30iii"):
                    #funny one!!
                    if charge==6:
                        continue

                elab=vertices[v][1]
                orig_e=elab[0]
                prev_v=(v-1) % 4
                slab=vertices[prev_v][1]
                orig_s=slab[0]
                hk1=slab[-1]
                hk2=elab[1]
                #print hk1
                if not (hk1.isalpha() or hk2.isalpha()):
                    continue
                if (hk1=='=') or (hk2=='='):
                    continue
                sdeg = get_degree(slab)
                if '.' in slab:
                    sdeg*=-1
                edeg = get_degree(elab)
                if '.' in elab:
                    edeg*=-1
                todo_keys=[]
                if not hk1.isalpha():
                    #need to find the 3 possible pre letters to slab[0] and
                    # generate separate keys with hk2
                    for rule in post_pre_rules:
                        if slab[0]==rule[0]:
                            for i in range(len(rule[2])):
                                todo_keys.append([rule[2][i],hk2])
                            break    
                elif not hk2.isalpha():
                    #need to find the 3 possible post letters to elab[0] and
                    # generate separate keys with hk1
                    for rule in post_pre_rules:
                        if elab[0]==rule[0]:
                            for i in range(len(rule[1])):
                                todo_keys.append([hk1,rule[1][i]])
                            break
                else:
                    todo_keys.append([hk1,hk2])
                square=[cc,vv]
                for todo_key in todo_keys:
                    update_charge_hash(todo_key,sdeg,edeg,charge,
                                       orig_s,orig_e,config[0],square)

                    

def make_charge_hk(hk1,hk2):
    if hk1.lower() > hk2.lower():
        (hk1,hk2) = (hk2,hk1)
    if hk1.isupper() or hk1=='m':
        hk1=swap_case(hk1)
        hk2=swap_case(hk2)
    return hk1+hk2

def get_vertex_charges(degv1,degv2):
    results=[]
    keys= charge_hash.keys()
    prev_value=[0,0,0]
    for hk in keys:
        values=charge_hash[hk]
        for value in values:
            d1=abs(value[0])
            d2=abs(value[1])
            if (((d1 >= degv1) and (d2 >= degv2) or (d1 >= degv2) and (d2 >= degv1))):
                if value[:3] !=prev_value:
                    results.append([hk, value[0],value[1],value[2]])
                prev_value=value[:3]
    return results
        
 

def get_edge_charges(edge):
    hk=make_charge_hk(edge[0],edge[1])
    if not charge_hash.has_key(hk):
        return 
    vals=charge_hash[hk]
    print vals
    

    
def get_2_highest(hk1,hk2,lim):
    
    hk=make_charge_hk(hk1,hk2)
    top2=[0,0]
    if not charge_hash.has_key(hk):
        return top2
    vals=charge_hash[hk]
    for val in vals:
        charge = val[2]
        if charge >= lim:
            continue
        if top2[0]==0:
            top2[0]=charge
            top2[1]=charge
        elif charge >= top2[0]:
            top2[0] = charge
        elif charge > top2[1]:
            top2[1]=charge
    return top2

