#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2017 <+YOU OR YOUR COMPANY+>.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

import datetime
import threading
import sqlite3
import time
import numpy as np

import pmt
from gnuradio import gr

class timed_source(gr.sync_block):
    """
    docstring for block timed_source
    """
    def __init__(self, filename, table_name, vector_column_name, timestamp_column_name, db_start_timestamp, realtime_factor):
        gr.sync_block.__init__(self,
            name="timed_source",
            in_sig=None,
            out_sig=None)

        self.table_name = table_name
        self.vector_column_name = vector_column_name
        self.timestamp_column_name = timestamp_column_name
        self.db_start_timestamp = db_start_timestamp
        self.realtime_factor = realtime_factor

        # Setup run thread
        self.thread = threading.Thread(target=self.run)

        # Establish database connection
        self.conn = sqlite3.connect(filename, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()

        if self.db_start_timestamp is None:
            # Get first timestamp from database
            self.c.execute(
                "SELECT * FROM " + self.table_name + " " +
                "ORDER BY " + self.timestamp_column_name + " ASC" + " " +
                "LIMIT 1"
            )
            row = self.c.fetchone()
            self.db_start_timestamp = int(np.floor(row[self.timestamp_column_name]))

        # Start SQL query and then fetch one row per time delay
        self.c.execute(
            "SELECT * FROM " + self.table_name + " " +
            "WHERE " + self.timestamp_column_name + " >= " + str(self.db_start_timestamp) + " " +
            "ORDER BY " + self.timestamp_column_name + " ASC"
        )

        self.message_port_register_out(pmt.to_pmt("pdu"))


    def start(self):
        self.block_start_time = datetime.datetime.utcnow()
        self.block_sim_delta = self.block_start_time - datetime.datetime.utcfromtimestamp(self.db_start_timestamp)
        self.thread.start()
        return True


    def stop(self):
        self.thread.join()
        return True


    def run(self):
        for row in self.c:
            # Format into PDU
            meta = dict(row)
            vector = meta.pop(self.vector_column_name, None)
            vector = pmt.to_python(pmt.deserialize_str(str(vector)))

            # Calculate time to sleep
            current_sim_time = self.calculate_sim_time()
            pdu_time = datetime.datetime.utcfromtimestamp(meta[self.timestamp_column_name])
            seconds_to_sleep = (pdu_time - current_sim_time).total_seconds()

            # Sleep until PDU publish time
            if seconds_to_sleep > 0.0:
                time.sleep(seconds_to_sleep)

            # Publish PDU
            try:
                pdu = pmt.cons(pmt.to_pmt(meta), pmt.to_pmt(vector))
                self.message_port_pub(pmt.to_pmt("pdu"), pdu)
            except:
                return


    def calculate_sim_time(self):
        current_time = datetime.datetime.utcnow()
        elapsed_time = current_time - self.block_start_time
        return (current_time - self.block_sim_delta) + datetime.timedelta(seconds=elapsed_time.total_seconds()*self.realtime_factor)


    def work(self, input_items, output_items):
        assert False
