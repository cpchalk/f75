from f75_processes import *
hexagon_store=["blah","blah"]

        
def clear_hexagon_store ():
    while len(hexagon_store)>0:
        hexagon_store.pop()
def hex_get_results(required_degs,required_edges,filter):
    clear_hexagon_store()
    results1=[[[]for i in range(len(required_degs))] for j in range(len(required_edges))]
    for j in range(6):
        results=get_vertex_edge_charges(3,3,required_edges[j])
        for i in range(13):
            d1=required_degs[i][0]
            d2=required_degs[i][1]
            max=0
            for result in results:
                if len(result[5])>3:
                    if result[5][:4] in filter:
                        continue
                    if result[5].startswith("4.07xii"):
                        continue
                    if result[5][:2] in filter:
                        continue
                    
                r0=result[0]
                r1=result[1]
                c=result[2]
                if r0<0:
                    r0*=-1
                if r1<0:
                    r1*=-1
                if c>1000:
                    c=0

                hit=False
                if (result[:2]==required_degs[i]):
                    hit=True
                elif d1<0 and d2>0:
                    if ((r0>=(d1*-1)) and (d2==r1)):
                        hit=True
                elif d1<0 and d2>0:
                    if ((r1>=(d2*-1)) and (d1==r0)):
                        hit=True
                elif d1<0 and d2<0:
                    if ((r1>=(d2*-1)) and ((r0>=(d1*-1)))):
                        hit=True
                    
                if hit:
                    if c>max:
                        max=c
            results1[j][i]=max
    return results1

required_degs=[[3,3],[3,4],[4,3],[3,5],[5,3],[3,-6],
                   [-6,3],[4,4],[4,5],[5,4],[4,-6],[-6,4],[-5,-5]]
v_chain=[[],[],[],[0,1,3,5],[2,7,8,10],[4,9,12],[6,11,12]]
required_edges1 = ["bm","mY","YA","Al","lx","xb"]
required_edges2 = ["BZ","ZX","Xa","az","zy","yB"]
required_edgesAB1 = ["Al","lx","xb"]
required_edgesAB2 = ["bY","YZ","ZA"]
required_edgesCD1 = ["yl"]
required_edgesCD2 = ["ZX"]

diff=[0,0,0,0,5,8,10]
def fill_hexagon_store (filter):
    results1=hex_get_results(required_degs,required_edges1,filter)
    results2=hex_get_results(required_degs,required_edges2,filter)
    maxc=[0,[]]
    c=[0,0]
    j=0

    for i in range(len(required_degs)):
        hist=[]
        start=required_degs[i][0]
        maxc=navigate_paths(hist,start,i,j,c,results1,results2,maxc)
        
def update_charge_table (hexagon,distr,fig,):
    for i in range(len(distr)):
        if distr[i].isdigit():
            next_i = (i+1) % 6
            edge=hexagon[i][0]+hexagon[next_i][0]
            key1=hexagon[i][-1]
            key2=hexagon[next_i][1]
            v1=len(hexagon[i])
            v2=len(hexagon[next_i])
            charge=int(distr[i])
            update_charge_hash(key1+key2,v1,v2,
                               charge,edge[0],edge[1], fig,[])
#            print key1+key2,v1,v2,charge,edge[0],edge[1], fig
        
def filter_hexagons(hex_list,filterx,type,override_charges):
    print ""
    if type>=0:
        print "charge,curvature,c(i,j),vertex labels,figure,charge distribution"
    else:
        print "charge,curvature,c(i,j),vertex labels"
        
    distr=""
    for poss_6gon in hex_list:
        (distr,fig)=process_6gon (poss_6gon,filterx,type,override_charges)
        if (distr != "") and (fig != ""):
            update_charge_table(poss_6gon,distr,fig)
       
  
def show_p21_table():
    filter=["4.27","4.28","4.29"]

    results1=hex_get_results(required_degs,required_edges1,filter)
    results2=hex_get_results(required_degs,required_edges2,filter)
    print "          ",
    for i in range(len(required_edges1)):
        print " ",required_edges1[i]+"/"+required_edges2[i],
    print ""
    for i in range(len(required_degs)):
        qual1="  "
        qual2="  "
        r1=required_degs[i][0]
        r2=required_degs[i][1]
        if r1<0:
            r1*=-1
            qual1=">="
        if r2<0:
            r2*=-1
            qual2=">="

        print qual1+str(r1),qual2+str(r2)+"   ",
        for j in range(len(required_edges1)):
            print str(results1[j][i])+"/"+str(results2[j][i])+"     ",
        print ""

def get_max_charge(deg1,deg2,inner_edge,outer_edge,filterx):
    results=get_vertex_edge_charges(deg1,deg2,inner_edge)
    maxc=0
    for resx in results:
        #print resx[5],filterx
        if len(resx[5])>3:
            if resx[5][:4] in filterx:
                continue
            if (resx[5][:4]+inner_edge) in filterx:
                continue
            if resx[5].startswith("4.07xii"):
                continue
            if resx[5][:2] in filterx:
                continue
            if resx[5][:3] in filterx:
                continue
        #print resx[5],"passed"
        if (deg1,deg2,outer_edge[0],outer_edge[1]) == (resx[0],resx[1],resx[3],resx[4]):
            #print "found!!"
            c=resx[2]
            if c>1000:
                #ignore!!
                c=0
            if c>maxc:
                maxc=c
    return maxc
def get_cld(poss_6gon,charges,type):
    #get charge breakdown and any labels and (re)distribution breakdonwn
    patterns0 = [[1,3],[1,2],[6],[5],[3],[2],['b'],['X'],['B'],['Y'],[]]
    labels0 =['i','ii','iii','iv','v','vi','vii','viii','vii','viii','ix']
    dist0=['1','.....3','.1','.2','4','..1','.1','.21','.1','.21','321']
    patterns1 = [[3,5],[3],['X','x'],['Y','y']]
    labels1 =['ii','iii','iv','iv']
    dist1=['1','5','2','2']
    patterns2 = [['X'],["Y"],['X','x'],["Y","y"]]
    labels2 =['iii','iv','v','vi']
    dist2=['..2','..2','1','1']

    figs=[['5.1','5.2'],['5.3','5.4'],['5.5','5.5']]
    hex_types =[[patterns0,labels0,dist0],[patterns1,labels1,dist1],
                [patterns2,labels2,dist2]]
    patterns=hex_types[type][0]
    labels=hex_types[type][1]
    dist=hex_types[type][2]
    #(chargesx,lab,dist)=get_cld(poss_6gon)
    pat1=[]
    pat2=[]
    lab=""
    if poss_6gon[0][0]=='b':
        lab=figs[type][0]
    else:
        lab=figs[type][1]
    chargesx=""
    for i in range(6):
        if len(poss_6gon[i])==4:
            pat1.append(i+1)
            pat2.append(poss_6gon[i][1])
        cc=(i+1)%6
        if charges[cc]>0:
            chargesx+=str(charges[cc])
        else:
            chargesx+='.'
    distx="......  "
    distxx=""
    if pat1 in patterns:
        lab+=labels[patterns.index(pat1)]
        distxx=dist[patterns.index(pat1)]
    elif pat2 in patterns:
        lab+=labels[patterns.index(pat2)]
        distxx=dist[patterns.index(pat2)]

    return chargesx,lab,distxx+distx[len(distxx):]

  
def process_6gon (poss_6gon,filterx,typex,override_charges):
    # evaluate if 6gon has positive curvature allowing for
    # max possible  charges received
    #print poss_6gon
    distr=""
    lab=""
    charge=0
    neg_curv=0
    charges=[[0] for i in range(6)]
    for i in range(6):
        previ=(i-1)%6
        slab=poss_6gon[previ]
        elab=poss_6gon[i]
        deg1=len(slab)
        deg2=len(elab)
        inner_edge=slab[0] + elab[0]
        outer_edge=slab[-1]+elab[1]
        charges[i]=get_max_charge(deg1,deg2,inner_edge,outer_edge,filterx)
        charge+=charges[i]
        neg_curv+=diff[deg2]
    if (charge>neg_curv):
        # display if positive curvature
        typexx=typex
        if typex==-1:
            typexx=0
        (chargesx,lab,distr)=get_cld(poss_6gon,charges,typexx)
        chargesxx=""
        for c in range(6):
            if override_charges[c] == 9:
                chargesxx+=chargesx[c]
            else:
                newc=override_charges[c]
                chx=str(newc)
                if newc==0:
                    chx='.'
                chargesxx+=chx
                oldc=0
                if chargesx[c].isdigit():
                    oldc = int(chargesx[c])
                    charge-=(oldc-newc)
                else:
                    charge+=newc
        print charge,neg_curv,'\t',
        print chargesxx,poss_6gon,
#        print pat1,pat2
        if typex >= 0:
            print lab,distr
        else:
            print ""
            return "",""
    return distr,lab
            

def process_possible_6gons (required_edges,hist):
            poss_6gon=[]
            for k in range(6):
                poss_6gon.append(get_v_label(required_edges[k][0],hist[k][0]))
            poss1_6gon=[]
            poss2_6gon=[]
            for vv in poss_6gon:
                if len(vv)==1:
                    poss1_6gon.append(vv[0])
                    poss2_6gon.append(vv[0])
                elif len(vv)==2:
                    #only expect one of these
                    poss1_6gon.append(vv[0])
                    poss2_6gon.append(vv[1])
            if poss1_6gon==poss2_6gon:
                hexagon_store.append(poss1_6gon)
            else:
                hexagon_store.append(poss1_6gon)
                hexagon_store.append(poss2_6gon)

         
    
def navigate_paths(hist,start,i,j,c,results1,results2,maxc):
    charge=max(results1[j][i],results2[j][i])
    curv=diff[abs(required_degs[i][0])]
    c[0]+=charge
    c[1]+=curv
    hist.append([required_degs[i][0],charge,c])
    if j==5:
        if c[1]<c[0]:
            process_possible_6gons(required_edges1,hist)
            process_possible_6gons(required_edges2,hist)
    
    # curvature is positive if 2 * Sigma (1/3-1/d(v)) < c
    if c>=maxc[0]:
        maxhist=[]
        for h in hist:
            maxhist.append(h)
        maxc=[c,maxhist]
    if j < 5:
        j+=1
        next=v_chain[required_degs[i][1]]
        for i in next:
            if j==5:
                if required_degs[i][1] != start:
                    continue
            maxc= navigate_paths(hist,start,i,j,c,results1,results2,maxc)
    hist.pop()
    c[0]-=charge
    c[1]-=curv
    
    return maxc   

