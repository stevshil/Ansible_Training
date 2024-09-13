# Follow the instructions to build a database server

In this scripted exercise you will build a MySQL (MariaDB) database server on your other host.

## Create a new playbook

In the lecture session you created a playbook for the webservers.  Now we want to create a playbook called **databases.yml**.

In this file we will need to target the **databases** host group in our inventory.ini file.  Let's add a name of our playbook and a hosts section to target that host group.

```yaml
- name: Manage MySQL database servers
  hosts: databases
```

We should also add some variables that can be overridden at run time, but provide defaults for development.

```yaml
  vars:
    sauser: root
    sapass: secret123
    dbuser: devuser
    dbpass: secret123
  
  tasks:
```

Here we have created 2 variables for the database user and password.

## Adding the tasks

Now we will install the database and configure it so that we can log on from a remote server as root.

Before we install any system we would need to know what the instructions are to actually perform the installation, so we would got through the manual process so we know what packages and files are required.

For MariaDB we require the following:

Packages:

* mariadb-server
  * The actual database server package
* mariadb-client
  * Allows us to check that the server is configured correctly
  * On a real server we would not normally require this

Ansible modules:

From https://docs.ansible.com/ansible/latest/collections/community/mysql/index.html

* mysql_user
  * Requires PyMySQL (apt package python3-pymysql)
* mysql_query
  * Allows us to run ad-hoc SQL commands

### If building on Ubuntu/Debian

If you're building on a Debian derived system such as Ubuntu or Mint you will need to ensure your package cache is up to date.  This would be the equivalent of running the **apt update** command, which is not required on RHEL (Red Hat Enterpirse Linux) systems.

```yaml
    - name: Update apt cache
      apt:
        update_cache: true
```

### Installing the packages

```yaml
    - name: Install MariaDB package
        package:
          name:
            - mariadb-server
            - mariadb-client
            - python3-pymysql
```

The above packages are for installing MariaDB onto a Debian based server, and the Python package is to enable Ansible modules to work that we will need.

On a RHEL based server you will change the packages as follows:

* mariadb-client = mysql
* python3-pymysql = python3-PyMySQL

### Configuring the users

Let's take a look at updating the server so that the root user can log in from a remote host.  This we would not normally do on a production level system, but for the training we'll demonstrate it.

```yaml
    - name: Add remote root user
      community.mysql.mysql_user:
        check_implicit_admin: yes
        login_unix_socket: "/run/mysqld/mysqld.sock"
        login_user: root
        login_password: ""
        name: "{{ sauser }}"
        host: "%"
        password: "{{ sapass }}"
        encrypted: false
        priv: '*.*:ALL'
        state: present
```

There are some essential attributes we need to ensure that we use the local **root** account for MariaDB which has no password.  The attributes that ensure Ansible uses this account are:

* check_implicit_admin
* login_unix_socket
* login_user
* login_password

Most of the other attributes are self explanatory, but here are some essentials:

* host: "%"
  * This defines that the root account we are creating can log in from any where
  * MySQL syntax uses the SQL wildcard % for this purpose
* encrypted: false
  * States that we have used a non-encrypted password
  * This is where features such as Ansible Vault will come in handy, more later
* priv: "*.*:ALL"
  * Defines which databases and tables the user will have access to

The **devuser** is as follows:

```yaml
    - name: Add remote devuser
      community.mysql.mysql_user:
        check_implicit_admin: yes
        login_unix_socket: "/run/mysqld/mysqld.sock"
        login_user: root
        login_password: ""
        name: "{{ dbuser }}"
        password: "{{ dbpass }}"
        host: "%"
        encrypted: false
        priv: "*.*:ALL"
        state: present
```

### Making the database available on all networks

By default MariaDB will run on localhost, so to enable external access we need to update the files in /etc/my.cnf.

```yaml
    - name: Change Mariadb to run from any IP
      ansible.builtin.lineinfile:
        path: /etc/mysql/mariadb.conf.d/50-server.cnf
        regexp: "^bind-address.*="
        line: bind-address = 0.0.0.0
      notify:
        - Restart DB


  handlers:
    - name: Restart DB
      service:
        name: mariadb
        state: restarted
```

For Ubuntu the file **/etc/mysql/mariadb.conf.d/50-server.cnf** has to be modified to change the **bind-address**.  For this we use the **lineinfile** module to change the content of that line.  You'll also notice that we include and **notify** to restart the database server process after this change.

For RHEL system MariaDB will automatically start on all network interfaces.  If you did need to modify the attributes, or add the entry to the file you would be using **/etc/my.cnf** as the **path**.

# Check before running

Before running the playbook, check the linting and that it will work.

Let's do a full lint check first:

```sh
ansible-lint -f full databases.yml
```

The first change is that we used the **apt** module, rather than the full **ansible.builtin.apt**.

The same change is required for **package** module, as the short notation is used.  Change **package** to **ansible.builtin.package**.

The **check_implicit_admin** attribute states a **truthy** variable.  We have used **yes**, when Ansible prefers **true**.

Our **service** is also using the shortname, so we need to change that to **ansible.builtin.service**.

Now that we have fixed the lint issues, let's check that the playbook would run without other issues.

```sh
ansible-playbook --check --diff databases.yml
```

**NOTE:** Due to the requirement of MariaDB, the check will fail since the **mysql** modules will need the database to be running to perform the check.

Luckily for us Ansible is idempotent, so we can run the playbook.  If there are failures we can fix them and run the playbook.

**NOTE:** We should always test our playbooks against an empty system to prove it works.  The reason behind this is that sometimes we don't spot issues if we have a partial build that we continue to build on.