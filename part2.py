import sys
import csv
import time


def spaSearchGrid(qrange):

    start_time = time.time()
    results = []
    temp = []
    end_search = 0

    # Use coord_array (list) to find which restaurants are inside the query range. These restaurants will be found from the grid
    for i in range(50):
        if end_search == 1:
            break
        for j in range(50):


            # When the x-low of a range is larger than the x-high of the query range, then break because there is no way a restaurant
            # is inside the query range. Also, break out of the outer loop as all ranges from that spot and beyond will have larger x-highs
            if float(coord_array[i][j][0][0]) > qrange[1]:
                end_search = 1
                break

            # When the x-low of a range is larger than the x-high of the query range, then break because there is no way a restaurant
            # is inside the query range. Saves computation time.
            if float(coord_array[i][j][1][0]) > qrange[3] :
                break

            # Condictions to check if x and y ranges are intersecting with the range query
            x_intersect_cond1 = (float(coord_array[i][j][0][0]) >= float(qrange[0]) and float(coord_array[i][j][0][0]) <= float(qrange[1]))
            x_intersect_cond2 = (float(coord_array[i][j][0][1]) >= float(qrange[0]) and float(coord_array[i][j][0][1]) <= float(qrange[1]))
            x_intersect_cond3 = (float(coord_array[i][j][0][0]) < float(qrange[0]) and float(coord_array[i][j][0][1]) > float(qrange[1]))
            y_intersect_cond1 = (float(coord_array[i][j][1][0]) >= float(qrange[2]) and float(coord_array[i][j][1][0]) <= float(qrange[3]))
            y_intersect_cond2 = (float(coord_array[i][j][1][1]) >= float(qrange[2]) and float(coord_array[i][j][1][1]) <= float(qrange[3]))
            y_intersect_cond3 = (float(coord_array[i][j][1][0]) < float(qrange[2]) and float(coord_array[i][j][1][1]) > float(qrange[3]))
            x_intersect = x_intersect_cond1 or x_intersect_cond2 or x_intersect_cond3
            y_intersect = y_intersect_cond1 or y_intersect_cond2 or y_intersect_cond3
            is_intersecting = x_intersect and y_intersect


            # Conditions to check if x and y ranges are inside the range query
            x_inside_cond1 = (float(coord_array[i][j][0][0]) <= float(qrange[0])) and (float(coord_array[i][j][0][0]) >= float(qrange[1]))
            x_inside_cond2 = (float(coord_array[i][j][0][1]) <= float(qrange[0])) and (float(coord_array[i][j][0][1]) >= float(qrange[1]))
            y_inside_cond1 = (float(coord_array[i][j][1][0]) <= float(qrange[2])) and (float(coord_array[i][j][1][0]) >= float(qrange[3]))
            y_inside_cond2 = (float(coord_array[i][j][1][1]) <= float(qrange[2])) and (float(coord_array[i][j][1][1]) >= float(qrange[3]))
            x_inside = x_inside_cond1 or x_inside_cond2
            y_inside = y_inside_cond1 or y_inside_cond2
            is_inside = x_inside and y_inside

            if is_inside or is_intersecting:
                temp = []

                # In case they are intersecting, check if the restaurants are inside the query range
                for el in grid[i][j]:
                    if qrange[0] <= locations_list[el][0] and qrange[1] >= locations_list[el][0] and qrange[2] <= locations_list[el][1] and qrange[3] >= locations_list[el][1]:
                        temp.append(el)
                results.append(temp)

    # For each list with restaurants that got in results list, find its number of restaurants and adds it to number_of_results
    number_of_results = 0
    for list in results:
        number_of_results += len(list)

    print("\nspaSearchGrid: " + str(number_of_results) + " results, cost = " + str(time.time() - start_time) + " seconds")
    for result in results:
        for res in result:
            print(' '.join(data[res]))

    return



def spaSearchRaw(qrange):

    start_time = time.time()
    results = []
    line_counter = 0

    # For each entry in data list that contains all the file lines
    for entry in data:
        # In order to take the coordinates of every restaurant
        location = entry[1]
        location = location[10:]
        x_y = location.split(',')

        # x and y coordinates of each restaurant
        x = float(x_y[0])
        y = float(x_y[1])

        # Check if every restaurant is inside the range query. If it is, put in results list
        if qrange[0] <= x and qrange[1] >= x and qrange[2] <= y and qrange[3] >= y:
            results.append(line_counter)

        line_counter += 1


    print("\nspaSearchRaw: " + str(len(results)) + " results, cost = " + str(time.time() - start_time) + " seconds")
    for result in results:
        print(data[result])

    return

with open('Restaurants_London_England.tsv', 'r') as infile:
    tsv_reader = csv.reader(infile, delimiter = '\t')
    data = []
    locations_list = []
    first_time = 1

    # Read file until the end
    while True:
        try:
            # Variable s contains the new line that is read
            s = next(tsv_reader)

            # Every entry is a file line in data list
            data.append(s)

            # In order to take the coordinates of every restaurant
            location = s[1]
            location = location[10:]
            x_y = location.split(',')

            # x and y coordinates of every restaurant
            x = float(x_y[0])
            y = float(x_y[1])

            # List with all the coordinates
            locations_list.append([x, y])


            # Vriskw ti megalyteri kai mikroteri timi tis kathe syntetagmenis
            # Find the largest and smallest value of each coordinate
            if first_time == 1:
                xmax = x
                ymax = y
                xmin = x
                ymin = y
                first_time = 0

            if x < xmin:
                xmin = x

            if x > xmax:
                xmax = x

            if y < ymin:
                ymin = y

            if y > ymax:
                ymax = y


        except StopIteration:
            break

    # Value range of x and y coordinates
    x_min_max_difference = float(xmax) - float(xmin)
    y_min_max_difference = float(ymin) - float(ymax)

    # Distance between cells so that 50 are created
    x_space_distance = x_min_max_difference / 50
    y_space_distance = y_min_max_difference / 50


    x_lists = []
    y_lists = []
    x1 = xmin
    y1 = ymin

    # Creation of x and y ranges
    for i in range(50):
        x_inserted_list = [x1, x1 + x_space_distance]
        x_lists.append(x_inserted_list)
        x1 = x1 + x_space_distance

        y_inserted_list = [y1, y1 - y_space_distance]
        y_lists.append(y_inserted_list)
        y1 = y1 - y_space_distance


    temp = []
    coord_array = []
    grid = []


    # Initiate grid creation and create coord_array which has the correct x, y ranges in each index.
    # In every index inside grid, an empty list is put which will be filled later
    # with the restaurant locations
    for i in range(50):
        row = []
        empty_row = []
        for j in range(50):
            temp = [x_lists[i], y_lists[j]]
            row.append(temp)

            empty_list = []
            empty_row.append(empty_list)
        coord_array.append(row)
        grid.append(empty_row)


    line_counter = 0
    # For every location
    # locations_list[0] = x, locations_list[1] = y
    for el in locations_list:
        x = el[0]
        y = el[1]

        # Grid creation
        for i in range(50):
            for j in range(50):
                # For each restaurant location, check inside which x and y range it falls into and place it in the corresponding grid index
                if x >= coord_array[i][j][0][0] and x < coord_array[i][j][0][1] and y >= coord_array[i][j][1][0] and y < coord_array[i][j][1][1]:
                    grid[i][j].append(line_counter)
                    break

        line_counter += 1


    # Print results
    print("\nbounds: " + str(xmin) + ' ' + str(xmax) + ' ' + str(ymin) + ' ' + str(ymax))
    print("widths: " + str(xmax - xmin) + ' ' + str(ymin - ymax))

    for i in range(50):
        for j in range(50):
            if grid[i][j]:
                print(str(i) + ' ' + str(j) + ' ' + str(len(grid[i][j])))


    # List that contains range query
    range_queries = []
    for i in range(1,len(sys.argv)):
        range_queries.append(float(sys.argv[i]))


    # Call functions with range query as a parameter
    spaSearchGrid(range_queries)
    spaSearchRaw(range_queries)
