import db
import json

from github import Github
from pprint import pprint

if __name__ == '__main__':
    global git
    with open('app.json') as raw:
        data = json.loads(raw.read())
        git = Github(data['githubAccessToken'])
    raw.close()

    # Full sync of the org data
    for org in data['organizations']:
        # General data
        orgobj = git.get_organization(org)
        db.add_organization(org, vars(orgobj)['_rawData'])

        # Now the projects
        for project in orgobj.get_repos(type='all'):
            db.add_project(org, project.name, vars(project)['_rawData'])
        
