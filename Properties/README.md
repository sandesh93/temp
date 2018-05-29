
Synopsis:

This script will deploy fresh eCatalog depending on the build version.
This will pull build from nexus repo and all the configuration from git and deploy in the given environment as target
the name of releasable (being uploaded) should be "builds.zip"

Requirements

User: webtech
OS: Centos6
App: Ansible


External parameters needs to be given to ansible script:

- git_tag


Dependencies:

None


Point to note:

"maven_artifact" module has dependency on "python-lxml" (which has dependency on python-2.7), hence we are pulling nexus repo on the ansible server 1st and then copying it to remote location.