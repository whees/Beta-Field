# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 20:58:08 2024

@author: lcuev
"""
import sqlite3 as sql


class Librarian:
    def __init__(self):
        self.con = sql.connect('dab/Tension.sqlite')
        self.cur = self.con.cursor()
        self.places, self.revplaces = self.get_places()

    def get_places(self):
        places = {}
        revplaces = {}
        query = """select holes.x, holes.y from placements 
        inner join holes on holes.id=placements.hole_id 
        where placements.layout_id=11;"""

        fetches = self.cur.execute(query).fetchall()
        for i, fetch in enumerate(fetches):
            places[(fetch[0], fetch[1])] = i
            revplaces[i] = (fetch[0], fetch[1])

        return places, revplaces
