# querying-geo-textual-data
Implementing an inverted file and a spatial index for quering geo-textual data with Python 3. Data used is a tsv file with information about restaurants in London. Information includes restaurant name, latitude-longitude and tags like breakfast, hamburgers, chinese, bar, etc...

<p>
<h2>Part 1: Creating the inverted file and using it to perform key-words/tags queries (inverted_file.py)</h2>
Reads all data from the restaurant file and saves it in a list, where each entry is a file line. While reading the data, the inverted file is being created in main memory. For each tag, every line number that contains it is put in ascending order into the inverted file. Using the lines that have been written in the lists, the restaurants that contain the corresponding tags can be recovered. The number of distinct keywords and their frequency is printed.
</p>

<p>
Function kwSearchIF takes a sequence of query keywords as a parameter and uses the inverted file to find the entries that contain all of them.
</p>

<p>
Function kwSearchRaw takes a sequence of query keywords as a parameter, reads all the entries and returns those that contain all query keywords without using the inverted file.
</p>

<p>After giving query keywords as command line arguments, the file lines that correspond to restaurants which contain all the query keywords in their tags are printed. Functions kwSearchIF and kwSearchRaw are called and their results and run times are printed.</p>


<p>
<h3>Usage</h3>
python3 inverted_file.py query_keywords
</p>

<p>
<h3>Results</h3>
kwSearchIF is quite faster than kwSearchRaw.
</p>

<p>
<h2>Part 2: Creating the spatial index and using it to perform spatial/latitude-longitude queries (spatial_index.py)</h2>
Reads all data from the restaurant file and saves it in a list, where each entry is a file line. A spatial index based on a grid from the file data is created. The grid splits the space that restaurant coordinates cover in 50*50 = 2500 equal sized cells (rectangles). In each grid cell, the line (entry) numbers of the restaurants that fall into the corresponding range are saved. For each dimension (x, y), it prints the smallest and largest value of the restaurant dimensions and the value range in each dimension. After the grid is created, the number of restaurants for each cell that isn't empty is printed.
</p>

<p>
Function spaSearchGrid takes a two-dimensional rectangle area (range query) as a parameter and returns the restaurants inside that area using the grid.
</p>

<p>
Function spaSearchRaw takes a range query as a parameter and returns the restaurants inside that area without using the grid.
</p>

<p>
After giving the query range's coordinates as command line arguments, the file lines that correspond to restaurants which are inside the query range are printed. Functions spaSearchGrid and spaSearchRaw are called and their results and run times are printed.
</p>

<p>
<h3>Usage</h3>
python3 spatial_index.py query_rectangle_range(x-low, x-high, y-low, y-high)
</p>

<p>
<h3>Results</h3
spaSearchGrid is quite faster than spaSearchRaw.
</p>

<p>
<h2>Part 3: Geo-textual queries</h2>
Reads all data and creates the above mentionted inverted file and grid.
</p>

<p>
Function kwSpaSearchIf takes a query range and a sequence of query keywords as parameters and returns the restaurants that are inside the query range and contain all the query keywords in their tags. The inverted file is used to find the restaurants that contain the query keywords and for each one of those, verifies that it is inside the query range.
</p>

<p>Function kwSpaSearchGrid takes a query range and a sequence of query keywords as parameters and returns the restaurants that are inside the query range and contain all the query keywords in their tags. The grid is used to find the restaurants that are inside the query range and for each one of those, verifies that it contains all the query keywords in its tags.
</p>

<p>
Function kwSpaSearchRaw takes a query range and a sequence of query keywords as parameters and returns the restaurants that are inside the query range and contain all the query keywords in their tags. For each of the restaurants, it checks if it's inside the query range and if it contains all the query keywords in its tags without using the inverted file or the grid.
</p>

<p>
After giving the query range's coordinates and at least one query keyword, it prints the file lines that correspond to restaurants that are inside the query range and contain all the query keywords in their tags. Functions kwSpaSearchIF, kwSpaSearchGrid and kwSpaSearchRaw are called and their results and run times are printed.
</p>

<p>
<h3>Usage</h3>
python3 spatial_index.py query_rectangle_range(x-low, x-high, y-low, y-high) query_keywords
</p>

<p>
<h3>Results</h3>
kwSpaSearchIf's and kwSpaSearchGrid's run times are quite similar. They are both quite faster than kwSpaSearchRaw.
</p>

