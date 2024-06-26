# f75
Python Code to verify Edjvet and Juhasz’s proof that the 
Fibonacci groups in the family {f75,f85} have aspherical presentations.
In the paper 'The infinite Fibonacci groups and relative asphericity' 
Trans. London Math. Soc. (2017) 4(1) 148–218 
accessible, online at

https://londmathsoc.onlinelibrary.wiley.com/doi/pdf/10.1112/tlm3.12007

Martin Edjvet and Arye Juhász work through a long list of enumeration of
cases and curvature calculations to show that presentations of the 
Fibonacci group family defined by {F(7,5),  F(8,5)} are aspherical
 and so infinite. 
This python code aims to follow each step of their proof
and verify that a) all possible cases are covered, b) all
curvature calculations are correct.
The interested reader is therefore offered two choices 

1) read the original paper and check by hand that all 
the calculations are correct and all cases arevcovered 

or

2) understand and/or trust that the attached python 
code is correct and so automates this checking process.

To run type 

 python f75.py 

and then press 'enter'.

The output refers to various sections of the paper
and so can only be understood by reference to the 
paper itself.

The 'proof' is deemed correct if the program finishes
without any error message being displayed.
