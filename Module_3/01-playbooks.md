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

```yaml
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

You'll notice that the hosts, vars, tasks and handlers are all aligned.  This means that the vars, tasks and handlers will be associated to the hosts specified as the value.

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

The layout of an Ansible playbook is YAML.

If you are new to YAML here are some quick online tutorials you can try:

* https://spacelift.io/blog/yaml
* https://circleci.com/blog/what-is-yaml-a-beginner-s-guide/
* https://yaml.org/spec/1.2.2/
* https://learnxinyminutes.com/docs/yaml/

### A very quick intro to YAML

YAML is a data formatting language, and allows us to structure our data.  If you've heard of JSON, then YAML is an alternative way of formatting data to represent scalar values, arrays/lists or dictionary/maps.

#### Single/Scalar variables

An attribute/variable with value:

```yaml
linux_system: Debian Buster
system_version: 12.0.2
```

Basic scalar variables that contain a single value are mapped as key/value pairs, separated by a colon :.  Each key/value pair is stored on it's own line.

YAML does not deal with data types, that is down to the language that creates or uses the data.

#### An array/list

Array's are a named item with many values.  A list identifies the data associated with it by indentation, where the values are indented at the same level.  Another key point is that each value is preceded by a minus (-) symbol.

Below we have an array/list called **fruits** as follows:

```yaml
fruits:
  - apple
  - banana
  - pear
  - kiwi
```

As you can see above the values are all indented by 2 spaces, followed by the - and a space to indicate a value and finally the actual value.

In Python the code for the above list would be:

```python
fruits = ["apple","banana","pear","kiwi"]
```

If you were to use Python then we would access the fruit pear using;

```python
fruits[2]
```

#### A dictionary/map

In most good languages as well as having an indexed set of values in an array/list, we can also have associative arrays, also known as a dictionary, map or hash map.  YAML supports this in a similar way to the list above, but instead of the - we have an indented set of key/value pairs.

Here we have a collection for a telephone book contacts:

```yaml
contacts:
  Steve: 555-1234
  John: 555-1111
  Nick: 555-2222
  David: 555-3333
```

Notice in this case that we are back to scalar variables, which are indented, therefore making them belong to the data **contacts**.

The creation of the above dictionary in Python would be:

```python
contacts = {"Steve": "555-1234", "John": "555-1111", "Nick": "555-2222", "David": "555-3333"}
```

In Python you would access Nick as follows;

```python
contacts["Nick"]
```

#### Nested data

YAML also supports nested data allowing you to create complex structures.

```yaml
listOfUsers:
  - name: Steve
    phone: 555-1234
    os: Linux
    hobbies:
      - Squash
      - Cycling
      - "Drawing & painting"
  - name: Nick
    phone: 555-3333
    os: Windows
    hobbies:
      - Hacking
      - "Cooking:Cleaning:Sleeping"
```

Above is a simpler complex structure where **listOfUsers** contains a list of 2 elements, where each element is a dictionary object, using the same keys for each value.

Another point from the above example is that we have quoted some of the values.  This is due to special characters & and : being used in the value.  Certain characters will require quoting, and Ansible will throw errors if it does.

## Example build a web service

In this single playbook we will see how to build up a playbook to create an Apache web services and our own default starting page.  This example will introduce you to;

* Variables
* Tasks
* Files
* Handlers

We will start with a playbook that will install Linux for RedHat flavours of Linux.

### 1st we will target the servers to build

In our last lab we created the inventory.ini file with 2 separate node groups, one of which we named webservers.  We only have one node listed in the group, but if we had multiple then they would all be provisioned.

Let's create our playbook, and call it webserver.yml.

```yaml
- hosts: webservers
  vars:
    web_page_content: Welcome to my Ansible built web server, using Apache.
```

Above we have specified that our playbook will target the host group **webservers** from our **inventory.ini** file.  The **hosts** directive allows us to specify one or more nodes or host groups.  If you are list multiple groups or nodes you would change hosts to be an array, e.g.:

```yaml
- hosts:
    - node01
    - node02
    - mywebservers
```

### Now we will specify the tasks

The tasks will perform the actions on the hosts being provisioned.  These will be the nodes listed in the **webservers** node group in our **inventory.ini**.

The tasks we will be performing to provision our web server are:

* Install Apache
* Create an index.html with our own text from the **web_page_content** variable
* Start and enable the Apache service

As we create each task we will consult the Ansible documentation to get an idea how we can build tasks, and understand the attributes available.  When looking for Ansible modules you can do so in 1 of 2 ways:

* Using your favourite search engine and typing in:
  * Example of looking for installing software
    * Ansible module install package
    * Ansible module install software
  * If you know the module name
    * Ansible module **package**
    * Ansible module **lineinfile**
* Alternatively you can use the **all modules** documentation
  * https://docs.ansible.com/ansible/2.9/modules/list_of_all_modules.html
    * Change 2.9 for the version of Ansibl you are using
    * There is a grouping menu on the left if you have an idea of the category
    * You could use **find** in your web browser
    * **NOTE:** Using this method you should ideally know the module you want to use

```yaml
  tasks:
    - name: Install Apache
      ansible.builtin.package:
        name: httpd
        state: present
    
    - name: Create index file
      ansible.builtin.lineinfile:
        path: /var/www/html/index.html
        line: "{{ web_page_content }}"
        create: yes
        group: root
        owner: root

    - name: Start and Enable Apache
      ansible.builtin.systemd:
        name: httpd
        state: started
        enabled: yes
```

Modules used above for reference:

* https://docs.ansible.com/ansible/2.9/modules/package_module.html#package-module
* https://docs.ansible.com/ansible/2.9/modules/lineinfile_module.html#lineinfile-module

In the above you will see 3 tasks.  The 1st installs the Apache package using the generic **package** module instead of having to decide if we need to use **yum** or **dnf** or **apt**.  The **state** attribute allows you to ensure that the application is installed (present), or you can always ensure the **latest** version is installed, although dangerous; could break your system.

If you wish to specify a specific version you can do so through the **name** value, e.g. **httpd>=2.4**.

The main thing to notice is the layout where the tasks are an array, with each task being named so that when the playbook runs we can identify where it currently is or has failed.  After the name the Ansible module is then specified which will perform the underlying action on the node.  The attributes that are specified can be found within the documentation with full description about what the attribute will do and the values that can be used.  The documentation also specifies what attribute **must** be specified.

For the **Create index file** task you will notice that we have used the **web_page_content** variable.  In particular notice how we have specified the variable in double quotes and double curly brackets.

Now that we have our playbook, in the same directory as our inventory.ini and ansible.cfg we can run the playbook and provision our server.

### Running the playbook

In the earlier modules we used the **ansible** command to run ad-hoc Ansible modules and specified various options.  When executing a playbook we use the **ansible-playbook** command.

Run the playbook on the Ansible controller, which is where we've been creating these files.  If you're using Git, then you'll need to git pull your changes to your Ansible controller.

```sh
ansible-playbook webservers.yml
```

Since the playbook contains the hosts to target, and we have our ansible.cfg already configured, we're good to go.

The output of the command will look something like:

```sh
[WARNING]: Found both group and host with same name: controller

PLAY [webservers] ******************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [web01]

TASK [Install Apache] **************************************************************************************************
changed: [web01]

TASK [Create index file] ***********************************************************************************************
changed: [web01]

TASK [Start and Enable Apache] *****************************************************************************************
changed: [web01]

PLAY RECAP *************************************************************************************************************
web01                      : ok=4    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

```

Not how the output is written with the summary at the end to help us identify quickly if there are issues.  In the above we see 4 ok, but 3 were changed since the 3 tasks we needed to run had to make changes to the system.

## Ansible is idempotent

Run the playbook again, exactly as you just did.

```sh
[WARNING]: Found both group and host with same name: controller

PLAY [webservers] ******************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [web01]

TASK [Install Apache] **************************************************************************************************
ok: [web01]

TASK [Create index file] ***********************************************************************************************
ok: [web01]

TASK [Start and Enable Apache] *****************************************************************************************
ok: [web01]

PLAY RECAP *************************************************************************************************************
web01                      : ok=4    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

Notice this time everything reports as **ok=4**, meaning nothing was updated as nothing changed.

Let's make a change to our Ansible playbook.

Edit the webservers.yml file and locate the line **web_page_content**.

Add ** Part Duex** to the end of that line and save the file.

Run the Ansible playbook.

```sh
$ ansible-playbook webservers.yml

[WARNING]: Found both group and host with same name: controller

PLAY [webservers] ******************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [web01]

TASK [Install Apache] **************************************************************************************************
ok: [web01]

TASK [Create index file] ***********************************************************************************************
changed: [web01]

TASK [Start and Enable Apache] *****************************************************************************************
ok: [web01]

PLAY RECAP *************************************************************************************************************
web01                      : ok=4    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

Notice this time we have 1 change, since the index.html file was updated due to our modification.

Ansible will only make changes to that which has been modified in the code and is different on the node being provisioned.

If you **curl** the webserver node or use your web browser you can see that an extra line was created, since we did not tell **lineinfile** to modify the existing line.