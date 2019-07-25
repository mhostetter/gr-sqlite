#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2017 Matt Hostetter.
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

class sink(gr.sync_block):
    """
    docstring for block sink
    """
    def __init__(self, filename, table_name, vector_column_name, fixed_position_columns):
        gr.sync_block.__init__(self,
            name="sink",
            in_sig=None,
            out_sig=None)


        self.table_name = table_name
        self.vector_column_name = vector_column_name
        self.fixed_position_columns = fixed_position_columns if type(fixed_position_columns) is list else []

        # Establish database connection
        self.created_table = False
        self.conn = sqlite3.connect(filename, check_same_thread=False)
        self.c = self.conn.cursor()
        self.conn.text_factory = str
        self.c.execute("PRAGMA journal_mode=WAL")

        self.message_port_register_in(pmt.string_to_symbol("pdu"))
        self.set_msg_handler(pmt.string_to_symbol("pdu"), self.insert_pdu_into_table)


    def insert_pdu_into_table(self, pdu):
        # Only process PDUs
        if pmt.is_pair(pdu):
            meta = pmt.to_python(pmt.car(pdu))
            if meta is None:
                meta = dict()

            # Create table if we haven"t already
            if not self.created_table:
                # Find the non fixed-position columns and sort alphabetically
                non_fixed_position_columns = meta.keys()
                for key in self.fixed_position_columns:
                    try:
                        non_fixed_position_columns.remove(key)
                    except:
                        continue

                ordered_keys = self.fixed_position_columns + sorted(non_fixed_position_columns)
                if self.vector_column_name not in ordered_keys:
                    # Add the vector column at the end unless otherwise specified in the Fixed-Position Columns list
                    cols = "(" + ", ".join(ordered_keys) + ", " + self.vector_column_name + ")"
                else:
                    cols = "(" + ", ".join(ordered_keys) + ")"

                # Attempt to create the table
                self.c.execute("CREATE TABLE IF NOT EXISTS " + self.table_name + " " + cols)
                self.conn.commit()
                self.created_table = True

                # Get list of true column names (whether we just made the table or it already existed)
                self.c.execute("SELECT * FROM " + self.table_name)
                self.column_names = [description[0] for description in self.c.description]

            # Set the PDU vector into the meta dictionary with appropriate key
            # meta[self.vector_column_name] = buffer(pmt.to_python(pmt.cdr(pdu)))
            meta[self.vector_column_name] = buffer(pmt.serialize_str(pmt.cdr(pdu)))

            # Insert PDU into table, with only columns that already exist in the table
            valid_keys = [key for key in meta.keys() if key in self.column_names]
            cols = "(" + ", ".join(valid_keys) + ")"
            question_marks = "(" + ", ".join(["?"]*len(valid_keys)) + ")"
            vals = [meta[key] for key in valid_keys]

            self.c.execute("INSERT INTO " + self.table_name + " " + cols + " VALUES " + question_marks, vals)
            self.conn.commit()


    def work(self, input_items, output_items):
        assert False
