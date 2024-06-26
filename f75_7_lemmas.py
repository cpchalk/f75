from f75_processes import *
ba_59_table={'aba':11,'mba':13,'aba':12}
def prove7_3 ():
  #circuits=['xbYXayBA','zbYXYAlx','ZAxyxbmY']
  circuits=['xbYXayBA']
  # d(u3), d(u4) is 3
#  patterns=[[0,0,3,3,0,0,0,0,0],[3,3,3,3,3,3,3,3,3],[4,3,3,3,3,3,3,3,4],
#            [3,4,3,3,3,3,3,3,3]]
  initial_pattern=[0,0,0,0,0,0,0,0,0]
  pattern=[0,0,3,3,0,0,0,0,0]
  initial=True
  for cc in circuits:
    print cc+'...'
    (dd,charges) = display_charges_for_pattern(cc,initial_pattern,True)
    print dd
    print charges
    max4=(charges - 20)/6
    print 'max number of 4 vertices for positive charge = ',(charges - 20)/6
    i=0
    while i < max4:
      patterns=make_patterns(pattern,i)
      for patt in patterns:
        #print patt
        (dd,charges) = display_charges_for_pattern(cc,patt,False)
        print dd
        print charges
      i+=1


def make_patterns(pattern,no_4_vertices):
    # make them all 3
    patternx=[ 3 for i in range(len(pattern))]
    return [patternx]

def display_charges_for_pattern(cc,pattern,initial):
      print pattern
      retd=""
      charges=0
      disp=print_highest_charges(cc+cc[0],pattern,initial)
      ll=len(disp)
      skip=False
      for  i in range(1,ll):
        if skip:
          skip=False
          continue
        dd=disp[i]
#        print dd
        next_i=(i+1) % ll
        
        if initial and disp[next_i][4].lower() == 'ba':
          skip=True
          ba_key=dd[4]+disp[next_i][4][1]
          
          if ba_59_table.has_key(ba_key):
             valx= ba_59_table[ba_key]
             retd+= '0 ' + str(valx)
             charges+=valx
             
          else:
             retd+=' 5 6'
             charges+=11
        else:
          retd+=' '+str(dd[3])
          charges+=dd[3]
      return retd,charges
      
def print_highest_charges(edges,pattern,initial):
    display_if_pos=[]
    edges=edges.strip()
    display_if_pos.append(edges)
    circuit=edges[0]==edges[-1]
    shape_charges=[-20,-30,-40,-50]
    k=len(edges)-1
    total_c=60-10*k
    deg1=[0,0]
    first_deg=-1
    for i in range(k):
        if initial:
          deg1=[0,0]  # dont chain
        next_i=(i+1)
        degx1=[pattern[i],pattern[i+1]]
        e0=edges[i]
        e1=edges[i+1]
        new_link=e1
        swap=False
        if i==k-1:
             deg1[1]=display_if_pos[1][0]
             #print "**",deg1

        if e0.lower() > e1.lower():
            (e0,e1)=(e1,e0)
            new_link=e0
            deg1=[deg1[1],deg1[0]]
            degx1=[degx1[1],degx1[0]]
            #print "!",degx1,e0+e1
            swap=True
        if e0.isupper() or e0=='m':
            e0=swap_case(e0)
            e1=swap_case(e1)
            new_link=swap_case(new_link)
        use_all_deg=False
        if len(display_if_pos) > 1:
            if display_if_pos[-1][1]==0:
                use_all_deg=True
        (hh,hc)=print_highest_charge(e0+e1,degx1,use_all_deg)
        if len(hh)==0:
            hh=degx1+[0]
            hc=0
        total_c+=hc
        item=[]
        if swap:
            item+=[hh[1],hh[0], hh[2]]
            if first_deg<0:
                first_deg=hh[1]
            deg1=[hh[0],0]
        else:
            item+=[hh[0],hh[1], hh[2]]
            if first_deg<0:
                first_deg=hh[0]

            deg1=[hh[1],0]
        item+=[hc,edges[i]+edges[i+1]]
        display_if_pos.append(item)

#        print "next degree has to be",deg1[0]
#    if total_c>0:
   # if True:      
   #     for dd in display_if_pos:
   #         print dd
   #     print total_c
    return display_if_pos
