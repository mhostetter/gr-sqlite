# gr-sqlite
A GNU Radio Out-Of-Tree (OOT) Module to write to and read from SQLite databases.


## Features
* Supports inserting asynchronous PDU messages to a SQLite table.
* Supports setting table Primary Key.
* Supports fixed column ordering.


## Usage
### GNU Radio
There are example GNU Radio Companion (.grc) files located in `/gr-sqlite/examples/`.  To use them, first open GNU Radio Companion `$ gnuradio-companion` and then open the .grc file.

### Blocks
#### SQLite Sink
![SQLite Sink](https://github.com/mhostetter/gr-sqlite/blob/master/docs/sqlite_sink.png)

The SQLite Sink block is designed to take PDU messages as input and insert them into one table of a SQLite database.  The PDU metadata (`pmt::car`) is stored in columns equal to their keys and the PDU vector (`pmt::cdr`) is stored in a column specified by **PDU Vector Column Name** (default is `data`).

Only one "type" of PDU should be connected to a SQLite Sink, with "type" meaning a unique set of metadata keys.  When the sink receives the first PDU input it will create a table named **Table Name** in the database, if it does not already exist, with columns defined by that PDU.  If the first PDU has metadata keys `a, b, c`, the table will be created with columns `a, b, c, data`.  If a subsequent PDU is inputted with different metadata keys `x, y`, the block will insert a row into the table with only matching columns.  In this case only the `data` column (corresponding to the PDU vector) matches.  This block is designed for one type of PDU, for instance demodulated or decoded bursts, to be logged into one database table.  To log multiple types of PDUs into multiple tables in the same flowgraph, you can use multiple SQLite Sinks with different table names.

Because the metadata key/value pairs are unordered, it's impossible for the user to specify the desired column order in the PDU itself.  By default, the block will sort the metadata keys alphabetically and then append the vector column.  For example, if the first PDU has metadata keys `timestamp, snr, frequency`, the table will be created with columns ordered as `frequency, snr, timestamp, data`.  However, a user might want timestamp to be the first column.  This is achieved by adding `'timestamp'` to the **Fixed-Position Columns** Python list.  Enter a subset (or the full set) of columns listed in the desired column order.  To set timestamp to be the first column, **Fixed-Position Columns** should be `['timestamp']`.  Any columns not specified in **Fixed-Position Columns** will be appended in alphabetically order.  In this example the new column order would be `timestamp, frequency, snr, data`.  To not specify any column positions, just leave **Fixed-Position Columns** as an empty list `[]`.

### Viewing the Database
I've personally had great success using [DbVisualizer](https://www.dbvis.com/) to inspect, query, and modify databases.  If you don't have a SQLite viewer, I suggest you look into it.  It's supported on Linux, Mac, and Windows.


## Installation
GNU Radio is a dependency for gr-sqlite.  I recommend installing it with [PyBOMBS](https://github.com/gnuradio/pybombs).

### Source Build
To build gr-sqlite manually from source, follow this procedure.

1. `$ cd gr-sqlite`
2. `$ mkdir build`
3. `$ cd build`
4. `$ cmake ../` or `$ cmake -DCMAKE_INSTALL_PREFIX=<path_to_install> ../`
5. `$ make`
6. `$ sudo make install`
7. `$ sudo ldconfig`
