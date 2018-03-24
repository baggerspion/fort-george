import json
import plyvel

def add_organization(name, data):
    orgdb = plyvel.DB('../data/', create_if_missing=True)
    orgdb.put(name.encode(), json.dumps(data).encode())
    orgdb.close()

def add_project(org, name, data):
    orgdb = plyvel.DB('../data/', create_if_missing=True)
    projdb = orgdb.prefixed_db(org.encode())
    projdb.put(name.encode(), json.dumps(data).encode())
    orgdb.close()

def add_issues(org, project, issues):
    orgdb = plyvel.DB('../data/', create_if_missing=True)
    projdb = orgdb.prefixed_db(org.encode())
    issuedb = projdb.prefixed_db(("%s-issues" % project).encode())
    batch = issuedb.write_batch()
    for issue in issues:
        data = vars(issue)['_rawData']
        batch.put(str(issue.number).encode(), json.dumps(data).encode())
    batch.write()
    orgdb.close()

def add_prs(org, project, prs):
    orgdb = plyvel.DB('../data/', create_if_missing=True)
    projdb = orgdb.prefixed_db(org.encode())
    prsdb = projdb.prefixed_db(("%s-prs" % project).encode())
    batch = prsdb.write_batch()
    for pr in prs:
        data = vars(pr)['_rawData']
        batch.put(str(pr.number).encode(),
        json.dumps(data).encode())
    batch.write()
    orgdb.close()
