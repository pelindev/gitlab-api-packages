import requests
import json
import config

def main():
    headers = {'PRIVATE-TOKEN': config.mainToken}
    createProjectUrl = '{}/projects'.format(config.url)
    publishNpmrc = "@root:registry={}://{}\n//{}:_authToken={}\n"
    createGroupData = {'name': config.groupName, 'path': config.groupName}
    createGroupUrl = '{}/groups'.format(config.url)
    projectComposerData = {'name': config.composerProject}


    def getToken(self):
        jsonData = self.text
        jsonData = json.loads(jsonData)
        return jsonData["token"]


    requests.post(createGroupUrl, data=createGroupData, headers=headers)
    requests.post(createGroupUrl, data=projectComposerData, headers=headers)

    # Getting group id from search results
    listOfGroups = requests.get(createGroupUrl + '?search=' + config.groupName, headers=headers)  # get group info
    for group in json.loads(listOfGroups.text):
        if group["name"] == config.groupName:
            groupId = group["id"]
            break

    # Creating npm project
    projectNpmData = {'name': config.npmProject, 'namespace_id': groupId}
    requests.post(createProjectUrl, data=projectNpmData, headers=headers)

    # Getting npm project id from search results
    listOfProjects = requests.get(createProjectUrl + '?search=' + config.npmProject, headers=headers)  # get projects info

    for project in json.loads(listOfProjects.text):
        if project["name"] == config.npmProject:
            npmProjectId = project["id"]
            break

    # Creating composer project
    projectComposerData = {'name': config.composerProject, 'namespace_id': groupId}
    requests.post(createProjectUrl, data=projectComposerData, headers=headers)

    # Getting composer project id from search results
    listOfProjects = requests.get(createProjectUrl + '?search=' + config.composerProject, headers=headers)  # get users info

    for project in json.loads(listOfProjects.text):
        if project["name"] == config.composerProject:
            composerProjectId = project["id"]
            break


    createNpmProjectTokenUrl = '{}/projects/{}/deploy_tokens/'.format(config.url, npmProjectId)

    createGroupTokenUrl = '{}/groups/{}/deploy_tokens/'.format(config.url, groupId)


    # Project token
    tokenData = {'name': 'project_npm_token', 'scopes[]': 'read_package_registry'}
    response = requests.post(createNpmProjectTokenUrl, data=tokenData,
                            headers=headers)
    projectToken = getToken(response)

    # Group token
    tokenData = {'name': 'group_npm_token', 'scopes[]': 'read_package_registry'}
    response = requests.post(createGroupTokenUrl, data=tokenData, headers=headers)
    groupToken = getToken(response)

    # Find user id
    listUsersUrl = '{}/users'.format(config.url)
    listOfUsers = requests.get(listUsersUrl + '?search=' + config.user, headers=headers)  # get projects info

    for user in json.loads(listOfUsers.text):
        if user["username"] == config.user:
            userId = user["id"]
            break


    # Composer token
    createComposerTokenUrl = '{}/users/{}/personal_access_tokens'.format(config.url, userId)
    tokenData = {'name': 'project_composer_token', 'scopes[]': 'read_api'}
    response = requests.post(createComposerTokenUrl, data=tokenData, headers=headers)
    composerToken = getToken(response)

    # Create package.json and .npmrc
    npmPackagesUrl = config.domain + '/api/v4/projects/{}/packages/npm/'.format(npmProjectId)
    packageJson = open('package.json', 'w')
    packageJson.write(config.exampleNpmPackage % (config.domain, npmPackagesUrl))
    npmrc = open('.npmrc', 'w')
    npmrc.write(publishNpmrc.format(config.proto, npmPackagesUrl, npmPackagesUrl, config.mainToken))

    print('New project deploy token: ' + projectToken)
    print('New group deploy token: ' + groupToken)
    print('New composer deploy token: ' + composerToken)
    print("""
Create .npmrc file in test project root with following data:
@root:registry={}://{}
//{}:_authToken={}""".format(config.proto, npmPackagesUrl, npmPackagesUrl, projectToken))

if __name__ == "__main__":
    main()
