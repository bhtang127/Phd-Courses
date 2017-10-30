import numpy as np

si = np.matrix([[ 3.09574148, -0.06653618,  0.64183925],
                [-0.06653618,  3.09574148,  0.64183925],
                [ 0.64183925,  0.64183925,  0.41962453]])

u1 = [2,5,1.554774]
u2 = [1,0,-2.053749]

n = 200000000

sample1 = np.random.randn(n,3)
sample2 = np.random.randn(n,3)
sp1 = np.array(sample1.dot(si.T) + u1)
sp2 = np.array(sample2.dot(si.T) + u2)

sp1p = sp1[sp1[:,2]>0]
sp1n = sp1[sp1[:,2]<0]

e1 = (np.sum(sp1p[:,0]) + np.sum(sp1n[:,1])) / n
e3 = (2 * len(sp1p[:,0]) + 5 * len(sp1n[:,1])) / n

sp2p = sp2[sp2[:,2]>0]
sp2n = sp2[sp2[:,2]<0]

e2 = (np.sum(sp2p[:,0]) + np.sum(sp2n[:,1])) / n
e4 = len(sp2p[:,0]) / n

print(e1,e2,e3,e4)