# querying-geo-textual-data
Implementing an inverted file and a spatial index for quering geo-textual data with Python 3. Data used is a tsv file with information about restaurants in London. Information includes restaurant name, latitude-longitude and tags like breakfast, hamburgers, chinese, bar, etc...

<p><h2>Part 1: Creating the inverted file and using it to perform key-words/tags queries (inverted_file.py)</h2>

</p>

<p><h3>Usage</h3>
python3 inverted_file.py query_keywords
</p>

<p><h2>Part 2: Creating the spatial index and using it to perform spatial/latitude-longitude queries (spatial_index.py) </h2>

</p>

<p><h3>Usage</h3>
python3 spatial_index.py query_rectangle_range(x-low, x-high, y-low, y-high)
</p>


