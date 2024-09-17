# Final Practical

A build it yourself environment.
We’ll destroy the current set of servers and rebuild as follows;
	- Ansible controller with Jenkins to automate build
	- Jenkins to poll git repo for changes and execute ansible-playbook
	- Ansible playbook to install simple Python API service with database backend or Java SpringBoot CD API
	- Make changes through code and push to git
	- Jenkins does the rest