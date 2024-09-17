# Variables follow the instructions

Here we will create an uninstall database server playbook, and then re-run our database playbook using different passwords by supplying the values on the command line using the **--extra-vars** option.

## Creating the uninstall playbook

Here we will get you to create the playbook to uninstall MariaDB.  We will provide the steps, but not the commands for this section.

1. Create a new YAML file called **uninstallDB.yaml** and in that file:
2. Set the name of the playbook
3. Set the hostgroup to **databases** so that we target only the database server
4. Add a tasks section
5. Add a name for a task called **Stop database**
6. Add the module called **systemd**
    * Using the Ansible **systemd** documentation write the attributes to stop the **mariadb** service
7. Add a name for the task called **Uninstall database**
    * Using the **package** module uninstall **mariadb-server**, **mariadb-client** and **python3-pymysql**
    * As part of the removal you should also consider **purging** and **autoremove**
8. Remove the data directory so that we can re-install without issues
    * To remove a directory you will need to look at the Ansible **file** module
    * Ansible can delete directories that contain files, so you **don't** have to delete all files first.
    * The directories to remove are:
      * /var/lib/mysql
      * /etc/mysql

Save the file, and run the playbook as normal:

```sh
ansible-playbook uninstallDB.yaml
```

Make sure your playbook returns successful, before continuing.

## Re-installing MariaDB using CLI variables

Now let's re-install our Ansible playbook for the **database**, but this time we'll change the password for the **devuser** from **secret123** to **mydb123secret**, and we'll change **root**'s password to **1mp0rt4nt** (that's important but a 1, zero and 4).

This requires you to run the playbook, but provide the 2 variable changes using the **--extra-args** and space separating the key=value pairs.