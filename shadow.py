# project = automate shadow edge checking
# for octagon calculate all shadow edges and corner labelling
# for 3 b-segements show that no possible shadowing for n2<8

def add_shadow_edges(edges,s):
    # start from 1
    no_vertices=edges[0]
    for i in range(1,no_vertices+1):
        for j in range(1,no_vertices+1):
            if (((j-i) > 1) or ((i-j) > 1)):
                print i,j
                # (i,j) is a potential shadow edge
                # check if it already exists
                # check if it crosses with another shadow edge
                # if not add this edge
                # if s==1 then check validity of diag
                # print if ok
                
def process_shape(no_vertices):
    edges=[no_vertices]
    for i in range(1,no_vertices+1):
        next_i=i+1
        if next_i==no_vertices+1:
            next_i=1
        edges.append([i,next_i])
    print edges
    # max no of shadow edges = n-3
    for s in range(no_vertices-3):
        diag=add_shadow_edges(edges,s)
process_shape(8)
#process_shape(4)





