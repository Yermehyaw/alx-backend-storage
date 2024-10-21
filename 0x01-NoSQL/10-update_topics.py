#!/usr/bin/env python3
"""
Updates a field of a doc in a collection

Modules Imported: none

"""


def update_topics(mongo_collection, name, topics):
    """Update the docs of a collection with a topics field"""
    filter_prop = {"name": name}
    new_field = {"$set": {"topics": topics}}

    mongo_collection.update_many(filter_prop, new_field)
