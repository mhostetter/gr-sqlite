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
| Parameter | Description |
| --- | --- |
| **Filename** | |
| **Table Name** | |
| **Primary Key** | |
| **Fixed-Position Column** | |


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
