# Final Practical

## Do you have an idea?

Is there something you want to build, or work through?

If so talk with the instructor and use this as a starting point to help get your project moving.

## Create a decomission playbook

During this course we have mainly focused on provisioning our systems.

We should also have the ability to decomission the servers in the event we wish to repurpose them.

Write the roles and playbooks to decomission the servers.

## Deploying the Python API service

Create an Ansible playbook, if you haven't already to deploy and manage the API service in this repository on the Ansible controller.  The script does not come with a service file, so you may need to create one at this time.

## Add your own Ansible project to a git repo

Turn your **oursite** into a git repository and add it to Git.

Edit your code via VS Code or your favourite IDE and push your changes to the repository.

Git pull your changes to the Ansible controller and check that they work.

## Automating with Jenkins

If you haven't already use Ansible Galaxy to install Jenkins.

Add a Job/Task to Jenkins to manage your **oursite** Git repository and run the site.

### Optional Jenkins

If you have time and your Jenkins server is available on the Internet add a WebHook to Jenkins so that Git can trigger the job when you push to the git repository:

* https://www.blazemeter.com/blog/how-to-integrate-your-github-repository-to-your-jenkins-project


### Optional Firewall

Research the available modules in Ansible to see how you can manage firewall rules.

Add to your **oursite** project and configure the relevant access for the servers:

* Controller
  * Jenkins = 8080
  * SSH = 22
* Databases
  * MariaDB = 3306
  * SSH = 22
* Webservers
  * Apache = 80
  * SSH = 22
  * NGINX = 81

### Optional networking

Do a search for Ansible modules relating to routers.  You'll find that it refers to **network** modules.  Can you configure F5 routers?

Are there any Ansible modules already for working with InfoBlox?