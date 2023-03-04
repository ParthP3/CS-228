### TEAM MEMBERS
## Parth Pujari: <210100106>
## Anish Kulkarni: <21b090003>
## Jennisha Aggarwal: <210050074>


from z3 import *
import sys

file = sys.argv[1]

with open(file) as f:
	n,T = [int(x) for x in next(f).split()]
	matrix = []
	for line in f:
		matrix.append([int(x) for x in line.split()])

T=T+1
s = Solver()
X = [[[ Int("x_%s_%s_%s" % (i, j, t)) for t in range(T)] for j in range(n) ]for i in range(n)  ] 
M = [Int("m_%s" %(k)) for k in range(T)]

something_c = [And(X[i][j][t]<=n*n, X[i][j][t]>=1) for i in range(n) for j in range(n) for t in range(T)]
#distinct_c = [Distinct(X[i][j]) for i in range(n)for j in range(n)]
moves_rr = [Implies(M[t]== i, X[i%n][j][t] == X[i][(j+1)%n][t+1]) for i in range(n) for j in range(n) for t in range(T-1)]
moves_rl = [Implies(M[t]== i, X[i%n][j][t] == X[i%n][(j-1)%n][t+1]) for i in range(n,2*n) for j in range(n) for t in range(T-1)]
moves_cd = [Implies(M[t]== j, X[i][j%n][t] == X[(i+1)%n][j%n][t+1]) for j in range(2*n, 3*n) for i in range(n) for t in range(T-1)]
moves_cu = [Implies(M[t]== j, X[i][j%n][t] == X[(i-1)%n][j%n][t+1]) for j in range(3*n, 4*n) for i in range(n) for t in range(T-1)]


non_moves = []
for t in range(T-1):
	for j in range(n):
		for i in range(n):
			non_moves.append(Implies(And(M[t]!=i,M[t]!=n+i,M[t]!=2*n+j,M[t]!=3*n+j),X[i][j][t]==X[i][j][t+1]))


move_nothing = [Implies(M[t]==4*n, X[i][j][t]==X[i][j][t+1]) for i in range(n) for j in range(n) for t in range(T-1)]
# Set s to the required formula
move_limit = [And(M[i]<=4*n , M[i]>=0) for i in range(T)]
final_pos = [X[i][j][T-1] == n*i+j+1 for i in range(n) for j in range(n)]

start_pos = [ X[i][j][0] == matrix[i][j] for i in range(n) for j in range(n)]
s.add(moves_rr+moves_rl+moves_cd+moves_cu+move_nothing+move_limit+final_pos+start_pos+non_moves+something_c)
x = s.check()
print(x)
if x == sat:
	m = s.model()

	for i in range(T-1):
		a=(m.evaluate(M[i])).as_long()
		if a<n:
			print(f"{int(a)}r")
		elif a<2*n:
			print(f"{int(a-(n))}l")
		elif a<3*n:
			print(f"{int(a-(2*n))}d")
		elif a<4*n:
			print(f"{int(a-(3*n))}u")

	
	# Output the moves