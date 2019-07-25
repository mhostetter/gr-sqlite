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

import numpy as np
import sqlite3

import pmt
from gnuradio import gr

class triggered_source(gr.sync_block):
    """
    docstring for block triggered_source
    """
    def __init__(self, filename, table_name, vector_column_name, sql_condition):
        gr.sync_block.__init__(self,
            name="triggered_source",
            in_sig=None,
            out_sig=None)

        self.table_name = table_name
        self.vector_column_name = vector_column_name
        self.sql_condition = sql_condition

        # Establish database connection
        self.conn = sqlite3.connect(filename, check_same_thread=False)
        self.c = self.conn.cursor()
        self.conn.text_factory = str

        # Start SQL query and then fetch one row per trigger
        self.c.execute("SELECT * FROM " + self.table_name + " " + self.sql_condition)

        self.message_port_register_in(pmt.string_to_symbol("trigger"))
        self.message_port_register_out(pmt.string_to_symbol("pdu"))
        self.set_msg_handler(pmt.string_to_symbol("trigger"), self.fetch_new_pdu)


    def fetch_new_pdu(self, trigger):
        # Fetch the next row of the database
        row = self.c.fetchone()

        if row is not None:
            # Format into PDU
            meta = dict()
            vector = None
            for idx, col in enumerate(self.c.description):
                column = col[0]
                if column == self.vector_column_name:
                    vector = pmt.to_python(pmt.deserialize_str(str(row[idx])))
                else:
                    meta[col[0]] = row[idx]

            pdu = pmt.cons(pmt.to_pmt(meta), pmt.to_pmt(vector))
            self.message_port_pub(pmt.string_to_symbol("pdu"), pdu)


    def work(self, input_items, output_items):
        assert(False)
