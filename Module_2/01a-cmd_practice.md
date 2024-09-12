# Ad-hoc Command Practice

Here we will run some **ansible** commands to understand the syntax.  The instructor will talk you through these examples and how you construct the commands and how to find out what to put in the commands.

## Finding the documentation

To work with the Ansible command you need to know how to find the following;
* The syntax for the ansible command.
  * In Google/DuckDuckGo you can type **ansible ad-hoc commands**.
    * The first link should be [Introduction to ad hoc commands](https://docs.ansible.com/ansible/latest/command_guide/intro_adhoc.html).
* Next you would need to know about the module you wish to run against the host or group of hosts.
  * In Google/DuckDuckGo you can type **ansible modules**.
    * The first link should be [All modules](https://docs.ansible.com/ansible/2.9/modules/list_of_all_modules.html)
      * &#x26a0;&#xfe0f; NOTE: The 2.9 is the version of Ansible you have installed.
        * If you change the value to one that does not exist you'll get an error page and a pull down list of versions.
* Finally the help page for the **ansible** command;
  * On your Linux system, as long as **man** is installed, you can type;
    
    ```bash
    man ansible
    ```
  
  * Alternative do a web search for **man ansible**;
    * The first link should be [ansible(1): run command somewhere else - Linux man page](https://linux.die.net/man/1/ansible)

## Running some commands

Here we will run commands against hostnames as we have not yet configured our host groups.

### Recap on ping

First we'll recap the **ping** command from the last section.

```bash
ansible localhost -m ping
```

### Listing Ansible facts

Facts are variables that can be used in Ansible playbooks and templates which you'll see later in the course.

```bash
ansible localhost -m setup
```

As mentioned in the last module as of version 2.6 of Ansible you can use the module name clarification;

```bash
ansible localhost -m ansible.builtin.setup
```

> Most people who are only just learning Ansible will write the second one since this is what is now in the documentation.  If you use version prior to 2.6 you'll have to use the first one, which as you can see still works today.

The output from this command is JSON formatted.

### Create a file

To create a file we can use the **lineinfile** module, which you can search the documentation for by typing **ansible lineinfile** into a search engine.  This should point you to [ansible.builtin.lineinfile module – Manage lines in text files](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/lineinfile_module.html)

```bash
ansible localhost -m lineinfile -a "create=true line='Hello World' mode=500 path=/tmp/hello_world"
```

We can check that the command worked from the output;
```
localhost | CHANGED => {
    "backup": "",
    "changed": true,
    "msg": "line added and ownership, perms or SE linux context changed"
}
```

We can see **localhost | CHANGED** letting us know the host the action happend on and that a change was requested.  Within the curly braces we are told if the action succeeded with **"changed": true**.  The **msg** let's us know further details.

We can also see the details by listing and catting the file;
```bash
$ ls -l /tmp/hello_world
-r-x------ 1 ansible ansible 12 May  3 15:46 /tmp/hello_world

$ cat /tmp/hello_world
Hello World
```

Run the command again and look at the output, it should be as follows;

```
localhost | SUCCESS => {
    "backup": "",
    "changed": false,
    "msg": ""
}
```

* What tells you that the module worked or not?
* Did Ansible run successfully?

### Grab information from a URL

If you use Linux regularly you may have come across **curl** or **wget** to download web content or files.  Ansible uses **get_url**.  As with earlier you can simply search for the module by typing **ansible** in front of the module name you want.  Or you can do a search such as **ansible url**.

The module documentation is [ansible.builtin.get_url module – Downloads files from HTTP, HTTPS, or FTP to node](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/get_url_module.html)

Let's download the following DNS forward configuration [DNS forward config](https://raw.githubusercontent.com/stevshil/docker/master/dns/files/var_named/forward.data) using Ansible;

```bash
ansible localhost -m ansible.builtin.get_url -a "url=https://raw.githubusercontent.com/stevshil/docker/master/dns/files/var_named/forward.data dest=/tmp/forward.data mode=0644"
```

You'll notice that similar to last time there is output to let you know what happend.

### Adding a group

Here we'll escalate our permissions to use **sudo** and add our own group to the server.

```bash
ansible localhost -m ansible.builtin.group -a "name=training state=present"
```

You'll notice that this fails with the **localhost | FAILED!**.

We need to **become** root using **sudo**, which in Ansible is performed with the **--become** option as mentioned in the ad-hoc commands Ansible documentation.

```bash
ansible localhost -m ansible.builtin.group -a "name=training state=present" --become
```

The documentation for the group module is [ansible.builtin.group module - Add or remove groups](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/group_module.html)

You should be able to run the following command to confirm that the **training** group is on the system;

```bash
$ grep training /etc/group
training:x:1001:
```

Or something similar as the number may vary.

### Finally let's remove a file

For this we use the **file** module.  Let's remove our DNS forwarder file.

```bash
ansible localhost -m ansible.builtin.file -a "path=/tmp/forward.data state=absent"
```

The **state** option allows us to ensure the file has or gets deleted by using **absent**.

This module can also be used for ensuring files are there and change attributes such as permissions, user or group as well as creating links.

# RIGHT - NOW IT'S YOUR TURN