# Playbook to Role

Let's look at converting our webservers.yml playbook to a role, so that we can start to understand and move away from single playbooks if we are intending to work with more complex Ansible configurations.

## Playbook reminder

Our webservers.yml playbook currently looks something as follows:

```yaml
- hosts: webservers
  vars:
    portno: 80
    nameservers:
      - 8.8.8.8
      - 1.1.1.1

  tasks:
    - name: Install Apache
      ansible.builtin.package:
        name: httpd
        state: present

    - name: Create index file
      ansible.builtin.template:
        src: templates/index.html.j2
        dest: /var/www/html/index.html
        group: root
        owner: root
        mode: 0644

    - name: "Set port number {{ portno }}"
      ansible.builtin.lineinfile:
        path: /etc/httpd/conf/httpd.conf
        regexp: "^Listen 80"
        line: "Listen {{ portno }}"
      notify:
        - Restart Apache

    - name: Start and Enable Apache
      ansible.builtin.systemd:
        name: httpd
        state: started
        enabled: yes

    - name: Edit hosts file
      ansible.builtin.template:
        src: templates/etc_hosts.j2
        dest: /etc/hosts
        group: root
        owner: root
        mode: 0644
      tags:
        - hosts

    - name: Configure resolver
      ansible.builtin.template:
        src: templates/etc_resolv.conf.j2
        dest: /etc/resolv.conf
        group: root
        owner: root
        mode: 0644

  handlers:
    - name: Restart Apache
      ansible.builtin.systemd:
        name: httpd
        state: restarted
```

## Creating the role directory structure

Based on the above we can start to create the directory structure for our **apache** role.

Let's start by creating a completely new directory where we will run our completed site from.  We haven't discussed sites yet, but we will soon.

```sh
mkdir oursite
```

Change into the directory

```sh
cd oursite
```

Every site would need to specify the roles which it requires.  This is done by having a **roles** directory, which will contain the roles of everything we wish to build.

```sh
mkdir roles
```

Change into the roles directory.

```sh
cd roles
```

We now need to create the role directory, which we will call **apache**.

```sh
mkdir apache
```

Change into this directory so that we can create our role.

```sh
cd apache
```

Our playbook has the following sections, which we will need to create the corresponding directories for:

* defaults
  * For this we will use our variables as later we will want to override
* vars
* tasks
* handlers
* templates
* files
  * Although we do not have any static files for this project, so we could potentially drop this one.

```sh
mkdir defaults vars tasks handlers templates files
```

We now have the structure we need.


## The variables

The variables directory will contain variables associated with this role, where as defaults contians lower priority variables.  Both can be overridden by site variables.  We will use our **defaults** directory to set our variables.

The variables and defaults directories require a file called **main.yml** or **main.yaml** to contain the code.  If there is no code required then we do not create the file or directory.

```sh
cd defaults
```

Create the **main.yml** file using your favourite editor or IDE.  In the file we will add the following:

```yaml
portno: 80
nameservers:
  - 8.8.8.8
  - 1.1.1.1
```

As you can see we simply list the variables.  There is no need to include the section header as we did with the single playbook because the directory contains the relevant name.

You'll notice that this is the code below the **vars:** section of your playbook.

## The tasks

Now we do the same for tasks.  Here we will create a **main.yml** to include our code.

In an earlier module we introduced conditional tasks, where we set the package for the specific operating system.  If we have lots of tasks that are specific, or want to make our code easier to read we can break these out into different files and call them with include.  More later.

Change to the tasks directory:

```sh
cd ../tasks
```

Create the **main.yml** file and add the following content:

```yaml
- name: Set package if Debian
  ansible.builtin.set_fact:
    package_name: apache2
    when: ansible_facts['os_family'] == 'Debian'

- name: Set package if RHEL
  ansible.builtin.set_fact:
    package_name: httpd
    when: ansible_facts['os_family'] == 'RedHat'

- name: Install Apache
  ansible.builtin.package:
    name: "{{ package_name }}"
    state: present

- name: Create index file
  ansible.builtin.template:
    src: templates/index.html.j2
    dest: /var/www/html/index.html
    group: root
    owner: root
    mode: 0644

- name: "Set port number {{ portno }}"
  ansible.builtin.lineinfile:
    path: /etc/httpd/conf/httpd.conf
    regexp: "^Listen 80"
    line: "Listen {{ portno }}"
  notify:
    - Restart Apache

- name: Start and Enable Apache
  ansible.builtin.systemd:
    name: httpd
    state: started
    enabled: yes

- name: Edit hosts file
  ansible.builtin.template:
    src: templates/etc_hosts.j2
    dest: /etc/hosts
    group: root
    owner: root
    mode: 0644
  tags:
    - hosts

- name: Configure resolver
  ansible.builtin.template:
    src: templates/etc_resolv.conf.j2
    dest: /etc/resolv.conf
    group: root
    owner: root
    mode: 0644
```

As we saw earlier, we have copied everything related to the **tasks:** section, removed the **tasks:** and the indentation as only tasks are written to the file.

## Handlers

Now we do the same for the handlers.

```sh
cd ../handlers
```

Create the **main.yml** file and add:

```yaml
- name: Restart Apache
    ansible.builtin.systemd:
    name: httpd
    state: restarted
```

Here we copied just the handler code from the **handlers** section and place that into a file called **main.yml**

# Templates

The templates and files we can copy directly from our folders earlier, as there is no specific naming convention for these, except how we named them earlier.

```sh
$ cd ..
$ cp ~/templates/*  templates
$ cp ~/files/*  files
```

Once completed the templates and files directories will look as follows:

```sh
$ ls templates/
etc_hosts.j2  etc_resolv.conf.j2  index.html.j2

$ ls files/
index.html
```

We now have our role.

## Testing the role

If we wanted to test our role we can by creating a simple playbook with the following at the top of the **oursite** directory, where we would see roles.

Change to the site directory:

```sh
cd ~/oursite
```

Create a simple playbook, but this time with a difference.

Let's call the file **test-apache.yml**.

```yaml
- name: Testing apache role
  hosts: webservers

  roles:
    - apache
```

Copy the inventory that we had been using earlier into this directory.

```sh
cp ~/inventory.ini .
```

Note we will remove this playbook later, and the inventory too.  This is just to prove our role works.

Run the playbook:

```sh
$ ansible-playbook -i inventory.ini test-apache.yml
```

This time we have explicitly named the **inventory.ini** file with the **-i** option as we have not copied in our **ansible.cfg**.  This is because we are going to create a site, and this is just for testing.

## Summary

A role can be created by breaking down a playbook into separate directories and giving the directory a name.  The subdirectories of the role match the section names of a single playbook.

You don't have to write single playbooks if you know that the code you are going to write is going to be reused, in which case you would write a role.