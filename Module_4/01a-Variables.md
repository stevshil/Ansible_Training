# Variables

REF: https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html

Ansible allows the use of variables for:

* Host facts
  * Information obtained by Ansible from hosts
  * Normally required **gather_facts = true** to be set, which is the default value
* User defined values
  * These can be set either in the inventory
    * Next to the host if the variable is host specific, e.g. assigning an attribute such as **environment=production** to designate your hosts
    * These are referred to as **hostvars**
  * In a **all:vars** section in the inventory to assign values to all hosts
  * In a **hostgroup:vars** section in the inventory to assign values to all hosts within a particular group
  * In the playbook **vars** section
    * These are directly associated to the hosts using the playbook
* Storing output of modules
  * These are referred to as **register** variables
  * You can manipulate the output based on its structure as a dictionary, list or string
    * Dictionaries allow you to use dot notation to access the elements
    * Lists work just like arrays using the numerical index
  * You need to know how the data is captured

There may be other uses, but these tend to be the key ones.

The use of variables allows us to supply different values for different environments, which we will review in the **Roles and sites** section.  We can also override variables when running the playbook on the command line using the **--extra-vars** option and specifying the **key=value** pairs as a space separated string or as a JSON formatted string.

## Variable precendence

* This is taken directly from the Ansible documentation, referenced at the beginning.
* command line values (for example, -u my_user, these are not variables)
* role defaults (as defined in Role directory structure)
* inventory file or script group vars
* inventory group_vars/all
* playbook group_vars/all
* inventory group_vars/*
* playbook group_vars/*
* inventory file or script host vars
* inventory host_vars/*
* playbook host_vars/*
* host facts / cached set_facts
* play vars
* play vars_prompt
* play vars_files
* role vars (as defined in Role directory structure)
* block vars (only for tasks in block)
* task vars (only for the task)
* include_vars
* set_facts / registered vars
* role (and include_role) params
* include params
* extra vars (for example, -e "user=my_user")(always win precedence)

This is not something you'll remember, but worth knowing where the reference is, when debugging a weird value error.

## Using variables

In our playbooks earlier we saw the use of the **vars:** section which is at the same top level as **tasks**, **handlers**, and **hosts**.

```yaml
- name: Playbook description
  hosts: host_or_hostgroups
  vars:
    your_variable_name: your_variable_value
```

As you can see from the syntax above the **vars:** location in a **single** playbook.

This type of variable can be created up front and changed as part of your code, so that you can use your version control system to keep track of the changes.  This is useful for features such as software package versions, and other values that may change in your host configuration or software deployments.

### Using variables and CLI override

Let's take a look at how the command line options **--extra-vars** can override a variable that you have set in a playbook.  For this we'll write a simple playbook that we'll run on the controller.

```yaml
- name: Variable command line override
  hosts: controller
  vars:
    my_version: 1.0

  tasks:
    - name: Show variable value
      ansible.builtin.debug:
        msg: "The value of my_version is {{ my_version }}"
```

Save the playbook, and we'll run it normally first to see the value of **1.0** being displayed.

```sh
$ ansible-playbook 01-cli.yaml
[WARNING]: Found both group and host with same name: controller

PLAY [Variable command line override] **********************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [controller]

TASK [Show variable value] *********************************************************************************************
ok: [controller] => {
    "msg": "The value of my_version is 1.0"
}

PLAY RECAP *************************************************************************************************************
controller                 : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

We can see on the **ok: [controller] => {** line that our value for **my_version** has printed **1.0**.

Let's now use the command line override:

```sh
$ ansible-playbook 01-cli.yaml --extra-vars 'my_version=2.0'
[WARNING]: Found both group and host with same name: controller

PLAY [Variable command line override] **********************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [controller]

TASK [Show variable value] *********************************************************************************************
ok: [controller] => {
    "msg": "The value of my_version is 2.0"
}

PLAY RECAP *************************************************************************************************************
controller                 : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

As you can see from the output we now have **2.0**, as specified.

This is handy if you want to supply default values for your development or local environments, but wish to use **single** file playbooks and override the values using your CI/CD environments.

In your CI/CD servers you can set shell scripts to run the commands to override.  However, we will see a different way to handle different environments and releases when we look at **roles and sites**.

## Hostvars

Hostvars are the variables that are stored against a particular host within the inventory.  If we take a look at our current inventory:

```ini
[controller]
controller ansible_host=192.168.1.225 ansible_connection=local os=ubuntu

[webservers]
web01 ansible_host=192.168.1.186 ansible_user=ansible ansible_ssh_private_key_file=~/.ssh/ansible os=rhel ansible_become=true ansible_become_user=root

[databases]
db01 ansible_host=192.168.1.222 ansible_user=ansible ansible_ssh_private_key_file=~/.ssh/ansible os=ubuntu ansible_become=true ansible_become_user=root
```

In the above we can see the hostvars for **web01** as:

* ansible_host
* ansible_user
* ansible_ssh_private_key_file
* os
  * This is one we created for our own purpose
* ansible_become
* ansible_become_user

The **ansible_** variables are ones recognised by the **Ansible** system and will be used for specific purposes.  The **os** variable is one we added our selves.

Let's use some code to obtain the **os** and **ansible_host** values and print them out on the controller.

```yaml
- name: Get hostvars
  hosts: controller

  tasks:

    - name: Show os name for web01
      ansible.builtin.debug:
        msg:
          - "{{ hostvars['web01'].os }}"
          - "{{ hostvars['web01'].ansible_host }}"
```

You'll notice that to obtain a variable associated with a particular host we need to specify the Ansible host name from the inventory file.  Like the other variables that contain keys we can use the dot notation to access specific attributes.

Changing the Ansible hostname will show the attributes for the other hosts.

Variables listed in a section such as **[all:vars]** or **[webserver:vars]** where they would be classed with the group are still accessible as host vars.

Let's test this by adding **environment=production** to a section called **[all:vars]** in our **inventory.ini** file.

```ini
[all:vars]
environment=production
```

If we then change our example code to access the **environment** variable:

```yaml
- name: Get hostvars
  hosts: controller

  tasks:

    - name: Show os name for web01
      ansible.builtin.debug:
        msg:
          - "{{ hostvars['web01'].os }}"
          - "{{ hostvars['web01'].ansible_host }}"
          - "{{ hostvars['web01'].environment }}"
```

We access the **environment** variable in the same way as if the variable was associated with each host and written on every host line.

## Groups

Group variables will list the Ansible host names associated with each host group section.

```yaml
- name: Get group vars
  hosts: controller

  tasks:
  - name: Get all hosts in inventory
    ansible.builtin.debug:
      msg: "{{ groups['all'] }}"
  
  - name: Get hosts from databases
    ansible.builtin.debug:
      msg: "{{ groups['databases'] }}"
```

When working with group variables you are aiming to obtain the hosts within the groups.

You will also note, that even if you do not specify **all** in your inventory that you will still have access to the **all** group, which covers all hosts listed in your inventory file.