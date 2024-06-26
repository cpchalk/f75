from f75_processes import *
from f75_hexagons import *
octagon_store=["blah","blah"]

required_degs=[[3,3],[3,4],[4,3],[3,5],[5,3],[3,-6],
                   [-6,3],[4,4],[4,5],[5,4],[4,-6],[-6,4],[-5,-5]]
v_chain=[[],[],[],[0,1,3,5],[2,7,8,10],[4,9,12],[6,11,12]]
#required_edges1 = ["bY","YX","XY","YA","Al","lx","xz","zb"]
required_edges1=[]
#diff=[0,0,0,0,5,8,10]
diff6=[0,0,0,0,5,8,10]
# 2 * how many 1/30's a 1/4, 1/5 and 1/6 differ from 1/3 (10/30)
diff8=[0,0,0,10,30,42,50]
# 2 * how many 1/120's a 1/3, 1/4, 1/5 and 1/6 differ from 3/8 (45/120)
diff9=[0,0,0,160,190,208,220]
# 2 * how many 1/180's a 1/3, 1/4, 1/5 and 1/6 differ from 7/9 (140/180)

units=[0,1,2,3,4,5,[1,diff6],7,[4,diff8],[6,diff9]]
tolerance=0
def get_max_charge2(deg1,deg2,inner_edge,outer_edge,filterx,prev):
    results=get_vertex_edge_charges(deg1,deg2,inner_edge)
    maxc=[0,""]
    for resx in results:
        #print resx[5],filterx
        if len(resx[5])>3:
            if resx[5][:4] in filterx:
                continue
            if (resx[5][:4]+inner_edge) in filterx:
                continue
            if resx[5].startswith("4.06"):
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
            if c>maxc[0]:
                if not ((c==10) and (prev==10)):
                    maxc=[c,resx[5]+inner_edge]
    return maxc

def process_possible_8gons (required_edges,hist,filterx):
            #hist contains list of vertex degrees corresponding
            #to the required edges
            poss_8gon=[]
            for k in range(len(required_edges)):
                v_label=get_v_label(required_edges[k][0],hist[k][0])
                poss_8gon.append(v_label)
            # need to expand 8 gons when there are > 1 labels for vertex
            if len(poss_8gon) <  8:
                #bug!!
                print poss_8gon
                return
            poss1_8gon=[]
            poss2_8gon=[]
            for vv in poss_8gon:
                if len(vv)==1:
                    poss1_8gon.append(vv[0])
                    poss2_8gon.append(vv[0])
                elif len(vv)==2:
                    #only expect one of these
                    poss1_8gon.append(vv[0])
                    poss2_8gon.append(vv[1])
            if poss1_8gon==poss2_8gon:
                if len(poss1_8gon)==len(required_edges):
                    if process_8gon (poss1_8gon,filterx,-1,False,0):
                        octagon_store.append(poss1_8gon)
            else:
                if len(poss1_8gon)==len(required_edges):
                    if process_8gon (poss1_8gon,filterx,-1,False,0):
                        octagon_store.append(poss1_8gon)
                    if process_8gon (poss2_8gon,filterx,-1,False,0):
                        octagon_store.append(poss2_8gon)

def oct_get_results(required_degs,required_edges,filterx):
    clear_octagon_store()
    results1=[[[]for i in range(len(required_degs))] for j in range(len(required_edges))]
    for j in range(len(required_edges)):
        results=get_vertex_edge_charges(3,3,required_edges[j])
        for i in range(13):
            d1=required_degs[i][0]
            d2=required_degs[i][1]
            max=0
            for result in results:
                if len(result[5])>3:
                    if result[5][:4] in filterx:
                        continue
                    if result[5][:2] in filterx:
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
def process_8gon (poss_8gon,filterx,typex,printit,tolerance):
    # evaluate if 8gon has positive curvature allowing for
    # max possible  charges received
    #print poss_8gon
    distr=""
    lab=""
    charge=0
    neg_curv=0
    charges=[[0] for i in range(len(poss_8gon))]
    units_to_use=units[len(poss_8gon)]
    cf=units_to_use[0]
    diff=units_to_use[1]
    prev=0
    for i in range(len(poss_8gon)):
        modv=len(poss_8gon)
        previ=(i-1)%modv
        slab=poss_8gon[previ]
        elab=poss_8gon[i]
        deg1=len(slab)
        deg2=len(elab)
        inner_edge=slab[0] + elab[0]
        outer_edge=slab[-1]+elab[1]
        charges[i]=get_max_charge2(deg1,deg2,inner_edge,outer_edge,filterx,prev)
        prev=charges[i][0]
        charge+=(charges[i][0]*cf)
        neg_curv+=diff[deg2]
    if (charge>neg_curv-tolerance):
        # display if positive curvature
        typexx=typex
        if typex==-1:
            typexx=0
        chargesx=[]
        for cc in charges:
            if cc[0]==0:
                chargesx.append(',')
            else:
                chargesx.append(cc)
        if printit:       
            print charge,neg_curv,'\t',poss_8gon
            print chargesx
        return True
    return False
         

def filter_octagons(oct_list,filterx,type,override_charges,tolerance):
    print ""
    if type>=0:
        print "charge,curvature,c(i,j),vertex labels,figure,charge distribution"
    else:
        print "charge,curvature,vertex labels"
        
    distr=""
    i=0
    for poss_8gon in oct_list:
        i+=1
        print i
        process_8gon (poss_8gon,filterx,type,True,tolerance)
        
def clear_octagon_store ():
    while len(octagon_store)>0:
        octagon_store.pop()
        
def oct_navigate_paths(hist,start,i,j,c,results1,maxc,required_edges1,filterx):
    charge=results1[j][i]
    limit=len(required_edges1)-1
    #print charge
    units_to_use=units[len(required_edges1)]
    cf=units_to_use[0]
    diff=units_to_use[1]

    curv=diff[abs(required_degs[i][0])]
    c[0]+=(charge*cf)
    c[1]+=curv
    hist.append([required_degs[i][0],charge,c])
    if j==limit:
        if c[1]< c[0]+tolerance:
            process_possible_8gons(required_edges1,hist,filterx)
    
    # curvature is positive if 2 * Sigma (1/3-1/d(v)) < c
    if c>=maxc[0]:
        maxhist=[]
        for h in hist:
            maxhist.append(h)
        maxc=[c,maxhist]
    if j < limit:
        j+=1
        next=v_chain[required_degs[i][1]]
        for i in next:
            if j==limit:
                if required_degs[i][1] != start:
                    continue
            maxc= oct_navigate_paths(hist,start,i,j,c,results1,maxc,required_edges1,filterx)
    hist.pop()
    c[0]-=charge
    c[1]-=curv
    
    return maxc   

def fill_octagon_store (filterx,required_edges1):
    results1=oct_get_results(required_degs,required_edges1,filterx)
    maxc=[0,[]]
    c=[0,0]
    j=0
    depth=len(required_edges1)
    for i in range(len(required_degs)):
        hist=[]
        start=required_degs[i][0]
        maxc=oct_navigate_paths(hist,start,i,j,c,results1,maxc,required_edges1,filterx)

def prove6_3 ():
    print "c* <= 0 for A regions??"
    reqes=["lllBAlll","llBXmmay","lxzbmYZA","lxbabYZA",
           "AxzbmYAB","AxbabYAB","AxbmayBZ","bYXayBAx",
           "azzyBZZX","bYXYAlxz","AxyxbmYZ",  "lllBAllll"]
    reqes=reqes[3:4]
    for reqe in reqes:
        re=[]
        ll=len(reqe)
        for i in range(ll):
            next_i = (i+1)% ll
            re.append([reqe[i],reqe[next_i]])
        print "\n*****\n"
        print str(len(reqe))+"-gon",reqe
        filterx=['4.27','4.28','4.29']
        fill_octagon_store(filterx,re)
        print len(octagon_store),"with possible positive curvature"
        if len(octagon_store)>0:
 #           print octagon_store[-1]
            filter_octagons(octagon_store,filterx,-1,re,tolerance)
    prove6_3_explained()

def prove6_3_explained ():
    print "explaining exception..."
    reqes=["lxbabYZA"] # explained by contradiction between 4.11viii and
                       # 4.07xiii (cant be in same 4 vertex)
    
    for reqe in reqes:
        re=[]
        ll=len(reqe)
        for i in range(ll):
            next_i = (i+1)% ll
            re.append([reqe[i],reqe[next_i]])
        print "\n*****\n"
        print reqes
        filterx=['4.27','4.28','4.29']
        fill_octagon_store(filterx,re)
        print len(octagon_store)
        print "exception explained by fact that 4.11 and another 4gon configs cant share", 
        print "the degree 4 vertex. "
        print "with 4.07..4gon with charge of 16/120's(4/30's)"
        filter_octagons(octagon_store,filterx,-1,re,10)
        print "now without 4.07, will reduce charges by at least 8/120's (2/30's)"
        print "(even if the configuration is still invalid!)"
        filterx=['4.27','4.28','4.29','4.07']
        tolerance=1
        filter_octagons(octagon_store,filterx,-1,re,tolerance)
def prove6_1 ():
    print "the curvature of >=10gon is <=-40, so >=-4 per edge."
    print "So need to show that any 3 consecutive edges have  total charge <= 12"
    print "or something??"

          

