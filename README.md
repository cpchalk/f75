# f75
Python Code to automate and verify Edjvet and Juhasz’s proof that the 
Fibonacci groups in the family {f(7,5),f(8,5)} have aspherical presentations.

In the paper 'The infinite Fibonacci groups and relative asphericity' 
Trans. London Math. Soc. (2017) 4(1) 148–218, 

accessible, online at

https://londmathsoc.onlinelibrary.wiley.com/doi/pdf/10.1112/tlm3.12007

Martin Edjvet and Arye Juhász determine various enumerations of 
possible cases and curvature calculations to show that presentations of the 
Fibonacci group family defined by {f(7,5),  f(8,5)} are aspherical
 and so define infinite groups. 
The python code f75.py aims to follow each step of this  paper
and verify that 

a) all possible cases are covered, 

b) all curvature calculations are as stated
.
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

The 'proof' is deemed correct if the program finishes
without any error message being displayed.
