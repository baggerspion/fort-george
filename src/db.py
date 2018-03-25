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

def add_commits(org, project, commits):
    orgdb = plyvel.DB('../data/', create_if_missing=True)
    projdb = orgdb.prefixed_db(org.encode()) 
    commitsdb = projdb.prefixed_db(("%s-commits" % project).encode())
    batch = commitsdb.write_batch()
    for commit in commits:
        data = vars(commit)['_rawData']     
        batch.put(str(commit.sha).encode(), json.dumps(data).encode())
    batch.write()
    orgdb.close()
