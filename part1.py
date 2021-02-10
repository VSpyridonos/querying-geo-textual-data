import sys
import csv
import time


def kwSearchIF(keywords):
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
            print("kwSearchIF: keyword " + kw + "doesn't exist!")

    print("kwSearchIF: " + str(len(results)) + " results, cost = " + str(time.time() - start_time) + " seconds")
    for result in results:
        print(' '.join(data[result]) + '\n')

    return




def kwSearchRaw(keywords):
    start_time = time.time()

    results = []
    first_time = 1
    found = 0

    # For each entry in data list which contains all the file lines
    for entry in data:

        # For each query keyword that has been given
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

    print("kwSearchRaw: " + str(len(results)) + " results, cost = " + str(time.time() - start_time) + " seconds")
    for result in results:
        print(' '.join(result) + '\n')

    return


with open('Restaurants_London_England.tsv', 'r') as infile:
    tsv_reader = csv.reader(infile, delimiter = '\t')
    data = []
    tags_list = []

    # Dictionary which has tags as keys and lines in which tags appear as values
    inverted_file = {}
    line_counter = 0

    # Read the whole file
    while True:
        try:
            # Variable s holds the new line that is read
            s = next(tsv_reader)

            # Every entry in data list is a file line
            data.append(s)

            # In order to put the tags of each line in inverted_file
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

            line_counter += 1

        except StopIteration:
            break


    print("\nnumber of keywords: " + str(len(inverted_file)))

    # The frequency of distinct keywords
    frequencies = []
    for k, v in inverted_file.items():
        frequencies.append(len(v))

    # Ascending sort
    frequencies.sort()
    print("frequencies: " + str(frequencies) + '\n')

    # List that contains all query keywords
    query_keywords = []
    for i in range(1,len(sys.argv)):
        query_keywords.append(sys.argv[i])

    # Call functions with query_keywords as a parameter
    kwSearchIF(query_keywords)
    kwSearchRaw(query_keywords)
