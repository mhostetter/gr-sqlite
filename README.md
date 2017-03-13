# gr-sqlite
A GNU Radio Out-Of-Tree (OOT) Module to write to and read from SQLite databases.


## Features
* Supports `INSERT`-ing PDU messages into a SQLite table.
* Supports outputting PDUs from message-triggered `SELECT` statements.
* Supports timed PDU output based of a UNIX timestamp in the SQLite database.

## Usage
### GNU Radio
There are example GNU Radio Companion (.grc) files located in `/gr-sqlite/examples/`.  To use them, first open GNU Radio Companion `$ gnuradio-companion` and then open the .grc file.

* `sqlite_sink.grc` An example of how to log PDUs into a SQLite database
* `sqlite_triggered_source.grc` An example of how to generate PDU from a database table upon a message trigger


### Blocks
#### SQLite Sink
![SQLite Sink](https://github.com/mhostetter/gr-sqlite/blob/master/docs/sqlite_sink.png)

The SQLite Sink block is designed to take PDU messages as input and insert them into one table of a SQLite database.  The PDU metadata (`pmt::car`) is stored in columns equal to their keys and the PDU vector (`pmt::cdr`) is stored in a column specified by **PDU Vector Column Name** (default is `data`).  The vector will be stored as a serialized PMT `BLOB`.  This allows for reconstruction of PMT type later.

Only one "type" of PDU should be connected to a SQLite Sink, with "type" meaning a unique set of metadata keys.  When the sink receives the first PDU input it will create a table named **Table Name** in the database, if it does not already exist, with columns defined by that PDU.  If the first PDU has metadata keys `a, b, c`, the table will be created with columns `a, b, c, data`.  If a subsequent PDU is inputted with different metadata keys `x, y`, the block will insert a row into the table with only matching columns.  In this case only the `data` column (corresponding to the PDU vector) matches.  This block is designed for one type of PDU, for instance demodulated or decoded bursts, to be logged into one database table.  To log multiple types of PDUs into multiple tables in the same flowgraph, you can use multiple SQLite Sinks with different table names.

Because the metadata key/value pairs are unordered, it's impossible for the user to specify the desired column order in the PDU itself.  By default, the block will sort the metadata keys alphabetically and then append the vector column.  For example, if the first PDU has metadata keys `timestamp, snr, frequency`, the table will be created with columns ordered as `frequency, snr, timestamp, data`.  However, a user might want timestamp to be the first column.  This is achieved by adding `'timestamp'` to the **Fixed-Position Columns** Python list.  Enter a subset (or the full set) of columns listed in the desired column order.  To set timestamp to be the first column, **Fixed-Position Columns** should be `['timestamp']`.  Any columns not specified in **Fixed-Position Columns** will be appended in alphabetically order.  In this example the new column order would be `timestamp, frequency, snr, data`.  To not specify any column positions, just leave **Fixed-Position Columns** as an empty list `[]`.

#### SQLite Triggered Source
![SQLite Triggered Source](https://github.com/mhostetter/gr-sqlite/blob/master/docs/sqlite_triggered_source.png)

The SQLite Triggered Source block is designed to take asynchronous message triggers and output PDU messages generated from the rows of one table in a SQLite database.  The **PDU Vector Column Name** column of table **Table Name** will be formatted into the PDU vector (`pmt::cdr`) and the remaining columns will be formatted into a dictionary in the PDU metadata (`pmt::car`).

Additional SQL query conditions can be enforced through the **SQL Condition**.  The condition should start with the `WHERE` keyword.  **WARNING:** This string will be entered directly into the SQL query with no sanitization.  Buyer beware!

Example **SQL Condition** fields include:

* `'WHERE timestamp > 1489233600'`
* `'WHERE timestamp > ' + (datetime.datetime(year=2017, month=3, day=11, hour=12, minute=0) - datetime.datetime.utcfromtimestamp(0)).total_seconds()`
* `'WHERE timestamp IS NOT NULL'`
* `'WHERE snr > 20.0'`
* `'WHERE frequency > -1000 AND frequency < 1000'`

#### SQLite Timed Source
![SQLite Timed Source](https://github.com/mhostetter/gr-sqlite/blob/master/docs/sqlite_timed_source.png)

The SQLite Timed Source block is designed to output PDU messages generated from the rows of one table in a SQLite database in realtime.  The block requires a UNIX timestamp in the database, specified by **Timestamp Column Name**.  When the flowgraph starts, the block will output rows at **Realtime Factor** times realtime starting at **Start Timestamp**.  The **PDU Vector Column Name** column of table **Table Name** will be formatted into the PDU vector (`pmt::cdr`) and the remaining columns will be formatted into a dictionary in the PDU metadata (`pmt::car`).

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
