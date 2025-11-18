# f75
Python Code to automate and verify Edjvet and Juhasz’s proof that the 
Fibonacci groups in the family {f(7,5),f(8,5)} have aspherical presentations.

In the paper 'The infinite Fibonacci groups and relative asphericity' 
Trans. London Math. Soc. (2017) 4(1) 148–218, 

accessible online at

https://londmathsoc.onlinelibrary.wiley.com/doi/pdf/10.1112/tlm3.12007
or
https://arxiv.org/abs/1708.01194

Martin Edjvet and Arye Juhász determine various enumerations of 
possible cases and curvature calculations to show that presentations of the 
Fibonacci group family defined by {f(7,5), f(8,5)} are aspherical
 and so define infinite groups. 

The python code f75.py aims to follow each step of this  paper
and verify that 

a) all possible cases are covered, 

b) all curvature calculations are as stated.

The interested reader is, therefore, offered two choices 

1) read the original paper and check by hand that all 
the calculations are correct and all cases are covered 

or

2) understand and/or trust that the attached python 
code is correct and so automates this checking process.

To run type 

 python f75.py 

and then press 'enter'.

The output refers to various sections of the paper
and so can only be properly understood by reference to the 
paper itself. 

However, I wrote this program based on a prepublished 
version of the paper and the labelling of figures in
the code no longer correspond to the figures in the
published paper!! How annoying - sorry!

The 'proof' is deemed correct if the program finishes
without any error message being displayed.

# Quick technical summary of proof.

The Fibonacci groups F(7,5) and F(8,5) have the 
same split extension with relative presentation  
belonging to the class 

Pn = <t,u| t^5,t^2utu^−n> (n ≥ 7).

The dual of pictures of this presentation comprises 
n+1 sided faces with boundary labels u^-1u^-n and 
corner labels t(=a), t^2 (=b) and t^0.

Such dual pictures are geometrically identical to 
certain van Kampen diagrams of the 'Fibonacci type' groups 
with cyclically symetrical presentations, eg

<a, b, c, d, e|

a=dbecadb

b=ecadbec

c=adbecad

d=becadbe

e=cadbeca>

where, the geometry of the van Kampen diagram 
is determined solely by the number of so called 
'outward' and 'inward' edges incident at each vertex 
and the assigned 'angles' between them. 

The angle between consecutive outward edges is +/-2 and 
corresponds to the corner label t^2 above. 
The angle between consecutive inward edges is +/-1 
and corresponds to the corner label t^1 above. 
All other angles between edges pair off and cancel 
each other out and so may as well be regarded as 0. 

We then require that the sum of the angles between 
edges incident at a non-boundary vertex is equal 
to 0 mod 5.

We consider pictures/van Kampen diagrams which are 
minimal as regards number of faces and maximal as 
regards number of vertices of degree 2.

Then, using a complex averaging out of local 
curvature of faces which results in a non-positive
value being obtained,  a contradiction to 
Eulers V-E+F=2 formula is arrived at if we suppose
that a spherical picture or diagram satisfying these 
minimal and maximal constraints exists.

Demonstrating that the average local curvature of 
faces is non-positive is equivalent to showing that 
the average interior vertex degree of the 
corresponding triangulated van Kampen diagram is >=6.
