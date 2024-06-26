from f75_processes2 import *
def calc_deficit(line,multi_edge_charges):
  #print "*** calc_deficit called for",line
  qual=''
  res="ok"
  if '<' in line:
    ix=line.index('<')
    ix+=1
    target=""
    targetx=0
    while line[ix].isdigit():
      target+=line[ix]
      ix+=1
    if target.isdigit():
      targetx=int(target)
    if target>0: 
      #print "target deficit is",int(target)
      v_deficits=[0,5,8]
      #line=line[ix:]
      ll=len(line)
      label=""
      while ix<ll:
        if line[ix].isalpha():
          jx=ix
          while jx<ll:
            if line[jx].isalpha(): 
              label+=line[jx]
              jx+=1
              ix+=1
            else:
              break
          if ix<ll:
            if line[ix]=='|':
              qual=line[ix+1:]
          break
        ix+=1
      #print "label=",label
      #expand label at both ends 
      first=return_second(label[0])
      last=return_second(label[-1])
      label=first+label+last

      lenlab=len(label)
      degs=[3,4,5]
      if lenlab==6:
        i,j=0,0
        while i<3:
          j=0
          while j<3:
            param=[3,3,degs[i],degs[j],3,3]
            v_deficit=v_deficits[degs[i]-3] + v_deficits[degs[j]-3]
            res=calc_label_deficit(
              targetx,v_deficit,param,label,multi_edge_charges,qual)
            if res=="FAIL":
              return "FAIL"
            j+=1
          i+=1
      if lenlab==7:
        i,j,k=0,0,0
        while i<3:
          j=0
          while j<3:
            k=0
            while k<3:
              param=[3,3,degs[i],degs[j],degs[k],3,3]
              xy_lets=['x','X','y','Y']
              # deg 3 not possible if this extends the xy sequence
              if degs[i]==3:
                #print "*",label
                if label[2] in xy_lets:
                  k+=1
                  continue
              if degs[k]==3:
                #print "**",label
                if label[4] in xy_lets:
                  k+=1
                  continue
              v_deficit=v_deficits[degs[i]-3] + v_deficits[degs[j]-3] + v_deficits[degs[k]-3]
              res=calc_label_deficit(
                targetx,v_deficit,param,label,multi_edge_charges,qual)
              if res=="FAIL":
                return "FAIL"
              k+=1
            j+=1
          i+=1
  #print len(multi_edge_charges),"multi edge charges"

def return_second(xy_char):
  return_char=''
  in_xy=['x','X','y','Y']
  out_xy=['y','Y','x','X']
  if xy_char in in_xy:
    return_char=out_xy[in_xy.index(xy_char)]
  return return_char
  
def calc_label_deficit(target,v_deficit,param,label,multi_edge_charges,qual):
  #print "calc_label_deficit",param,label
  c_deficit = 4 * (len(label) - 3)
  lab_charge,charges=get_lab_charge(label,param,[])
  deficit=v_deficit + c_deficit - lab_charge + 20
  if deficit < target:
    print label,param,target,v_deficit
    print charges, ' =',lab_charge
    print 'deficit=',deficit,'target=',target
    if qual != '':
      print 'try with qual',qual,'?'
      for mm in multi_edge_charges:
        if qual==mm[0]:
          print mm
        lab_charge2,charges2=overwrite_charge(lab_charge,charges,label,param,mm)
        deficit=v_deficit + c_deficit - lab_charge2 + 20
        if lab_charge2 != lab_charge:
          print charges2, ' =',lab_charge2
          print 'deficit=',deficit,'target=',target
          if deficit >= target:
            break
  if deficit < target:
    print "FAIL"
    return "FAIL"

          
def get_lab_charge(label,param,qual):

  lab_charge=0
  charges=[]
  for i in range(len(label)-1):
    edge=label[i]+label[i+1]
    maxc=0
    if i==0 or i==len(label)-2:
      #first and last edges have charge 10
      maxc=10
    else:
      n_edge,dir=normalize_edges(edge)
      dv1=param[i]
      dv2=param[i+1]
      if dv1 != 3:
        dv1*=11
      if dv2 != 3:
        dv2*=11
      if dir=='-':
        dv1,dv2=dv2,dv1
      filt=[dv1,dv2,'?','?',n_edge]
      resx=print_charge_hash(filt,False)
      #print len(resx)
      if len(resx)>0:
        for rr in resx:
          if rr[2] > 9:
            continue
          if rr[2] > maxc:
            if not (n_edge=='xy' and rr[2] > 8):
              maxc=rr[2]
    charges.append(maxc)
    lab_charge+=maxc
  return lab_charge,charges    

def overwrite_charge(lab_charge,charges,label,param,mm):
  charges2=[]
  for c in charges:
    charges2.append(c)
  lab_charge2=lab_charge
  qual=mm[0]
  ll=len(qual)
  if qual in label:
    ll=len(qual)
    ix=label.index(qual)
    #print 'll,ix',ll,ix
    for i in range(ll):
      deg=int(mm[i+1])
      #print 'deg',deg
      #print 'param',param[ix+i]
      if (deg == 0) or (deg == param[ix+i]):
        if i < ll-1:
          new_charge=int(mm[1+ll+i])
          #print 'new_charge',new_charge
          charges2[ix+i]=new_charge
          #print 'charges2',charges2
          lab_charge2=lab_charge2 - charges[ix+i] + new_charge
          #print 'lab_charge2',lab_charge2
      else:
        return lab_charge,charges
    return lab_charge2,charges2
  return lab_charge,charges
