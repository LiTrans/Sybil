from IPython.display import display
import numpy
from scipy.optimize import linprog


C=12         #numbers of RSUs
S=100
'''%Utility computing'''
'''W=randi([10 20],C);%average trip delay at intersection i after attack'''
W_B = numpy.random.random((1, C)) #its ndArray
#W = numpy.matrix(W_B)# it is matrix
W=[12,15,3,15,12,35,45,12,4,10,23,2]
'''T=randi([10 20],C);%average normal trip delay at intersection i'''
T_B = numpy.random.random((1, C)) #its ndArray
#T = numpy.matrix(T_B)# it is matrix
T=[11,14,1,14,11,32,41,11,2,9,21,1]

'''U=zeros(C); % attacker utility matrix'''
U= numpy.zeros((C, C))


for i in range(C):
    for j in range(C):
        if i==j:
           #U[i-1][j-1] = W[0,i-1]-T[0,i-1]
		   U[i-1][j-1] = W[i-1]-T[i-1]
        else:
            U[i-1][j-1] = 0
'''%Optimization problem of the defense'''
#f= numpy.zeros((1, C+1))
#f[0][0]= 1
f= [1,0,0,0,0,0,0,0,0,0,0,0,0]

#lb= numpy.zeros((C+1, 1))
#lb[0][0]= -10000
Aeq= numpy.ones((1, C+1))
Aeq[0][0]= 0
#Aeq=[0,1,1,1,1,1,1,1,1,1,1,1,1]
beq=1
b=[0,0,0,0,0,0,0,0,0,0,0,0]
#print(len(b))
#print(type(beq))
#print(A.shape)
#A=[-1*ones(C,1) U];
b_1= [[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1],[-1]]

A= numpy.concatenate((b_1, U), axis=1)
res = linprog(f, A, b, Aeq, beq, bounds=[(-10000,None), (0,None), (0,None),(0,None),(0,None),(0,None),(0,None),(0,None),(0,None),(0,None),(0,None),(0,None),(0,None)])
p=res.x
print(p)
'''[p,y1(end+1)] = linprog(f, A, b, Aeq, beq, lb);

%fair strategy for decision making
y2(end+1)=max(U*(ones(C,1)*1/C)); %utility values
z=1/C; %weight of information collected at each intersection in trivial non smart mitigation'''
    
#%Optimization problem (attacker)
f= [1,0,0,0,0,0,0,0,0,0,0,0,0]
#lb=[-1000; zeros(C,1)];
#ub=[1000; ones(C,1)];
Aeq= numpy.ones((1, C+1))
Aeq[0][0]= 0
beq=1;
#A=[ones(C,1) -1*U'];
#print(U)
U= -1*U.transpose()
#print(U)
b_1= [[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1],[1]]
A= numpy.concatenate((b_1, U), axis=1)
b=[0,0,0,0,0,0,0,0,0,0,0,0]
f= [-1,0,0,0,0,0,0,0,0,0,0,0,0]
res = linprog(f, A, b, Aeq, beq, bounds=[(-1000,1000), (0,1), (0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1)]);
q=res.x
print(q)


						
						
						
						
						
						
						
						
						
						
						
						
						
						