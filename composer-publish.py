import requests
import json
import config
import create


headers = {'PRIVATE-TOKEN': config.mainToken}
createProjectUrl = '{}/projects'.format(config.url)
# Getting composer project id from search results
listOfProjects = requests.get(createProjectUrl + '?search=' + config.composerProject, headers=headers)  # get projects info

for project in json.loads(listOfProjects.text):
    if project["name"] == config.composerProject:
        composerProjectId = project["id"]
        break


url = '{}://__token__:{}@{}/api/v4/projects/{}/packages/composer'.format(config.proto, config.mainToken, config.domain, composerProjectId)
data = {'tag': 'v1.0.0'}


response = requests.post(url, data = data)
print(response.text)
