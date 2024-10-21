#!/usr/bin/env python3
"""
Finds all sxhool docs with a specific topic field value
and returns it as a list

Modules Imported: None

"""


def schools_by_topic(mongo_collection, topic):
    """Returns a lost of docs with a spec field value"""
    filter_prop = {"topic": topic}

    doc_list = [doc for doc in mongo_collection.find(filter_prop)]

    return doc_list
