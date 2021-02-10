import sys
import csv
import time


def kwSpaSearchIF(qrange, keywords):

    start_time = time.time()

    results = []
    first_time = 1

    # For every query keyword that has been given
    for kw in keywords:

        # If keyword exists in inverted_file
        if kw in inverted_file:

            # If it's the first keyword, then results variable will be equal
            # to all the lines that it appears
            if first_time == 1:
                results = inverted_file[kw]

                # Tuple with exactly the same elements as results
                temp = tuple(results)
                first_time = 0
                continue

            # For every element (line number) of the tuple
            for el in temp:

                # If this line number doesn't exist in
                # the line numbers of this specifig tag
                if el not in inverted_file[kw]:

                    # Remove it from the results list
                    results.pop(results.index(el))
            temp = tuple(results)

        else:
            print("kwSpaSearchIF: keyword " + kw + "doesn't exist!")

    # The list with the final results
    final_results = []

    # For every restaurant that contains all query keywords, checks if it is inside the range query
    for result in results:
        if qrange[0] <= locations_list[result][0] and qrange[1] >= locations_list[result][0] and qrange[2] <= locations_list[result][1] and qrange[3] >= locations_list[result][1]:
            final_results.append(result)


    print("\nkwSpaSearchIF: " + str(len(final_results)) + " results, cost = " + str(time.time() - start_time) + " seconds")

    for result in final_results:
        print(' '.join(data[result]))

    return




def kwSpaSearchGrid(qrange, keywords):

    start_time = time.time()
    results = []
    final_results = []

    # Use coord_array (list) to find which restaurants are inside the query range. These restaurants will be found from the grid
    for i in range(50):
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


    found = 0

    # For every list with restaurants that got into results, checks if the restaurants
    # contain all the query keywords in their tags
    for list in results:
        for el in list:
            # For every query keyword that has been given
            for kw in keywords:
                found = 0
                temp = data[el][2]
                temp = temp[6:]
                temp = temp.split(',')
                # What temp will look like: temp = "['chinese', 'thai']"

                # For each tag in temp variable
                for tag in temp:

                    # If the keyword equals the tag
                    if kw == tag:
                        found = 1
                        break
                    else:
                        continue

                # If no keyword was found, get the next entry of data list
                if found == 0:
                    break

            # If all keywords were found in an entry, then put it in results list
            if found == 1:
                final_results.append(el)

    print("\nkwSpaSearchGrid: " + str(len(final_results)) + " results, cost = " + str(time.time() - start_time) + " seconds")
    for result in final_results:
        print(' '.join(data[result]))


    return



def kwSpaSearchRaw(qrange, keywords):

    start_time = time.time()
    results = []
    line_counter = 0

    # For each entry in data list which contains all the file lines
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
            for kw in keywords:
                found = 0
                temp = entry[2]
                temp = temp[6:]
                temp = temp.split(',')
                # What temp will look like: temp = "['chinese', 'thai']"

                # For each tag in temp variable
                for tag in temp:

                    # If the keyword equals the tag
                    if kw == tag:
                        found = 1
                        break
                    else:
                        continue

                # If no keyword was found, get the next entry of data list
                if found == 0:
                    break

            # If all keywords were found in an entry, then put it in results list
            if found == 1:
                results.append(entry)


    print("\nkwSpaSearchRaw: " + str(len(results)) + " results, cost = " + str(time.time() - start_time) + " seconds")
    for result in results:
        print(' '.join(result))


    return



with open('Restaurants_London_England.tsv', 'r') as infile:
    tsv_reader = csv.reader(infile, delimiter = '\t')
    data = []
    tags_list = []
    locations_list = []
    first_time = 1

    # Dictionary which has restaurant tags as keys and lines where tags appear as values
    inverted_file = {}
    line_counter = 0

    # Read the whole file
    while True:
        try:
            # Variable s contains the new line that is read
            s = next(tsv_reader)

            # Every entry is a file line in data list
            data.append(s)

            '''
            ###################
               inverted file
            ###################
            '''

            # In order to put each restaurant's/line's tags into inverted file
            for i in range(2, len(s)):
                # What tags will look like: tags = "tags: chinese,thai"
                tags = s[i]

                # What tag will look like: tag = "['tags: chinese', 'thai']"
                tag = tags.split(',')

                if i == 2:
                    # What first_tag will look like: first_tag = "chinese"
                    # Use it only to get the first tag
                    first_tag = tag[0][6:]

                    # If the first tag doesn't exist in the list with all the tags
                    if first_tag not in tags_list:
                        # Then append it to the list
                        tags_list.append(first_tag)
                        # Put the new pair in inverted_file
                        inverted_file[first_tag] = [line_counter]
                    else:
                        # Else, just append the new line number in inverted_file in tag's values
                        inverted_file[first_tag].append(line_counter)

            # In order to put the rest of the tags or tag-line_of_appearance pairs in inverted_file
            for k in range(1, len(tag)):
                if tag[k] not in tags_list:
                    tags_list.append(tag[k])
                    inverted_file[tag[k]] = [line_counter]
                else:
                    inverted_file[tag[k]].append(line_counter)


            '''
            ##################
                   Grid
            ##################
            '''

            # In order to take the coordinates of every restaurant
            location = s[1]
            location = location[10:]
            x_y = location.split(',')

            # x and y coordinates of every restaurant
            x = float(x_y[0])
            y = float(x_y[1])

            # List with all the coordinates
            locations_list.append([x, y])


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



            line_counter += 1

        except StopIteration:
            break

    '''
    ###################
       Grid again
    ###################
    '''

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


    range_queries = []
    query_keywords = []
    for i in range(1,len(sys.argv)):
        if i < 5:
            range_queries.append(float(sys.argv[i]))
        else:
            query_keywords.append(sys.argv[i])

    # Call functions with the range query and the query keywords sequence as parameters
    kwSpaSearchRaw(range_queries, query_keywords)
    kwSpaSearchIF(range_queries, query_keywords)
    kwSpaSearchGrid(range_queries, query_keywords)
