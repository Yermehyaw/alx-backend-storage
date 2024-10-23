#!/usr/bin/env python3
"""
Provides data insights from a mongodb dump file

Modules Imported: None

"""


if __name__ == '__main__':
    from pymongo import MongoClient

    """
    Format key metrics from a log file stored as
    mongodb db
    """
    session = MongoClient()
    db = session.logs
    nginx = db.nginx  # collection from db

    print(f'{nginx.count_documents({})} logs')
    print('Methods:')

    no_get = nginx.count_documents({"method": "GET"})
    no_post = nginx.count_documents({"method": "POST"})
    no_put = nginx.count_documents({"method": "PUT"})
    no_patch = nginx.count_documents({"method": "PATCH"})
    no_delete = nginx.count_documents({"method": "DELETE"})

    print(f'\tmethod GET: {no_get}')
    print(f'\tmethod POST: {no_post}')
    print(f'\tmethod PUT: {no_put}')
    print(f'\tmethod PATCH: {no_patch}')
    print(f'\tmethod DELETE: {no_delete}')

    status = nginx.count_documents(
        {
            "$and":
            [
              {"path": "/status"},
              {"method": "GET"}
            ]
        }
    )
    print(f'{status} status check')

    print('IPs:')

