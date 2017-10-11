#!/usr/bin/env python
# nrooks.py : Solve the N-Rooks problem!
# D. Crandall, 2016
# Updated by Zehua Zhang, 2017
# Updated by Harshit Krishnakumar, 2017
#
# The N-rooks problem is: Given an empty NxN chessboard, place N rooks on the board so that no rooks
# can take any other, i.e. such that no two rooks share the same row or column.

import sys

# Count # of pieces in given row
def count_on_row(board, row):
    return sum( board[row] ) 

# Count # of pieces in given column
def count_on_col(board, col):
    return sum( [ row[col] for row in board ] ) 

# Count total # of pieces on board
def count_pieces(board):
    return sum([ sum(row) for row in board ] )

# Return a string with the board rendered in a human-friendly format
def printable_board(board):
    return "\n".join([ " ".join([ "R" if col else "_" for col in row ]) for row in board])

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
					if count_on_row(board,r)+count_on_col(board,c) ==0:
						list_of_boards.append(add_piece(board, r, c))
	return list_of_boards
	
# check if board is a goal state
def is_goal(board):
    return count_pieces(board) == N 

# Solve n-rooks!
def solve(initial_board):
    fringe = [initial_board]
    while len(fringe) > 0:
        for s in successors2( fringe.pop() ): # DFS
        # for s in successors2( fringe.pop(0) ): # BFS
            if is_goal(s):
                return(s)
            fringe.append(s)
    return False

# This is N, the size of the board. It is passed through command line arguments.
N = int(sys.argv[1])

# The board is stored as a list-of-lists. Each inner list is a row of the board.
# A zero in a given square indicates no piece, and a 1 indicates a piece.
initial_board = [[0]*N for _ in range(N)]
print ("Starting from initial board:\n" + printable_board(initial_board) + "\n\nLooking for solution...\n")
solution = solve(initial_board)

print (printable_board(solution) if solution else "Sorry, no solution found. :(")


