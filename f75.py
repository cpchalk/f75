from f75_processes import *
from f75_processes2 import *
from f75_hexagons import *
from f75_5_lemmas import *
from f75_6_lemmas import *
from f75_7_lemmas import *
from f75_shadow import *
from f75_charge import *

# charges come from either a 4-gon with corners xbYA or from a 6-gon
#x3b12345m12Y12Alx
#y3B12345Z12X12azy
# (az) zy has charge 0 in azy
#(am) mX has charge 0 in amX
# (xy) xy? generates 0 charge on y?
# (yx) yx? generates 0 charge on x?
# (ma1)(za1) ay/aX generates charge 1 on may/zaX if a not next to a^5 vertex
# (4m)(4z) the m and Z corners are always degree 3 when bm/mY or BZ/ZX
# outputs a charge.
# (4lx) (4zy) l/z is a 3 vertex when xb/yB of lxb/zyB gives a charge.
# (m4Y)(z4x) y/x is corner of a 3 vertex when YA/Xa in mYA/ZXa has charge > 0 
fname="f75rules.txt"
fname2="f75rules2.txt"
fname3="labeltofig.txt"
trace=0
if trace:
    fname="f75rulesx.txt"
f1=open(fname,'r')
f2=open(fname2,'r')
f3=open(fname3,'r')
make_next_hash(f2)
make_labfig_hash(f3)
configs=[]
f1list=load_file(f1,configs)
expand_config(configs)
make_charge_hash(configs)
print "f75 rules read in from file",fname+',', len(configs),"figures"
#set_up_hexagon_charges(configs)
multi_edge_charges=[]
#charge_logic_script('charge_script0.txt',configs,multi_edge_charges)
#print configs[149]       

def f75_help ():
  print "'Show'commands"
  print "   4.00   -  description of the encoding format of figures 4.1 to 4.32"
  print "   4.nr   -  show figure(s) 4.nr, n= 1 - 32, r= i, ii, .. etc "
  print "'Proof steps' - show (that).. [where c*(..) = charges-curvature of ..]"  
  print "   4.1    -  for all X in 4.1-4.32, c*(X) <=0  including all overlaps"
  print "   5.1    -  6-gons with positive curvature and charge distribution"
  print "   5.2    -  c*(Delta1^) and c*(Delta2^) <=0 in figs 5.6 and 5.7"
  print "   5.8    -  non ab edges with charges 5,6 or 7"
  print "   5.9    -  ab edges with charges >=5"
  print "   5.10   -  what charges can follow 8 or 7 charges (lemma 5.5/fig 5.10)"
  print "   6.1    -  c*(c*('A' region=10) <= 0" 
  print "   6.3    -  c*('A' region<=9) <= 0"
  print "   7.3    -  c*(6.2viii/x/xi) <= 0"
  print " patterns and figures"
  print "   4.33i  -  highest charges for (?,?) edges of fig 4.33i"
  print "   4.33ii -  charges for edges with at least one vertex of degree >=5 "
  print "   p21    -  page 21 table of max charges per hexagon edge label"
  print "   p25    -  page 25 Note 2"
  print "Diagnostics"
  print "   4.nrp  -  show Python list structure of 4.nr above"
  print "   4.nrc  -  calculate curvature of 4.nr above"
  print "   scfgpq -  show charges for pq edges with vertex degrees >=f and >=g"
  print "   pcd [d1 d2 s1 s2 t1t2]   -  print charge dictionary "
  print " [d1/d2 = degrees or 0, s1/s2 = source letters or ?,t1t2 target letters]"  
  print "   quit or q"

def check_curvature ():
  i=1
  all_ok=True
  for config in configs:
      (curv,dist,target)=calc_curvature(config,False)

      if trace or curv-dist>target+0.0001: # or dist - curv > 1.0:
          if curv>0:
              print i,'**',config
              print "!!! curvature=",curv," distribution=",dist
              all_ok=False

      i+=1
  if all_ok:
     print  "all",len(configs),"figures have non-positive curvature after redistribution"
  else:
    "some figures have positive curvature"

def show_config(inpl): 
  e=-1
  while inpl[e].isalpha():
    e-=1
    if len(inpl)+e <= 0:
      return
  q=len(inpl)+e+1
  fig=inpl[:q]
  qual=inpl[q:]
  printing = False
  for xx in f1list:
    #print xx
    if qual != "":
      if printing and xx.startswith(qual):
        print xx,
        break
    if xx.startswith(fig):
        print xx,
        printing=True
    elif printing:
        if xx.startswith('4'):
          break
        if qual=="":
          print xx,
      
  #print fig,qual
def show_config_P(inpl):
  not_found=True
  for config in configs:
    name=config[0]
    if not name[-1].isalpha():
        name=strip_trailing_non_alpha(name)
    if name== inpl:
      not_found=False
      print config
    elif not_found==False:
      return
  if not_found:
    print inpl,"not found"

def show_config_C(inpl):
  not_found=True
  for config in configs:
    name=config[0]
    if not name[-1].isalpha():
        name=strip_trailing_non_alpha(name)
    if name== inpl:
      not_found=False
      (curv,dist,target)=calc_curvature(config,True)
      print  "curvature=",curv," distribution=",dist,
      if target > 0:
        print "target=",target
      else:
        print ""

    elif not_found==False:
      return
  if not_found:
    print inpl,"not found"


def show_433i():
    required= [["am","ly","xl","bx"],
               ["xy","mb","yz","By"],
               ["za","ll","zx","xA"],
               ["yx","bz","zz","ya"]] 
    for quartet in required:
        for pair in quartet:
            lim=100
            if pair=="xy" or "yx":
                # filter out 4.6
                lim=9
            top2=get_2_highest(pair[0],pair[1],lim)
            middle = " "+str(top2[0])+"  "
            if (top2[0],top2[1])==(7,5):
                middle="7(5)"
            elif (top2[0],top2[1])==(4,2): 
                middle="4(2)"
            print pair[0],middle,pair[1],"   ",
        print ""
def make_upper (letter):
    letteru=letter.upper()
    if letter=='l':
        letteru='m'
    if letter=='m':
        letteru='l'
    return letteru


    
def show_433ii():
    print "edges receiving a charge where at least one vertex has degree >=5"
    results=get_vertex_charges(3,5)
    print "no of edge types with charges > 6, 6, 5, 4, 3, 2:",
    i7=0
    i6=0
    i5=0
    i4=0
    i3=0
    i2=0
    for value in results:
        if value[3]>1000: # fraction
            continue
        if value[3]>6:
            i7+=1
        elif value[3] == 6:
            i6+=1
        elif value[3] == 5:
            i5+=1
        elif value[3] == 4:
            i4+=1
        elif value[3] == 3:
            i3+=1
        elif value[3] == 2:
            i2+=1
        
    print i7,",",i6,",",i5,",",i4,",",i3,",",i2
    print "labels of edge types with charge 6:",
    for value in results:
        if value[3]==6:
            print value[0][0],value[0][1],",",
    print ""
    i=0
    print "no of non- (l,l) or (z,z) edges with charges 3, 4 where neither end vertex has degree 4:",  
    for value in results:
        if (value[0]=="ll") or (value[0]=="zz"):
            continue
        if (value[3] == 3) or (value[3]==4):
            if not (value[1] == 4 or value[2] == 4):
                #print value[0]
                i+=1
    print i

    
def prompting (prompt,first_time):
    while True:
      inpl=raw_input(prompt+" ")
      if inpl.startswith('q'):
            break
      if first_time:
          if inpl != 'i':
              inpl='proof'
      prompt='?'
      quit=False
      if first_time:
          set_up_hexagon_charges(configs)
          charge_logic_script('charge_script0.txt',configs,multi_edge_charges)
      first_time=False

      if inpl.startswith('proof'):
          inpl='sh5;5.8;5.9;5.10;ch1;ch2;ch3;ch4;ch5;ch6;q'

      if inpl.startswith('charges'):
          inpl='ch1;ch2;ch3;ch4;ch5;ch6;q'
      comms=inpl.split(';')
      for comm in comms:
          if comm.startswith('q'):
              quit=True
              break
          process_command(comm)
      if quit:
          break
      
def process_command(inpl):
      if inpl=="4.1":
          check_curvature()
          find_overlaps(configs)
      elif inpl.startswith("olaps"):
        find_overlaps(configs)
      elif inpl.startswith("curv"):
        check_curvature()
      elif inpl.startswith("4.33ii"):
          show_433ii()
      elif inpl.startswith("4.33i"):
          show_433i()
      elif inpl.startswith("4."):
        if inpl.endswith('p'):
          show_config_P(inpl[:-1])
        elif inpl.endswith('c'):
          show_config_P(inpl[:-1])
          print "degrees, curvature, deg charge, target, plus curv"
          show_config_C(inpl[:-1])
        else:
          show_config(inpl)
      elif inpl.startswith('gvc'):
          d1=0
          d2=0
          if len(inpl)==5:
              if inpl[3].isdigit():
                     d1=int(inpl[3])
              if inpl[4].isdigit():
                     d2=int(inpl[4]) 
              if d1>0 and d2>0:
                     results=get_vertex_charges(d1,d2)
                     print results
      elif inpl.startswith('gec'):
          if len(inpl)==5:
              get_edge_charges(inpl[3:])
      elif inpl.startswith('sc') and len(inpl)>=6:
          d1=0
          d2=0
          e=4
          f=2
          g=3
          l1=1
          l2=1
          
          if inpl[f]=='-':
              l1=2
              g+=1
              e+=1
          if inpl[g]=='-':
              l2=2
              e+=1
             
              
          if len(inpl)>=e+2:
              if inpl[f+l1-1].isdigit():
                     d1=int(inpl[f:f+l1])
              if inpl[g+l2-1].isdigit():
                     d2=int(inpl[g:g+l2]) 
              if d1<>0 and d2<>0:
                     results=get_vertex_edge_charges(d1,d2,inpl[e:])
                     print results
      elif inpl.startswith('5.1ab'):
          print "find hexagons with +ve curvature in configs A and B"
          show_hex_figAB()
      elif inpl.startswith('5.1cd'):
          print "find hexagons with +ve curvature in configs C and D"
          show_hex_figCD()
      elif inpl.startswith('5.10'):
          do510()
      elif inpl.startswith('5.1'):
          # do the whole lot 
          set_up_hexagon_charges(configs)
          # print "find hexagons with +ve curvature not in configs A,B,C or D"
          # show_hex_fig()
          # print "find hexagons with +ve curvature in configs A and B"
          # show_hex_figAB()
          # print "find hexagons with +ve curvature in configs C and D"
          # show_hex_figCD()
      elif inpl.startswith('5.8'):
          pcd2("5 7 ab") # 5 to 7 charges not ab
      elif inpl.startswith('5.9'):
          pcd3("5 20 ab") # 5 to 9 charges ab
      elif inpl.startswith('pcd3'):
          if len(inpl)==8:
              # pcd3 pqr find maximum charge pq + charge qr
              pqr=inpl[5:8]
              charge=disp_max_combined_charge(pqr)
              print "max combined charge of",pqr,"is",charge
      elif inpl.startswith('pcd'):
          get_max=False
          all_alpha=True
          if len(inpl) >= 6:
              for xx in inpl[4:]:
                  if not xx.isalpha():
                      all_alpha=False
                      break
          if all_alpha:
              disp_max_charges(inpl[4:],[],9,[0,0,'?','?'])
          else:
              filtx=[]
              if len(inpl)>=6:
                  (d1,d2,s1,s2)=(0,0,'?','?')
                  items=inpl[4:].split(' ')
                  if len(items)>=3:
                      if items[0].isdigit():
                          d1 = int(items[0])
                      if items[1].isdigit():
                          d2 = int(items[1])
                  if len(items) >=5:
                      s1=items[2]
                      s2=items[3]
                  t1t2=items[-1]
                  filtx=[d1,d2,s1,s2,t1t2]
                  print_charge_hash(filtx,True)
      elif inpl.startswith('phc'):
          if len(inpl)>=5:
              print_highest_charges(inpl[3:])
      elif inpl.startswith('p21'):
          show_p21_table()
      elif inpl.startswith('p25'):
          print "page 25 Note 2"
          print "charges received across an (a,x^-1)-edge"
          print "v1,v2,charge,source edge,figure"
          for vv in get_vertex_edge_charges(3,3,'aX'):
              print vv
          print "charges received across an (a,y)-edge"
          print "v1,v2,charge,source edge,figure"
          for vv in get_vertex_edge_charges(3,3,'ay'):
              print vv
      elif inpl.startswith('5.6'):
          prove5_6(configs)
      elif inpl.startswith('5.7'):
          prove5_7(configs) 
      elif inpl.startswith('5.2'):
          prove5_6(configs)
          prove5_7(configs) 
      elif inpl.startswith('6.3'):
          prove6_3()
      elif inpl.startswith('6.1'):
          prove6_1()
      elif inpl.startswith('sh1'):
          shadow_edge_logic_script('shadow_script1.txt')
      elif inpl.startswith('sh2'):
          shadow_edge_logic_script('shadow_script2.txt')
      elif inpl.startswith('sh3'):
          shadow_edge_logic_script('shadow_script3.txt')
      elif inpl.startswith('sh4'):
          shadow_edge_logic_script('shadow_script4.txt')
      elif inpl.startswith('sh5'):
          shadow_edge_logic_script('shadow_script5.txt')
      elif inpl.startswith('sh6'):
          shadow_edge_logic_script('shadow_script6.txt')
      elif inpl.startswith('ch1'):
          charge_logic_script('charge_script1.txt',configs,multi_edge_charges)
      elif inpl.startswith('ch2'):
          charge_logic_script('charge_script2.txt',configs,multi_edge_charges)
      elif inpl.startswith('ch3'):
          charge_logic_script('charge_script3.txt',configs,multi_edge_charges)
      elif inpl.startswith('ch4'):
          charge_logic_script('charge_script4.txt',configs,multi_edge_charges)
      elif inpl.startswith('ch5'):
          charge_logic_script('charge_script5.txt',configs,multi_edge_charges)
      elif inpl.startswith('ch6'):
          charge_logic_script('charge_script6.txt',configs,multi_edge_charges)
      elif inpl.startswith('sh'):
          shl=len(inpl)
          if shl==2:
              shadow_edge_logic ()
          else:
              script=inpl[2:].lstrip()
              print script
              shadow_edge_logic_script(script)
      elif inpl.startswith('7.3'):
          circuit='xbYXayBAx'
          circuit="zbYXYAlxz"
          print "circuit=",circuit[:-1]
          # deg4s=[[0] for j in range(len(circuit)-1)]
          deg4s=0
          prev_4=False
          total_maxc=0
          lc=len(circuit)-1

          for i in range(lc):
              hasha={'a':'A','A':'a','b':'B','B':'b','x':'X',
                     'X':'x','y':'Y','Y':'y','l':'m','m':'l',
                     'z':'Z','Z':'z'}
              edge=circuit[i:i+2]
              edge0=edge
              swap=False
              if edge[0].isupper():
                  edge0=hasha[edge[0]] + hasha[edge[1]]
              filtx=[0,0,'?','?',edge0]
              resx=print_charge_hash(filtx,False)
              if len(resx)==0:
                  swap=True
                  edge2=edge0[1] + edge0[0]
                  if edge0[1].isupper():
                      edge2=hasha[edge0[1]] + hasha[edge0[0]]
                  filtx=[0,0,'?','?',edge2]
                  resx=print_charge_hash(filtx,False)
              maxc=0
              deg_status=3
              d4=1
              for item in resx:
                  if item[0]==3 and item[1]==3:
                      d4=0
                  charge=item[ 3]
                  if item[2]<100 and item[2]>maxc:
                      maxc=item[2]
              if  prev_4==False:
                  if d4==1:
                      prev_4=True
                      deg4s+=1
              else:
                  prev_4=False
              print edge,maxc
              total_maxc+=maxc
          if deg4s>0:
              print ".. there are at least",deg4s,"deg 4 vertices"
          max_curv=(2-lc) * 30 + total_maxc + 20*(lc-deg4s) + 15*deg4s
          print "(2-",lc,") * 30 + 20 * (",lc,"-",deg4s,") + 15 *",deg4s,"+",total_maxc
          print "max curvature is",max_curv
          #prove7_3()
      else:
        f75_help()

      
#f75_help()
prompting("type '' for proof or 'i' for interactive",True)
      