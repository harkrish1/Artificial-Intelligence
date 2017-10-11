#!/usr/bin/env python
# nrooks.py : Solve the N-Rooks problem!
# D. Crandall, 2016
# Updated by Zehua Zhang, 2017
# Updated by Harshit Krishnakumar, 2017
#
# The N-rooks problem is: Given an empty NxN chessboard, place N rooks on the board so that no rooks
# can take any other, i.e. such that no two rooks share the same row or column.

import sys
import random

# Count # of pieces in given row
def count_on_row(board, row):
    return sum( board[row] ) 

# Count # of pieces in given column
def count_on_col(board, col):
    return sum( [ row[col] for row in board ] ) 

# Count # of pieces on the backward diagonal (\) of the position 
def count_on_back_diag(board,row,col):
	count = 0
	while row < N-1 and col < N-1: 
		# First reach the top end of the diagonal 
		row+=1
		col+=1
	while row >=0 and col >=0:
		# Count back along the diagonal
		count = count + board[row][col]
		row-=1
		col-=1
	return count

# Count # of pieces on the forward diagonal (\) of the position 
def count_on_forw_diag(board, row, col):
	count = 0
	while row < N-1 and col > 0: 
		# First reach the bottom end of the diagonal 
		row+=1
		col-=1
	while row >= 0 and col < N:
		# Count back along the diagonal
		count = count + board[row][col]
		row-=1
		col+=1
	return count 

def count_conflicts_nqueens(board, row, col):
	return count_on_row(board,row)+count_on_col(board,col)+count_on_back_diag(board,row,col)+count_on_forw_diag(board,row,col) - (4*board[row][col] ) if [row,col] !=[x_blocked, y_blocked] else N*N

def total_conflicts_nqueen(board,row):	
	return [count_conflicts_nqueens(board, row,c) for c in range(N)]

# Count total # of pieces on board
def count_pieces(board):
    return sum([ sum(row) for row in board ] )

# Return a string with the board rendered in a human-friendly format
def printable_board_nrooks(board,x_block,y_block):
	if x_block<0 and y_block<0:
		return "\n".join([ " ".join([ "R" if board[r][c] else "_" for c in range(N) ]) for r in range(N)])
	else:
		return "\n".join([ " ".join([ "R" if board[r][c] else "X" if [r,c]==[x_block,y_block] else "_" for c in range(N) ]) for r in range(N)])

# Return a string with the board rendered in a human-friendly format
def printable_board_nqueens(board,x_block,y_block):
	if x_block<0 and y_block<0:
		return "\n".join([ " ".join([ "Q" if board[r][c] else "_" for c in range(N) ]) for r in range(N)])
	else:
		return "\n".join([ " ".join([ "Q" if board[r][c] else "X" if [r,c]==[x_block,y_block] else "_" for c in range(N) ]) for r in range(N)])

# Add a piece to the board at the given position, and return a new board (doesn't change original)
def add_piece(board, row, col):
	board[row][col] = 1
	return board

# Get list of successors of given board state
def successors(board):
    return [ add_piece(board, r, c) for r in range(0, N) for c in range(0,N) ]

def successors2(board):	
	# Checking if all total number of pieces on board are less than N, and there are no pieces in the same row and column as the iteration )
	# Added a check for blocked position
	list_of_boards=list()
	if count_pieces(board) <N:
		for r in range(N):
			if count_on_row(board,r)==0:
				for c in range(N):
					if [r,c]!=[x_blocked,y_blocked]:
						if count_on_row(board,r)+count_on_col(board,c) ==0:
							list_of_boards.append(add_piece(board, r, c))
	return list_of_boards
	
# check if board is a goal state
def is_goal_nrooks(board):
    return count_pieces(board) == N

def is_goal_nqueens(board):
    return count_pieces(board) == N and \
        all( [ count_on_row(board, r) <= 1 for r in range(0, N) ] ) and \
        all( [ count_on_col(board, c) <= 1 for c in range(0, N) ] ) and \
		all( [ count_on_back_diag(board, r, c) <= 1 and count_on_forw_diag(board, r, c) <=1 for r in range(0, N) for c in range(0, N) ] )		

# Solve n-rooks!
def solve_nrooks(initial_board):
    fringe = [initial_board]
    while len(fringe) > 0:
        for s in successors2( fringe.pop() ): # DFS
        # for s in successors2( fringe.pop(0) ): # BFS
            if is_goal_nrooks(s):
                return(s)
            fringe.append(s)
    return False

# Solve n-queens!
def solve_nqueens(initial_board):
	upper_iter = 0
	while upper_iter< 100 if N < 20 else 10000 :
		initial_board = [[0]*N for _ in range(N)]
		# Place n queens on the board one in every row, randomly
		for r in range(N):
			conflicts = total_conflicts_nqueen(initial_board,r)
			min_conf = min(conflicts)
			indices = [i for i, x in enumerate(conflicts) if x == min_conf]
			move_to = random.randint(0,len(indices)-1)
			move_to = indices[move_to]
			initial_board[r][move_to]=1
			
			# initial_board[r][random.randint(0,N-1)] = 1
		iter = 0
		while iter <1000:
			if is_goal_nqueens(initial_board):
				return initial_board
			# Randomly select one row to move the queen
			r = random.randint(0,N-1)
			conflicts = total_conflicts_nqueen(initial_board,r)
			# Check if queen is already in zero conflicts
			if conflicts[initial_board[r].index(1)]>0: 
				# If not, then move the queen to a lower conflicted place
				# Ties are broken randomly
				min_conf = min(conflicts)
				indices = [i for i, x in enumerate(conflicts) if x == min_conf]
				move_to = random.randint(0,len(indices)-1)
				move_to = indices[move_to]
				initial_board[r][initial_board[r].index(1)]=0
				initial_board[r][move_to]=1
			iter +=1
		upper_iter+=1
	return False



# Getting all inputs from user. It is passed through command line arguments.
problem_type = sys.argv[1]
N = sys.argv[2]
x_blocked = sys.argv[3]
y_blocked = sys.argv[4]

# Checking the inputs if user entered right values:

if problem_type not in ('nrook', 'nqueen'):
	print ('\n Error in problem type, Enter nrook or nqueen \n')
	sys.exit()

	
try:
	N= int(N)
except:
	print ('\n Error in second arguement, Enter a positive integer for N \n')
	sys.exit()


if N<0:
	print ('\n Error in second arguement, Enter a positive integer for N \n')
	sys.exit()

try:
	x_blocked = int(x_blocked)-1
except:
	print ('\n Error in third arguement, Enter an integer between 1 and N for x coordinate of blocked position, enter 0 for no blocked position \n')
	sys.exit()
	
try:
	y_blocked = int(y_blocked)-1
except:
	print ('\n Error in fourth arguement, Enter an integer between 1 and N for x coordinate of blocked position, enter 0 for no blocked position \n')
	sys.exit()
	
if not(x_blocked in range(-1,N)):
	print ('\n Error in third arguement, Enter an integer between 1 and N for x coordinate of blocked position, enter 0 for no blocked position \n')
	sys.exit()
if not(y_blocked in range(-1,N)):
	print ('\n Error in fourth arguement, Enter an integer between 1 and N for y coordinate of blocked position, enter 0 for no blocked position \n')
	sys.exit()



# The board is stored as a list-of-lists. Each inner list is a row of the board.
# A zero in a given square indicates no piece, and a 1 indicates a piece.
initial_board = [[0]*N for _ in range(N)]
print ("Starting from initial board:\n" + printable_board_nqueens(initial_board, x_blocked, y_blocked) + "\n\nLooking for solution...\n")



if problem_type == 'nrook':
	solution = solve_nrooks(initial_board)
	print (printable_board_nrooks(solution, x_blocked, y_blocked) if solution else "Sorry, no solution found. :(")
elif problem_type == 'nqueen':
	solution = solve_nqueens(initial_board)
	print (printable_board_nqueens(solution, x_blocked, y_blocked) if solution else "Sorry, no solution found. :(")




