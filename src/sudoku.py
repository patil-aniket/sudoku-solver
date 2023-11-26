

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import sys
import time

ROW = "ABCDEFGHI"
COL = "123456789"


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)


def find_MRV(board):
    min_MRV = 11
    res = (None, None, None)
    for r in ROW:
        for c in COL:
            if board[r + c] == 0:
                possible_values = get_MRV(board, r, c)
                currentCount = len(possible_values)
                if min_MRV > currentCount:
                    min_MRV = currentCount
                    res = (r, c, possible_values)
    return res


def get_MRV(board, r, c):
    possible_values = set(range(1, 10))
    for i in COL:
        if i != c:
            possible_values.discard(board[r+i])
    for j in ROW:
        if j != r:
            possible_values.discard(board[j+c])
    startIndexOfR = (ROW.index(r) // 3) * 3
    startIndexOfC = (COL.index(c) // 3) * 3
    for i in ROW[startIndexOfR: startIndexOfR + 3]:
        for j in COL[startIndexOfC: startIndexOfC + 3]:
            if i != r and j != c:
                possible_values.discard(board[i+j])
    return possible_values


# def is_valid_board(board, r, c, num):
#     for i in COL:
#         if i != c and board[r+i] == num:
#             return False
#     for j in ROW:
#         if j != r and board[j+c] == num:
#             return False
#     startIndexOfR = (ROW.index(r) // 3) * 3
#     startIndexOfC = (COL.index(c) // 3) * 3
#     for i in ROW[startIndexOfR: startIndexOfR + 3]:
#         for j in COL[startIndexOfC: startIndexOfC + 3]:
#             if i != r and j != c and board[i+j] == num:
#                 return False
#     return True


def backtracking(board):
    """Takes a board and returns solved board."""
    # TODO: implement this
    r, c, possible_values = find_MRV(board)
    if r is None and c is None:
        return board
    for i in possible_values:
        board[r+c] = i
        if backtracking(board) != False:
            return board
        # backtracking if no further solution is found
        board[r+c] = 0
    return False


if __name__ == '__main__':
    if len(sys.argv) > 1:

        # Running sudoku solver with one board $python3 sudoku.py <input_string>.
        print(sys.argv[1])
        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = {ROW[r] + COL[c]: int(sys.argv[1][9*r+c])
                 for r in range(9) for c in range(9)}

        solved_board = backtracking(board)

        # Write board to file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(board_to_string(solved_board))
        outfile.write('\n')

    else:
        # Running sudoku solver for boards in sudokus_start.txt $python3 sudoku.py

        #  Read boards from source.
        src_filename = 'sudokus_start.txt'
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")

        # Solve each board using backtracking
        tic = time.perf_counter()
        for line in sudoku_list.split("\n"):

            if len(line) < 9:
                continue

            # Parse boards to dict representation, scanning board L to R, Up to Down
            board = {ROW[r] + COL[c]: int(line[9*r+c])
                     for r in range(9) for c in range(9)}

            # Print starting board. TODO: Comment this out when timing runs.
            print_board(board)

            # Solve with backtracking

            solved_board = backtracking(board)

            # Print solved board. TODO: Comment this out when timing runs.
            print_board(solved_board)

            # Write board to file
            outfile.write(board_to_string(solved_board))
            outfile.write('\n')
        toc = time.perf_counter()
        print(f"Finished all boards in file in {toc - tic:0.4f} seconds.")
