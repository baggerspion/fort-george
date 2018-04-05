import json
import plyvel
import pprint

def add_organization(name, data):
    orgdb = plyvel.DB('../data/orgs/', create_if_missing=True)
    orgdb.put(name.encode(), json.dumps(data).encode())
    orgdb.close()

def add_project(org, name, data):
    projdb = plyvel.DB('../data/projects/', create_if_missing=True)
    part = projdb.prefixed_db(org.encode())
    part.put(name.encode(), json.dumps(data).encode())
    projdb.close()

def add_branches(org, project, data):
    print("- Branches")
    branchdb = plyvel.DB('../data/branches/', create_if_missing=True)
    orgs = branchdb.prefixed_db(org.encode())
    part = orgs.prefixed_db(project.encode())
    wb = part.write_batch()
    for branch in data:
        content = vars(branch)['_rawData']
        wb.put(branch.name.encode(), json.dumps(content).encode())
    wb.write()
    branchdb.close()

def add_collaborators(org, project, data):
    print("- Collaborators")
    collabdb = plyvel.DB('../data/collaborators/', create_if_missing=True)
    orgs = collabdb.prefixed_db(org.encode())
    part = orgs.prefixed_db(project.encode())
    wb = part.write_batch()
    for collaborator in data:
        content = vars(collaborator)['_rawData']
        wb.put(str(collaborator.id).encode(), json.dumps(content).encode())
    wb.write()
    collabdb.close()

def add_commits(org, project, data):
    print("- Commits")
    commitdb = plyvel.DB('../data/commits/', create_if_missing=True)
    orgs = commitdb.prefixed_db(org.encode())
    part = orgs.prefixed_db(project.encode())
    wb = part.write_batch()
    for commit in data:
        content = vars(commit)['_rawData']
        wb.put(str(content['commit']['author']['date']).encode(), json.dumps(content).encode())
    wb.write()
    commitdb.close()

def add_contributors(org, project, data):
    print("- Contributors")
    contribdb = plyvel.DB('../data/contributors/', create_if_missing=True)
    orgs = contribdb.prefixed_db(org.encode())
    part = orgs.prefixed_db(project.encode())
    wb = part.write_batch()
    for contributor in data:
        content = vars(contributor)['_rawData']
        wb.put(str(contributor.id).encode(),json.dumps(content).encode())
    wb.write()
    contribdb.close()

def add_issues(org, project, data):
    print("- Issues")
    issuesdb = plyvel.DB('../data/issues/', create_if_missing=True)
    orgs = issuesdb.prefixed_db(org.encode())
    part = orgs.prefixed_db(project.encode())
    wb = part.write_batch()
    for issue in data:
        content = vars(issue)['_rawData']
        wb.put(str(issue.id).encode(),json.dumps(content).encode())
    wb.write()
    issuesdb.close()

def add_languages(project, data):
    print("- Languages")
    langsdb = plyvel.DB('../data/languages/', create_if_missing=True)
    langsdb.put(project.encode(), json.dumps(data).encode())
    langsdb.close()

def add_prs(project, data):
    print("- PRs")
    pullsdb = plyvel.DB('../data/prs/', create_if_missing=True)
    orgs = pullsdb.prefixed_db(org.encode())
    part = orgs.prefixed_db(project.encode())
    wb = part.write_batch()
    for pr in data:
        content = vars(pr)['_rawData']
        wb.put(str(pr.id).encode(),json.dumps(content).encode())
    wb.write()
    pullsdb.close()

def add_stars(project, data):
    print("- Stars")
    starsdb = plyvel.DB('../data/stars/', create_if_missing=True)
    part = starsdb.prefixed_db(project.encode())
    wb = part.write_batch()
    for star in data:
        content = vars(star)['_rawData']
        wb.put(str(star.id).encode(),json.dumps(content).encode())
    wb.write()
    starsdb.close()
