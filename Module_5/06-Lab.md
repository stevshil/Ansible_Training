# Your turn

In this lab we want you to turn your Ansible controller into a Jenkins server.  By doing this we can then make our Ansible controller a CI/CD server for Ansible and control the running of playbooks when the Git repository containing the playbooks is updated.

For the time being we just want to install Jenkins and make sure we can access it.

Use Ansible Galaxy to do the installation, and work in the **oursite** directory to perform the provisioning.

You will need:

1. An Ansible playbook to install Jenkins
    * Geerlingguy is normally good
2. Identify variables to set
    * Check the documentation
    * Don't forget that the defaults are normally shown
    * Only set variables in the **group_vars** directory that you want to change
      * jenkins_admin_password
      * jenkins_plugins
        * git
        * workflow-aggregator
        * dashboard-view
        * cloudbees-folder
        * pipeline-utility-steps
        * ansible
      * jenkins_plugins_install_dependencies: true
      * jenkins_plugins_state: present
3. You will also need to install Java
    * The role also shows you this, and that you'll need the geerlingguy.java role
    * OpenJDK will need to be 11 or higher


## Optional

If you have time either:

* Create your own role to install NGINX web server
  * Install so that it is on port 81 as Apache will be on 80
  * Install the role on the webservers group
* Use an Ansible Galaxy role
  * Ensure it allows you to set the port number