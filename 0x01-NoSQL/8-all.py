#!/usr/bin/env python3
"""
Modules Imported: pymongo

"""
if __name__ == '__main__':
    import pymongo


    def list_all(mongo_collection):
        """Makes a list of a mobgodb collection"""
        doc_list = [doc for doc in mongo_collection.find()]

        return doc_list
    
