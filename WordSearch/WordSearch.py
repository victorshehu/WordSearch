import os


from pip._vendor.msgpack.fallback import xrange


def matrixify(grid, separator='\n'):
    return grid.split(separator)

def coord_char(coord, matrix): # this function returns the element located at that row and column:
    row_index, column_index = coord
    return matrix[row_index][column_index]

def convert_to_word(coord_matrix, matrix): # This function will run through a list of coordinates through a for loop and gets the single length strings using coord_char:
    return ''.join([coord_char(coord, matrix)
                   for coord in coord_matrix])


def find_base_match(char, matrix): #This function runs throug the grid and find the letters that match the find letter of the word we are looking for

    base_matches = [(row_index, column_index)
                    for row_index, row in enumerate(matrix)
                    for column_index, column in enumerate(row)
                    if char == column]

    return base_matches

def matched_neighbors(coord, char, matrix, row_length, col_length): #This function returns a list of the adjacent coordinates that match the given character
    row_num, col_num = coord
    neighbors_coords = [(row, column)
                        for row in xrange(row_num - 1,
                                          row_num + 2)
                        for column in xrange(col_num - 1,
                                             col_num + 2)
                        if row_length > row >= 0
                        and col_length > column >= 0
                        and coord_char((row,column),matrix) == char
                        and not (row, column) == coord]

    return neighbors_coords

def complete_line(base_coord, targ_coord, word_len, row_length, col_len):#This function check the given pattern has a match for the letters that follow the first letter of the word we are searching for
    if word_len == 2:
        return base_coord, targ_coord

    line = [base_coord, targ_coord]
    diff_1, diff_2 = targ_coord[0] - base_coord[0], targ_coord[1] - base_coord[1]

    for _ in xrange(word_len - 2):
        line += [(line[-1][0] + diff_1, line[-1][1] + diff_2)]

    if 0 <= line[-1][0] < row_length and 0 <= line[-1][1] < col_len:
        return line
    return []

def complete_match(word, matrix, base_match, word_len, row_len,col_len): # this function  applis the complete_line to all the neighbors of the first match.
    new = (complete_line(base, n, word_len, row_len, col_len)
           for base in base_match
           for n in matched_neighbors(base, word[1], matrix,
                                      row_len, col_len))

    return [ero for ero in new
            if convert_to_word(ero, matrix) == word]

print ("Enter the name of the file") #Prompt user to enter filename
Filename = input()


with open(Filename, 'r') as f:  # open the file
    row_num = f.readline(1) #get the num of rows
    f.readline(1)
    col_num = f.readline(1)#get the num of cols


with open(Filename, 'r') as f:  # open the file
    next(f)  # skips the first line that  the dimension of the grid
    grid = f.read().replace(' ', '').replace('\n',  ' ') #filters out the whitespace and the newline

matrix = matrixify(grid, ' ')
del matrix[int(row_num):]


with open(Filename, 'r') as f:  # open the file
    next(f)  # skips the first line that  the dimension of the grid
    for i in range(0, int(row_num)):
        next(f)
    words = f.read().replace(' ', '').replace('\n', ' ')  # filters out the whitespace and the newline

matrix_words = matrixify(words, ' ')


for i in matrix_words:

    base_match = find_base_match(i[0], matrix)
    result = (complete_match(i, matrix, base_match, len(i), int(row_num), int(col_num)))


    start_index = str(result[0][0]) # Turn the element at this positon and turns it to string so it can be manipulated
    start_index = start_index.replace(',', ':').replace('(', '').replace(')', '').replace(' ', '')

    end_index = str(result[0][len(i) - 1])
    end_index = end_index.replace(',', ':').replace('(', '').replace(')', '').replace(' ', '')

    formatted_results = " {} {} {}".format(i, start_index, end_index)

    print(formatted_results)

    input()
