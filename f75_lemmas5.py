from f75_processes import *
from f75_hexagons  import *

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
    print "See Figure 5.7"
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
