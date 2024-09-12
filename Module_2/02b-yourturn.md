# Your turn

This time, we're just going to drop you in it, as we've been using the commands, and this is more around the configuration and inventory.

We will continue to work with the inventory as we go through the course adding new features when relevant.

## Making our project

Let's start by creating a folder that we will use as our project for managing our hosts for the project.  We started in the follow me by adding the IP addresses of our systems and setting their names.  The inventory.ini currently resides in your home directory as **~/inventory.ini**.

Let's create the project directory.  You can add this to a git repository if you wish.

```
mkdir ansible_project_servers
```

Change into the new directory;

```
cd ansible_project_servers
```

From this point onward when working on the labs we will use this directory to build up our understanding of Ansible and build a working system.

For muscle memory, let's recreate the ansible.ini file from earlier that manages our machines;

```
[controller]
controller ansible_host=localhost ansible_connection=local

[webserver]
web01 ansible_host=192.168.1.2

[database]
db01 ansible_host=192.168.1.3

[appservers]
web01
db01

[all:vars]
ansible_ssh_common_args='-o StrictHostKeyChecking=no'
ansible_become=true 

[nodes:vars]
ansible_ssh_private_key_file=~/.ssh/ansible
```

Save the file.

The IP addresses for **node1** and **node2** will need to be changed to match the 2 servers that we will be managing under Ansible orchestration.

**NOTE:** We have also changed the section of nodes to be more specific, allowing us to target different nodes for different configuration.  In this case we are going to look at the build of a web server and a database server.  The types of server are irrelevant, as it's the concept of orchestration that is important with Ansible, and how we construct our playbooks and configuration.  The modules required will vary depending on the system you wish to manage.

## Check the configuration

Now let's check the configuration works by targetting different parts of the configuration through running an ad-hoc Ansible command.

Start by using the **ping** module.

1. Target the controller node
    * This is the node we are doing all the Ansible configuration on.
    * The node we are on right now
2. Target all nodes
    * For this you will need to specify **all** instead of the specific Ansible alias name for the node.
3. Target the webserver node using its group name
4. Target the database node using its alias node name
5. Target the webserver and database server using the **appserver** group name.
    * This should result in both web and database servers being pingged.

**NOTE:** Currently the configuration of our system is to run sequentially.  This is handy when things go wrong as it's easier to identify which system broke.

## Changing the configuration

Let's now create an **ansible.cfg** file to include the following;

* **forks** to enable at least 5 systems to run in parallel
* Specify the inventory file to be ./inventory.ini
* Set the remote user to ansible
  * This saves us having to specify it as a variable in our inventory file
* Turn off deprecation_warnings

Save the file.

Now let's check that the configuration is working.

1. Target all the nodes with a ping.
2. If you run the command multiple times does the order change?
3. Target the appserver node group with the **setup** module command
    * This will generate lots of output
    * OPTIONAL: Refer back to how we filtered earlier to obtain the **ansible_os_family** attribute, or pick an attribute from the output.
4. Run a **shell** module that will execute the **uname -a** command on each of the **appserver** group nodes.
    * This should return the kernel and architecture detail for each of the systems.


## OPTIONAL extra

If you have time or feeling brave, do the following;

1. Remove the line
    ```
    ansible_ssh_common_args='-o StrictHostKeyChecking=no'
    ```
    from the **all:vars** section
2. Save the file
3. Run the Ansible ad-hoc ping module against the appservers node group.
    * This should fail to execute as **ssh** will want to save the host fingerprint.
    * Terminate this run by hitting CTRL+C as normal for Linux to terminate a process
4. Now lets add the following line to our **ansible.cfg**
    ```
    host_key_checking = False
    ```
5. Now try running the Ansible ping module
    * All being well the 2 hosts will respond with **pong**
    * The configuration is global, so again saves us having to remember the SSH option