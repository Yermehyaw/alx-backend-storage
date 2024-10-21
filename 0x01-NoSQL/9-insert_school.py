#!/usr/bin/env python3
"""
Insert a doc into a collection

Modules Imported:

"""


def insert_school(mongo_collection, **kwargs):
    """Insert a doc to mongo_collection"""
    new_doc = mongo_collection.insert_one(kwargs)

    return new_doc.inserted_id
