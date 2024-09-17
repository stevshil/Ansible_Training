# Ansible Galaxy

Imagine if there was a bunch of developers out there who were writing Ansible roles that would provision anything we wanted, and all we have to do is to import the role and supply the variables.

Well, this is what Ansible Galaxy is all about.

When using Galaxy we normally install the roles onto the **controller**.  You can also do it for your development server.  When you install the roles with Galaxy they are installed to a specific location, rather than under your roles directory.  You can specify that the module is installed in your Roles directory, but we normally only place our own developed roles in there.

When roles are installed, Ansible will look for the roles in the following locations:

* $HOME/.ansible/roles
* /usr/share/ansible/roles
* /etc/ansible/roles

In most instances $HOME/.ansible/roles would be where the roles are installed, especially when using an controller, or CI/CD server.

* https://docs.ansible.com/ansible/latest/galaxy/user_guide.html

Roles not installed by Galaxy, but through Git would be placed in your Roles directory.

## Searching for roles

You can search for Ansible roles at [https://galaxy.ansible.com/ui/](https://galaxy.ansible.com/ui/).

Let's look for a module to install **mariadb** database, or **mysql**.

Click on Roles, then Roles again.

In the search type **mariadb** and press enter.

Change **Created** drop down to **Download count**.

If you click on **bertvv.mariadb** it will tell you how to install, documentation and normally a link to the GitHub site.  You'll see in this documentation we are told the variables.

**NOTE: ** Sadly this role is for RHEL only.

If we go back and select **lukasic.mariadb**, this claims to be for Debian.

When using roles you will normally just provide variable overrides in your **vars** directory, and then specify the **role name** in the playbook for the section that will be using it.

If we cannot find the variables in the documentation for the role, then we can go to the GitHub repository.

**NOTE:** You should install the Galaxy roles as the user that runs the playbooks, so that they are installed into the correct location.

## Using the role

Instead of creating a database role, let's use **bertvv.mariadb** role for managing our database.

1. On the controller run the command to install the role
    ```sh
    $ ansible-galaxy install lukasic.mariadb

    Starting galaxy role install process
   - downloading role 'mariadb', owned by lukasic
   - downloading role from https://github.com/lukasic/ansible-role-mariadb/archive/1.1.0.tar.gz
   - extracting lukasic.mariadb to /home/ansible/.ansible/roles/lukasic.mariadb
   - lukasic.mariadb (1.1.0) was installed successfully
    ```

    You should see something similar to the above if it installs successfully, and you'll notice it tells you the directory it was installed to.

2. Now we can create our **vars** for the **databases** **group_vars**.
    * Change directory into ~/oursite/environments/dev/group_vars
    * Create the file **databases.yml**
3. The content for the **databases.yml** file will be as follows, taken from the documentation page of the role:
    ```yaml
    mariadb_server_params:
      - option: bind_address
        value: 0.0.0.0
        section: mysqld
    mariadb_users:
      - name: devuser
        password: secret123
        priv: '*.*:ALL'
        host: '%'
      - name: root
        password: secret123
        priv: '*.*:ALL'
        host: '%'
    ```
4. Save the file.

That's it we've just configured our role.

The only other code we need to change is our **site.yml**, so that the **databases** all use the **lukasic.mariadb** role.

Edit the **~/oursite/site.yml** file, currently:

```yaml
- name: Web Servers
  hosts: webservers

  roles:
    - apache
```

Add a new section after the **apache** role, so that the file looks as follows:

```yaml
- name: Web Servers
  hosts: webservers

  roles:
    - apache

- name: Database Servers
  hosts: databases

  roles:
    - lukasic.mariadb
```

Now we just run the playbook.

```sh
ansible-playbook -i environments/dev site.yml
```

The system will update, but now we have the use of someone elses role.

## Managing Galaxy roles

You should treat Galaxy roles just like any other software, pinning the version so that you code does not break.

From the command line you can use:

```sh
ansible-galaxy install lukasic.mariadb,11.0
```

Here you can see the version placed after the role and a comma.

To manage our server in a DevOps way, we should version control our Ansible Galaxy roles by having a **requirements.txt** or **requirements.yml** file.  If you're familiar with Python, you'll realise where this name comes from.

In the **requirements.yml** file you would supply the name of the role and the version for all the modules you require.

### Example requirements.yaml

```yaml
- name: lukasic.mariadb
  version: 1.1.0
```

If we now had to rebuild our controller or CI/CD server we can simply reload all of our modules to the correct version as follows:

```sh
ansible-galaxy install -r requirements.yml
```

Our **requirements.yml** file would be under version contol, and a method in place to update this on the controller.

# Summary

It can be tricky sometimes using other peoples roles, but it can make development easier and quicker if you find a good module developer.

You will have to do some reading and trial and error to see if the module covers what you need.

If the module does not cover everything, then you only need to implement the extra parts as a role that you create and add that to the **site.yml** playbook for that specific host group under the **roles** section, which as we showed earlier is a list.

Remember to version control your roles by keeping a **requirements.yml** file in version control and installing or upgrading your modules from this file.