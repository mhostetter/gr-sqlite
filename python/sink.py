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

import numpy
from gnuradio import gr
import pmt
import sqlite3

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
        self.c.execute('PRAGMA journal_mode=WAL')

        self.message_port_register_in(pmt.string_to_symbol('pdu'))
        self.set_msg_handler(pmt.string_to_symbol('pdu'), self.insert_pdu_into_table)


    def insert_pdu_into_table(self, pdu):
        # Only process PDUs
        if pmt.is_pair(pdu):
            meta = pmt.to_python(pmt.car(pdu))
            vector = pmt.to_python(pmt.cdr(pdu))

            # Create table if haven't already
            if not self.created_table:
                # Find the non fixed-position columns and sort alphabetically
                non_fixed_position_columns = meta.keys()
                for key in self.fixed_position_columns:
                    try:
                        non_fixed_position_columns.remove(key)
                    except:
                        print 'WARNING: Fixed-position column %s is not a key of the input PDU' % (key)

                self.ordered_keys = self.fixed_position_columns + sorted(non_fixed_position_columns)
                cols = '(' + ', '.join(self.ordered_keys) + ', ' + self.vector_column_name + ')'

                self.c.execute('CREATE TABLE IF NOT EXISTS ' + self.table_name + ' ' + cols)
                self.conn.commit()
                self.created_table = True

            cols = '(' + ', '.join(self.ordered_keys) + ', ' + self.vector_column_name + ')'
            val_qs = '(' + ', '.join(['?']*(len(self.ordered_keys)+1)) + ')'
            vals = [meta[key] if key in meta.keys() else None for key in self.ordered_keys]
            vals.append(buffer(vector))

            self.c.execute('INSERT INTO ' + self.table_name + ' ' + cols + ' VALUES ' + val_qs, vals)
            self.conn.commit()


    def work(self, input_items, output_items):
        assert(False)
