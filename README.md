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
The SQLite Sink block is designed to take a PDU message as input and insert it into one table in a SQLite database.  The PDU metadata is stored with columns equal to their keys and the PDU vector is stored with column name `data` and type BLOB.  Only one type of PDU should be connected to a SQLite Sink.

| Parameter | Description |
| --- | --- |
| **Filename** | The database filename. |
| **Table Name** | The name of the table to insert the PDUs into. |
| **Primary Key** | **Optional:** The column name of the table to set as Primary Key.  Set to `''` if not desired. |
| **Fixed-Position Column** | **Optional:** A Python list of column names. |


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
