import db
import json

from datetime import datetime
from github   import Github
from pprint   import pprint

if __name__ == '__main__':
    global git
    with open('app.json') as raw:
        data = json.loads(raw.read())
        git = Github(data['githubAccessToken'])
    raw.close()

    today = datetime.now().date()

    # Do a complete sync of all metadata
    for org in data['organizations']:
        print("# Organization: %s" % org)

        # Full sync of the org data
        orgobj = git.get_organization(org)
        db.add_organization(org, vars(orgobj)['_rawData'])

        # Full sync of the project data
        for project in orgobj.get_repos(type='all'):
            print("## Project: %s" % project.name)
            db.add_project(org, project.name, vars(project)['_rawData'])

            # Now we gather all the commits
            print("- Writing commits")
            db.add_commits(org, project.name, project.get_commits())
        
            # Now we gather all the issues
            print("- Writing issues")
            db.add_issues(org, project.name, project.get_issues())

            # Now we gather all the prs
            print("- Writing PRs")
            db.add_prs(org, project.name, project.get_pulls())
