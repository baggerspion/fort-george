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

    # Do a complete sync of all metadata
    for org in data['organizations']:
        print("# Organisation: %s" % org)
        orgobj = git.get_organization(org)
        db.add_organization(org, vars(orgobj)['_rawData'])

        for project in orgobj.get_repos(type='all'):
            print("## Project: %s" % project.name)
            db.add_project(org, project.name, vars(project)['_rawData'])

            # Add all the project data
            db.add_branches(project.name, project.get_branches()) 
            db.add_collaborators(project.name, project.get_collaborators())
            db.add_commits(project.name, project.get_commits())
            db.add_contributors(project.name, project.get_contributors())
            db.add_issues(project.name, project.get_issues())
            db.add_languages(project.name, project.get_languages())
            db.add_prs(project.name, project.get_pulls())
            db.add_stars(project.name, project.get_stargazers())

            # Stats
            ## Contributors
            ## Commit Activity
            ## Code Frequency
            ## Participation
            ## Punch Card
