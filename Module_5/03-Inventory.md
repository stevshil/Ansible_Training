# Inventory as a directory

We can now move away from our **inventory.ini** file and create our site as a set of directories, including environments, and setting variables based on specific environments.

A site allows us to fully manage our systems as code, and to look after different environments.

In DevOps we use **environments** so that we can test out new changes to code and configurations first, before applying them to production.  This in turn allows us to create automated pipelines using tools such as Jenkins or GitHub Actions to automate the process of build and test, once we push our code.

In the previous section we copied down the **inventory.ini** so that we could run our webserver role using the **test-apache.yml** playbook.

Let's break our **inventory** into a site structure.

The following is a reference on the different methods creating inventory:

* https://docs.ansible.com/ansible/latest/inventory_guide/intro_inventory.html
* https://docs.ansible.com/ansible/latest/tips_tricks/sample_setup.html#sample-setup

We will be using the directory method here.

We should be in **oursite** directory, where we will see the following files and directories:

```sh
$ cd ~/oursite
$ ls
inventory.ini  roles  test-apache.yml
```

Let's create a directory called **environments** and inside this directory we will create **dev**, **uat** and **prod**, even though we will only be using **dev**.

```sh
mkdir -p environments/{dev,uat,prod}
```

The above command handles the creation of the subdirectories under **environments**.

## Directory layout

A directory layout can be found at https://docs.ansible.com/ansible/latest/tips_tricks/sample_setup.html#sample-setup

For ours we will be creating the following:

```
environments/
  dev
    hosts  # Files containing the hosts and groups, similar to the inventory.ini or in yaml
    group_vars
      all.yml
      databases.yml  # Variables specific to the group of hosts under databases
    host_vars
      web01.yml  # Variables specific to the host web01
  prod
    hosts
    group_vars
    host_vars
  uat
    hosts
    group_vars
    host_vars
```

We will focus on **dev** for our current environment, but the idea is you can set different inventory files and variables for each environment you wish to manage.  In this case the **hosts** file has to be called **hosts** as Ansible processes a directory as the inventory, and the default file name for an inventory is **hosts**.  In the group_vars and host_vars directories we create filenames based on the group or Ansible hostname.  The **yml** extension is not required.

## Building our Dev environment

Let's now change our **inventory.ini** file into the directory structure for an environment definition.

Our current **ini** file:

```ini
[controller]
controller ansible_host=10.0.1.1 ansible_connection=local os=ubuntu

[webservers]
web01 ansible_host=10.0.1.2 ansible_user=ansible ansible_ssh_private_key_file=~/.ssh/ansible os=rhel ansible_become=true ansible_become_user=root

[databases]
db01 ansible_host=10.0.1.3 ansible_user=ansible ansible_ssh_private_key_file=~/.ssh/ansible os=ubuntu ansible_become=true ansible_become_user=root

[all:vars]
# ansible_ssh_common_args='-o StrictHostKeyChecking=no'
environment=production
```

Change directory to **environments/dev**.

Create the file called **hosts** and add the following content.

```ini
[controllers]
controller ansible_host=10.0.1.1 ansible_connection=local

[webservers]
web01 ansible_host=10.0.1.2

[databases]
db01 ansible_host=10.0.1.3
```

Now we wish to associate the other attributes to the webservers and databases.  Since the majority are the same we will put the following into a **group_vars** file called **all**.

From the original file:

```ini
ansible_user=ansible ansible_ssh_private_key_file=~/.ssh/ansible ansible_become=true ansible_become_user=root
```

All of the above attributes can be placed in the file as follows:

1. Create the **group_vars** directory
   ```sh
   mkdir group_vars
   ```
2. Add the following content to **group_vars/all.yml**, but note how we change the **=** to **:** since we are working with YAML:
    ```yaml
    ansible_user: ansible
    ansible_ssh_private_key_file: ~/.ssh/ansible
    ansible_become: true
    ansible_become_user: root
    ```

We also have variables relating to each host, in this case our **os** variable, which we will place into the **host_vars** directory, where each file will be named after the Ansible hostname.

1. Create the **host_vars** directory.
    ```sh
    mkdir host_vars
    ```
2. Create the file **host_vars/web01.yml** and in that file add:
    ```yaml
    os: rhel
    ```
    Save the file and exit
3. Create the file **host_vars/db01.yml** and add the following to that file:
    ```yaml
    os: ubuntu
    ```

We have now created our inventory in a directory structure.  We can now delete our **inventory.ini** file in the root of **oursite** directory.

```sh
$ cd ~/oursite
$ rm inventory.ini
```

We can again run our **test-apache.yml** playbook as follows:

```sh
$ ansible-playbook -i environments/dev test-apache.yml
```

The playbook will run and provision as normal, but remember our server is already provisioned, so it should run through without error or changes.

Since we haven't created **prod** yet try running the playbook using the **prod** environment, by changing the directory from **dev** to **prod**.

You'll be told no hosts match.

To add more roles and features we simply add roles to the roles directory and then create the playbook to run the roles against the relevant hosts.

Ideally we would now rename our **test-apache.yml** file to **site.yml**, since we know that we want the role to be applied to that server.

```sh
mv test-apache.yml site.yml
```

Let's say we add a database role to our **roles** directory.  In the **site.yml** playbook we would change it by adding another **hosts** section and roles:

```yaml
- name: Web servers
  hosts: webservers

  roles:
    - apache

- name: Database servers
  hosts: databases

  roles:
    - database
```

You'll notice how each section is divided by the name of the hosts to manage, and the **hosts** section defines which hosts will be provisioned.

It is possible for a host section to contain more than one role, e.g.:

```yaml
- name: Database servers
  hosts: databases

  roles:
    - generic
    - database
    - security
```

Now that we know the structure of a site and how simpler our playbooks now look we can focus on the roles.