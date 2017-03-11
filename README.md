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
The SQLite Sink block is designed to take PDU messages as input and insert them into one table of a SQLite database.  The PDU metadata (`pmt::car`) is stored in columns equal to their keys and the PDU vector (`pmt::cdr`) is stored with column name `data` and type BLOB.

Only one "type" of PDU should be connected to a SQLite Sink, with "type" meaning a unique set of metadata keys.  The first PDU inputted to the sink will create a table in the database, if it does not already exist, with column definitions set by that PDU.  If the first PDU has metadata keys `a, b, c`, the table will be created with columns `a, b, c, data`.  If a subsequent PDU is inputted with different metadata keys `x, y`, the block will insert a row with only matching columns, in this case one the `data` column (corresponding to the PDU vector) match.

This block is designed for a type of PDU, for instance decoded bursts or demodulated bursts, to be logged into one database table.  To log multiple types of PDUs in the same flowgraph, you can use multiple SQLite Sinks with different table names.

| Parameter | Description |
| --- | --- |
| **Filename** | The database filename. |
| **Table Name** | The name of the table to insert the PDUs into. |
| **Primary Key** | **Optional:** The column name of the table to set as Primary Key.  Set to `''` if not desired. |
| **Fixed-Position Columns** | **Optional:** A Python list of column names. |


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
