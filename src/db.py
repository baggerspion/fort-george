import json
import plyvel

def add_organization(name, data):
    orgdb = plyvel.DB('../data/orgs/', create_if_missing=True)
    orgdb.put(name.encode(), json.dumps(data).encode())
    orgdb.close()

def add_project(org, name, data):
    orgdb = plyvel.DB('../data/orgs/', create_if_missing=True)
    projdb = orgdb.prefixed_db(org.encode())
    projdb.put(name.encode(), json.dumps(data).encode())
    orgdb.close()

