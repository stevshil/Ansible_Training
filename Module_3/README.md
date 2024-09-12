# Ansible Playbooks

## What are playbooks

Playbooks are files that contain the instructions you wish to apply to nodes in your infrastructure.

You may decide to break your playbooks into;
* Type of server
  * Playbook written specifically for that node, or cluster
* Roles (more common)
  * File server, DNS Server, Database server, Web server
  * The roles may have variations based on the operating system
    * These variations may well be coded in the playbook

Playbooks can be a singular file, or as a role, which is a collection of files and directories which breakdown the single file.  We'll dive into the detail of the differences later.

For this module we will focus on understanding playbook details and instructions in a single file.

## Playbook layout

Let's take a look at a skeleton playbook without instructions.

A good reference for this is https://docs.ansible.com/ansible/2.8/user_guide/playbooks_intro.html

```
- name: A synopsis of the playbook
  hosts: group_name
  gather_facts: true/false
  OTHER GENERAL ATTRIBUTES

  vars:
    a_variable: a_value

  tasks:
    - name: Synopsis of task
      module_command_name:
        module_attribute: module_attribute_value
        more_attributes: mode_values
        ...

    - name: Another task to perform
      module_command_name:
        module_attributes
        ...

  handlers:
    - name: Synopsis of handler
      handler_command_name:
        handler_attribute: handler_value
        ...
```

A playbook needs to know information about hosts to provision.

There are some sections we can point out here;

* name:
  * Allows us to tag parts of the playbook, which will be displayed when the playbook runs; making it easier to debug issues.
* hosts:
  * This allows us to specify the node names or groups from the Ansible inventory file that will be targetted by this playbook.
* gather_facts:
  * This tells Ansible whether we want to grab all the Ansible variables relating to that host.  This information is what you saw when you ran the **setup** module using the ad-hoc command.
* There are other top level actions you can specify.
* vars:
  * Variables that you wish to create and set that will be used throughout the playbook, allowing you to change them at run time.
* tasks:
  * The modules that you want to execute as part of your provisioning of nodes
  * Each task will specify the module that will execute the command on that node
  * Tasks allow you to also work with files and templates
    * These we will cover as we go
* handlers:
  * This is a trigger section.
  * Ansible will call handers when a task uses **notify**.  The **notify** will contain the name of the handler to call.
  * An example would be calling a service restart