import json

from datetime import datetime, timedelta
from github import Github
from pprint import pprint

if __name__ == '__main__':
    global git
    with open('app.json') as raw:
        data = json.loads(raw.read())
        git = Github(data['githubAccessToken'])
    raw.close()

    # Replicate zalando.github.io
    for org in data['organizations']:
        metrics = {}
        languages = []
        totals = [0, 0, 0]
        for project in git.get_organization(org).get_repos():
            language = project.language
            forks    = project.forks_count
            stars    = project.stargazers_count
            #team     = project.get_collaborators().totalCount
            metrics[project.name] = [language, forks, stars]
    
            # Gather total metrics
            if language is not None:
                if language not in languages: 
                    languages.append(language)
            totals[0] += forks
            totals[1] += stars
            totals[2] += 1

        # Print the result
        print("%s - Stars: %s, Repositories: %s, Languages: %s" %
              (org, totals[1], totals[2], len(languages)))
