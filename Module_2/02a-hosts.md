# Hosts configuration (Inventory)

Now you've worked with modules and learned how attributes work, let's do the same, but as orchestration of an environment of systems.

## Ansible inventory and configuration

Ansible allows for inventory files and configuration files to be stored in various locations.  The locations are as follows;

* System wide
  * /etc/ansible
  * Files include
    * hosts
      * This is the ansible inventory file, more later
    * ansible.cfg
      * Global settings for the Ansible commands, more later
        * Includes where to find inventory and role directories and more.
* Users home directory
* Directory where you run the **ansible** commands
  * Current directory normally, which would be your Ansible project.

In DevOps tradition we will work with both the inventory and configuration files as though they are part of the project, so the same directory as all of the files we will create that will manage our infrastructure.

## Before we begin we will need an inventory

Log on to your Ansible Controller.

First we need an inventory file so that our Ansible Controller can connect and know how.

Create a file called **~/inventory.ini** as follows;

```
nano ~/inventory.ini
```

In the file add the following lines;

```
[controller]
controller ansible_host=localhost ansible_connection=local  ansible_become=true

[nodes]
node1 ansible_host=192.168.1.2 ansible_user=ansible ansible_become=true ansible_ssh_private_key_file=~/.ssh/ansible
node2 ansible_host=192.168.1.3 ansible_user=ansible ansible_become=true ansible_ssh_private_key_file=~/.ssh/ansible

[all:vars]
ansible_ssh_common_args='-o StrictHostKeyChecking=no'
```

As this is an ini file each group of hosts is sectioned using the square brackets.  Here we have to host groups, controller and nodes.

You'll notice how we've laid out the file;
* The first column is the alias name for the host when used with ansible commands
  * This column can also be the DNS name of the host
* The subsequent columns must be key=value pairs of information.
  * ansible_host allows us to specify an IP address or hostname if we wish to use aliases
  * ansible_ssh_private_key_file allows us to override the default SSH private key file

You'll also notice the
```[all:vars]```
section, which allows us to add Ansible variables that will apply to all hosts.

We could therefore rewrite our inventory as follows, since we have repeated variables;

```
[controller]
controller ansible_host=localhost ansible_connection=local

[nodes]
node1 ansible_host=192.168.1.2
node2 ansible_host=192.168.1.3

[all:vars]
ansible_ssh_common_args='-o StrictHostKeyChecking=no'
ansible_become=true 

[nodes:vars]
ansible_user=ansible
ansible_ssh_private_key_file=~/.ssh/ansible
```

See [https://docs.ansible.com/ansible/latest/inventory_guide/intro_inventory.html](https://docs.ansible.com/ansible/latest/inventory_guide/intro_inventory.html) for more details on attributes you can specify in the host file.

## Remote examples

### Get the facts from node1;

```bash
ansible node1 -i inventory.ini -m setup
```

This command targets the Ansible host **node1** within the inventory.ini file we created under the **nodes** section.  The first column of the inventory file is the Ansible node alias.

### Get the facts from all nodes;

```bash
ansible nodes -i inventory.ini -m setup
```

The above command now targets both nodes under our **nodes** section in the inventory file.  The command will now run on both node1 and node2.

### Target all hosts in inventory;

```bash
ansible all -i inventory.ini -m setup
```

The word **all** is a reserved word that Ansible uses to target all hosts listed in the inventory file.

### Pinging your hosts

We can change the module to run as we saw in the previous modules.  Here we can simply ping all the hosts.

```bash
ansible nodes -i inventory.ini -m ping
```

### Creating a file

As in the previous modules we used **lineinfile** to create a file on the host we were on, we can now create the file on the remote servers using the inventory file as follows;

```bash
ansible nodes -i inventory.ini -m lineinfile -a "create=true line='Hello World' mode=500 path=/tmp/hello_world"
```

The output from the above command;

```bash
node1 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "backup": "",
    "changed": true,
    "msg": "line added and ownership, perms or SE linux context changed"
}
node2 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/libexec/platform-python"
    },
    "backup": "",
    "changed": true,
    "msg": "line added and ownership, perms or SE linux context changed"
}
```

If the host already has the file and there is no change you would see the following output;

```bash
node1 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "backup": "",
    "changed": false,
    "msg": ""
}
```

### Host is not reachable

If a host is not on or misconfigured in the inventory your will see **UNREACHABLE!** against the host.

```bash
node1 | CHANGED => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "backup": "",
    "changed": true,
    "msg": "line added and ownership, perms or SE linux context changed"
}
node2 | UNREACHABLE! => {
    "changed": false,
    "msg": "Failed to connect to the host via ssh: ssh: connect to host 192.168.1.222 port 22: Connection timed out",
    "unreachable": true
}
```

## Attributes with multiple values

Using the **filter** attribute to select 2 attributes;

```bash
ansible node1 -i inventory.ini -m setup -a '{"filter":["ansible_distribution","ansible_os_family"]}'
```

When you have an attribute that allows for multiple values we need to use { } to encapsulate the attribute and then we use [ ] to allow for an array of attributes.

## Multiple attributes

We can also add multiple attributes to our ad-hoc commands;

```bash
ansible nodes -i inventory.ini -m setup -a '{"filter":["ansible_distribution","ansible_os_family"]}' -a '{"gather_timeout":10}'
```

Rebooting a host;

```bash
ansible nodes -i inventory.ini -m reboot -a '{"reboot_timeout":0}' -a '{"msg":"Shutting down now"}'
```

&#x26a0;&#xfe0f; **NOTE:** You cannot shut down your control node using the **ansible** command line.


# Example configuration file

We could create a file called **ansible.cfg** in the directory where we plan to run our Ansible commands, and where we locate our inventory file.

An example of a parallel execution Ansible configuration file would be as follows;

```
[defaults]
retry_files_enabled = False
timeout = 60
connection = smart
interpreter_python = auto
forks = 10
inventory = inventory.ini
# roles_path = project/roles:/usr/share/ansible/roles
remote_user = ansible
host_key_checking = False
command_warnings = False
deprecation_warnings = False
```

In the above we can see that we have set many parameters.  Some of the notable ones are;

* connection = smart
  * Determine if we are to use local or ssh, etc to connect to the target node
* interpreter_python = auto
  * Determine the python interpreter path and version to run ansible commands
* forks = 10
  * Run modules/commands on up to 10 nodes in parallel, rather than 1 at a time

# Simple module

We have already seen an example of running a module earlier with;

* setup
* ping
* lineinfile
* reboot

You'll notice that the **-m** option to the **ansible** command is followed by the module name as the argument.

An example of installing **cowsay** package onto the nodes;

```
ansible nodes -i inventory.ini -m ansible.builtin.package -a "name=cowsay state=present" --become --become-user=root
```

In the above command we use the full path to the **package** module **ansible.builtin/package**.  In most instances you can use just **package**, but since version 2.6 you can use the full path.

You will also noticed that we've added the **--become** and **--become-user=root** to ensure that the command completes successfully, as installing software requries **root** privileges.

**NOTE** that cowsay might not install on the RHEL based servers.