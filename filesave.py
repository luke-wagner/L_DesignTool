def save_grid_to_file(file_path):
    # First get rid of "empty" rows and columns
    # --------------------------------------------------------------------
    # Remove empty rows (rows that only contain 'FE')
    altered_grid = [row for row in grid if any(cell != 'FE' for cell in row)]
    
    # Remove empty columns (columns that only contain 'FE' in each row)
    # Transpose the grid, filter columns, then transpose back
    altered_grid = list(zip(*altered_grid))  # Transpose the grid
    altered_grid = [col for col in altered_grid if any(cell != 'FE' for cell in col)]
    altered_grid = list(zip(*altered_grid))  # Transpose back to the original orientation
    
    # Convert tuples back to lists
    altered_grid = [list(row) for row in altered_grid]
    # --------------------------------------------------------------------

    # Write grid data to file
    with open(file_path, 'w') as file:
        # First write x/y dimensions to file
        file.write(str(len(altered_grid)) + '\n') # x
        file.write(str(len(altered_grid[0])) + '\n') # y

        for row in altered_grid:
            file.write(' '.join(row) + '\n')