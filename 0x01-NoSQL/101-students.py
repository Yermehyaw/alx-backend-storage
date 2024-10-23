#!/usr/bin/env python3
"""
Sorts the docs in a collection

Modules Imported: None

"""


def top_students(mongo_collection):
    """Returns all students sorted by average score"""
    pipeline = [
            {'$unwind': '$topics'},
            {
                '$addFields': {
                    'averageScore': {'$multiply': ['$topics.score']}
                }
            }
    ]

