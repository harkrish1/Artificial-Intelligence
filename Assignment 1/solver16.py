#!/usr/bin/env python
'''
(1) I formulated this search problem by using a star algorithm with algorithm number 2. I am considering an admissible heuristic function and a cost function.

State Space: Set of all possible arrangements of 15 pieces on a 4 X 4 space.

Successor Function: Set of possible moves from the given initial configuration. This will be after moving one, two or three pieces near the blank space

Edge Weights: 1, since every move costs one

Goal State: 

1  2  3  4 
5  6  7  8
9  10 11 12
13 14 15 X

Heuristic Function(s): The current implementation takes Manhattan distance of all pieces from their actual positions / 3. This is because maximum of three pieces can move to their actual positions at any move. Thus, it is not possible to over estimate the cost and so it is admissible. 

(2) This algorithm uses Python's heapq to implement the fringe data structure. We also use Python sets to store the visited states, so that we dont revisit states. The first step in the algorithm after reading the input is to check if the initial state is reachable, using number of permutation inversions. Next the solve() function is called, and it pushes the initial board into the fringe, and the loop runs till we find the goal state. 

(3) I faced the problem of optimizing the code to run quickly. I replaced all my list of lists with heapq and sets. I also removed deepcopy functions, all numpy functions and made alternative implementations of these which are quicker. I used Python's cProfile to look at the time consuming functions, and I found that the function "find_index" is the one which runs the most amount of times, and hence it takes the maximum time. I tried my best to optimize this function.
'''

import heapq as hq
import sys

def find_index(board, i):
	r = [r for r, row in enumerate(board) if i in row][0]
	return r, [c for c,col in enumerate(board[r]) if i == col][0]

goal = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]]
goal_coordinates = {}
for i in range(1,16):
	goal_coordinates[i]=find_index(goal,i)

def swap(inp_board,push_direction):
	if inp_board is None:
		return
	z_row,z_col=find_index(inp_board,0)
	if push_direction == 'down':
		if z_row-1 >= 0: 
			board = [[j for j in i]for i in inp_board]
			board[z_row][z_col] = board[z_row-1][z_col]
			board[z_row-1][z_col] = 0
		else:
			return
	elif push_direction == 'up':
		if z_row+1 <4:
			board = [[j for j in i]for i in inp_board]
			board[z_row][z_col] = board[z_row+1][z_col]
			board[z_row+1][z_col] = 0
		else:
			return
	elif push_direction == 'left':
		if z_col+1 < 4:
			board = [[j for j in i]for i in inp_board]
			board[z_row][z_col] = board[z_row][z_col+1]
			board[z_row][z_col+1] = 0
		else:
			return
	elif push_direction == 'right':
		if z_col-1 >=0:
			board = [[j for j in i]for i in inp_board]
			board[z_row][z_col] = board[z_row][z_col-1]
			board[z_row][z_col-1] = 0
		else:
			return
	else:
		return
	return board
			
			
def succ(board, visit):
	g = board[0]+1
	path = board[1]
	r,c=find_index(board[2],0)
	r = str(r+1)
	c = str(c+1)
	successors = []
	successors.append([g, path+' L1'+r, swap(board[2],'left')])
	successors.append([g, path+' L2'+r, swap(successors[-1][2],'left')])
	successors.append([g, path+' L3'+r, swap(successors[-1][2],'left')])

	successors.append([g, path+' R1'+r, swap(board[2],'right')])
	successors.append([g, path+' R2'+r, swap(successors[-1][2],'right')])
	successors.append([g, path+' R3'+r, swap(successors[-1][2],'right')])
	
	successors.append([g, path+' U1'+c, swap(board[2],'up')])
	successors.append([g, path+' U2'+c, swap(successors[-1][2],'up')])
	successors.append([g, path+' U3'+c, swap(successors[-1][2],'up')])
	
	successors.append([g, path+' D1'+c, swap(board[2],'down')])
	successors.append([g, path+' D2'+c, swap(successors[-1][2],'down')])
	successors.append([g, path+' D3'+c, swap(successors[-1][2],'down')])
	return [x for x in successors if x[2] is not None  and str(x[2]) not in visit ]

	
def man_dist(board, i):
	r,c = find_index(board,i)
	return abs(r - goal_coordinates[i][0]) + abs(c - goal_coordinates[i][1])
	
def heu_fun(board):
	dist = 0
	for i in range(1,16):
		# dist += man_dist(board[2],i)*(16-i)/float(15)
		dist += man_dist(board[2],i)/float(3)
	return (dist+board[0]), board


def solve(initial_board):
	fringe = []
	visited = set()
	hq.heappush(fringe, (0, [0, '', initial_board]))
	visited.add(str(initial_board))
	while fringe :
		popped = hq.heappop(fringe)[-1]
		visited.add(str(popped[-1]))
		for s in succ(popped, visited): 
			if (s[2]==goal):
				return(s[1].lstrip(' '))
			hq.heappush(fringe, heu_fun(s))
	return False


def check_input_parity(input):
	input_checking = [col  for row in input for col in row]
	zero_row, zero_col = find_index(input,0)
	input_checking.remove(0)
	permutations = 0
	for i in range(len(input_checking)):
		for j in input_checking[i+1:]:
			if input_checking[i] > j:
				permutations+=1
	if ((4-zero_row )% 2 != 0 and permutations %2 != 0) or ((4-zero_row )% 2 == 0 and permutations %2 == 0):
		return False
	return True

# Get Filename from command line
filename = sys.argv[1]

# Read the file
with open(filename) as f:
	board = f.readlines()
input = [[int(col) for col in row.split()] for row in board]

# Check if state is reachable, then solve it.
if check_input_parity(input):
	print(solve(input))
else: 
	print(False)