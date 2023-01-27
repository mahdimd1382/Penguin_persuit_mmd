
def rotate_map(board):
    converted = []

    for n_col in range(len(board[0])):
        new_list = []
        for n_row in board[::-1]:
            new_list.append(n_row[n_col])
        converted.append(new_list)

    for n_row in converted:
        for n_col in range(len(n_row)):
            if n_row[n_col] == "v" or n_row[n_col] == "b":
                try:
                    if n_row[n_col + 1] == "h" or n_row[n_col + 1] == "b":
                        n_row[n_col] = "b"
                    else:
                        n_row[n_col] = "h"
                except:
                    n_row[n_col] = "h"
            else:
                try:
                    if n_row[n_col + 1] == "h" or n_row[n_col + 1] == "b":
                        n_row[n_col] = "v"
                    else:
                        n_row[n_col] = " "
                except:
                    n_row[n_col] = " "

    return converted
