from f75_processes import *
from f75_hexagons  import *
def do510():
    #external f1list
    # 10i filter
    part="5.10i"
    filterx=[3,4,'Y', 'b' ,'ab']
    filterx_next1=[0,4,'?', 'y' ,'?b']
    filterx_next2=[4,0,'y', '?' ,'b?']
    do510part(part,filterx,filterx_next1,filterx_next2)
    part="5.10vii"
    filterx=[3,4,'x', 'b' ,'ab']
    filterx_next1=[0,4,'?', 'X' ,'?b']
    filterx_next2=[4,0,'X', '?' ,'b?']
    do510part(part,filterx,filterx_next1,filterx_next2)

def do510part(part,filterx,filterx_next1,filterx_next2):
    resx=print_charge_hash(filterx,False)
    res8=[]
    res7=[]
    for resxx in resx:
        if resxx[2]==8:
            res8.append(resxx)
        if resxx[2]==7:
            res7.append(resxx)
    print part,"8 charges"
    for res8x in res8:
        print res8x,get_neighbour(res8x[5])
    print part,"7 charges"
    for res7x in res7:
        print res7x,get_neighbour(res7x[5])
    res_next = []
    resx=print_charge_hash(filterx_next1,False)
    for resxx in resx:
        if resxx[2]>=3:
            res_next.append(resxx)
    resx=print_charge_hash(filterx_next2,False)
    for resxx in resx:
        if resxx[2]>=3: 
            res_next.append(resxx)
    print part," next charges"
    for res3x in res_next:
        qual = get_neighbour(res3x[5]) # 1st neighbour [2nd neighbour] [vertex]
        if qual.endswith(')'):   # temporary filter code to prove lemma5.5
            print res3x,get_neighbour(res3x[5])

def prove5_7 (configs):
    print "\n*****\n"
    print "See Figure 5.7"
    filter=[]
    fill_hexagon_store(filter)
    hex_to_process = []
    for poss_6_gon in hexagon_store:
        if len(poss_6_gon[2])==4 and len(poss_6_gon[0])==4:
            hex_to_process.append(poss_6_gon)
    print "Delta has degree 4, so Delta4 cant be 4.07xi, 4.09ii, 4.23xii"
    print " 3rd edge of Delta2^ cant interface with 4.27,4.28 "
    print "Delta4 cant be 4.01v or 4.03v since they cause contradiction that"
    print "Delta1 is a 4.27i/4.28i hexagon only"
    filterx=["4.28","4.27","4.29","4.07","4.09","4.23","4.08"]
    #"4.02","4.03"] ????
    override_charges=[9,9,9,5,9,9]
    print ""
    print "****"
    print "Calculate highest possible curvature of Delta2^"
    print "****"
    filter_hexagons(hex_to_process,filterx,-1,override_charges)

def prove5_6 (configs):
    print "\n*****\n"
    print "See Figure 5.6"
    print " identify possible delta6^ " 
    sd1=['bx','X','a',['a','y'],['b','x'],'(i)']
    sd2=['bY','y','a',['a','x'],['b','y'],'(ii)']
    search_data=[sd1,sd2]
    candidates=[]
    for sd in search_data:
        results=get_vertex_edge_charges(4,3,sd[0])
        for resx in results:
            target=[4,3,2] + sd[1:3]
            if resx[:5]==target:
                if resx[5].startswith("4."):
                    cc=resx[6][0]
                    vv=resx[6][1]+1
                    square=configs[cc][vv]
                    ignore=False
                    for v in square:
                        if v[2]==-1:
                            v_let=v[1][0].lower()
                            if v_let in sd[3]:
                                print "ignoring",resx[5],"in ", sd[-1],"since delta5^ >4"
                                ignore=True
                                #implies delta5 has deg=4, not possible
                                break
                    if ignore:
                        continue
                    candidates.append([sd[-1],resx[5],sd[4],square])
    rcharge=0
    if len(candidates)>0:
        gt4=False
        print "candidates for delta6^ are"
        for cc in candidates:
            print cc[0],cc[1]
            sq=cc[-1]
            for v in sq:
                if v[2] > 0:
                    if v[1][0] in cc[2]:
                        print "deg delta^^ is > 4 since it receives a charge"
                        rcharge+=1
                        break
    if rcharge == len(candidates) and rcharge>0:
        print "Since delta^^ has deg > 4 in all cases,"
        print " edge 5 of delta1^ receives no charge"
    print "vertex w4 has deg > 3 since no 3 vertex starts Yx"
    #get everything and filter those match above
    filter=[]
    fill_hexagon_store(filter)
    hex_to_process = []
    for poss_6_gon in hexagon_store:
        if len(poss_6_gon[2])>=4 and len(poss_6_gon[0])==4:
            hex_to_process.append(poss_6_gon)
    print "filter out contribution of 4.28, 4.27 to edge 3"
    filterx=["4.28","4.27","5.3","5.4"]
    override_charges=[9,9,9,9,9,0] # make 5th edge have charge 0
    print ""
    print "****"
    print "Calculate highest possible curvature of Delta1^"
    print "****"
    filter_hexagons(hex_to_process,filterx,-1,override_charges)
def show_hex_fig():
    filter=["4.27","4.28","4.29","5."]
    no_override=[9,9,9,9,9,9]
    fill_hexagon_store(filter)
    filter_hexagons(hexagon_store,filter,0,no_override)

def show_hex_figAB():
    filter=["5."]
    fill_hexagon_store(filter)

    known1=["mzb","YxBB","AyX"]
    known2=["ZlB","Xybb","axY"]
    hex_to_process = []
    for poss_6_gon in hexagon_store:
        if poss_6_gon[1:4]==known1:
            hex_to_process.append(poss_6_gon)
        if poss_6_gon[1:4]==known2:
            hex_to_process.append(poss_6_gon)
    filter=["4.27xb","4.28yB","5."]
    no_override=[9,9,9,9,9,9]
    filter_hexagons(hex_to_process,filter,1,no_override)

def show_hex_figCD():
    filter=["5."]
    fill_hexagon_store(filter)

    known1=["AyX","lBZ","xYa","bXyb"]
    known2=["axY","zbm","yXA","BYxB"]
    hex_to_process = []
    for poss_6_gon in hexagon_store:
        if (poss_6_gon[3:]==known1[:3]) and (poss_6_gon[0]==known1[-1]):
            hex_to_process.append(poss_6_gon)
        if (poss_6_gon[3:]==known2[:3]) and (poss_6_gon[0]==known2[-1]):
            hex_to_process.append(poss_6_gon)
    filter=["4.27xb","4.28yB","4.07xb","4.07yB",
            "4.08xb","4.09yB","4.23yB","5."]
    no_override=[9,9,9,9,9,9]
    filter_hexagons(hex_to_process,filter,2,no_override)
