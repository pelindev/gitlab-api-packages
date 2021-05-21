import requests
import json
import config


headers = {'PRIVATE-TOKEN': config.mainToken}
createProjectUrl = '{}/projects'.format(config.url)
createGroupUrl = '{}/groups'.format(config.url)

# Getting group id from search results
listOfGroups = requests.get(createGroupUrl + '?search=' + config.groupName, headers = headers) # get group info
for group in json.loads(listOfGroups.text):
    if group["name"] == config.groupName:
        groupId = group["id"]
        break

# Getting npm project id from search results
listOfProjects = requests.get(createProjectUrl + '?search=' + config.npmProject, headers = headers) # get projects info
for project in json.loads(listOfProjects.text):
    if project["name"] == config.npmProject:
        npmProjectId = project["id"]
        break

# Getting composer project id from search results
listOfProjects = requests.get(createProjectUrl + '?search=' + config.composerProject, headers = headers) # get projects info
for project in json.loads(listOfProjects.text):
    if project["name"] == config.composerProject:
        composerProjectId = project["id"]
        break

# Delete npm tokens
listNpmTokens = requests.get('{}/projects/{}/deploy_tokens'.format(config.url, npmProjectId), headers = headers)
for token in json.loads(listNpmTokens.text):
    if token["name"] == 'project_npm_token':
        requests.delete('{}/projects/{}/deploy_tokens/{}'.format(config.url, npmProjectId, token["id"]), headers = headers)
        print('npm token is deleted')

# Delete group tokens
listGroupTokens = requests.get('{}/groups/{}/deploy_tokens'.format(config.url, groupId), headers = headers)
for token in json.loads(listGroupTokens.text):
    if token["name"] == 'group_npm_token':
        requests.delete('{}/groups/{}/deploy_tokens/{}'.format(config.url, groupId, token["id"]), headers = headers)
        print('Group token is deleted')

# Find user id
listUsersUrl = '{}/users'.format(config.url)
listOfUsers = requests.get(listUsersUrl + '?search=' + config.user, headers=headers)  # get users info

for user in json.loads(listOfUsers.text):
    if user["username"] == config.user:
        userId = user["id"]
        break

# Delete composer tokens
tokenData = { 'user_id': userId }
listComposerTokens = requests.get('{}/personal_access_tokens'.format(config.url, composerProjectId), data = tokenData, headers = headers)
for token in json.loads(listComposerTokens.text):
    if token["name"] == 'project_composer_token' and not token['revoked']:
        requests.delete('{}/personal_access_tokens/{}'.format(config.url, token["id"]), headers = headers)
        print('Composer token is deleted')
