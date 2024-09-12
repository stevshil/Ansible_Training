# Handlers

Reference: https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_handlers.html

If we make a configuration change to our service we would want that configuration to be activated after the change, or at the end of the complete configuration.  To achieve this Ansible gives us **handlers** and **notify**.

The **hanlders** section is a separate section in your playbook, as is the **tasks** section and **hosts** section.

Handlers are called by specifying a **notify** in the task that should force the handler action, such as a reload or restart of the service, in the case of a configuration change.

Other uses for handlers:

* Trigger an **apt update** for Debian Linux systems after changing an apt repository configuration
* Deleting files after an application removal

There are others you may think of based on the systems and services you configure.

## Example

Let's look at adding a configuration change to our Apache web server so that we can change the port number.

Our current webservers.yml file is as follows;

```yaml
- hosts: webservers
  vars:
    web_page_content: Welcome to my Ansible built web server, using Apache. Part Duex

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

Let's add another task between the **Create index file** and **Start and Enable Apache** tasks.  We'll call the task **Set port number**.

```yaml
    - name: "Set port number {{ portno }}"
      ansible.builtin.lineinfile:
        path: /etc/httpd/conf/httpd.conf
        regexp: "^Listen 80"
        line: "Listen {{ portno }}"
```

You'll notice that we set a variable called **portno** which we will need to add to our **vars** section as follows;

```yaml
- hosts: webservers
  vars:
    web_page_content: Welcome to my Ansible built web server, using Apache. Part Duex
    portno: 8080
```

So that our playbook runs we'll set the port number to 8080.

Save the playbook and run it.

```sh
$ ansible-playbook webserver.yml

[WARNING]: Found both group and host with same name: controller

PLAY [webservers] ******************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [web01]

TASK [Install Apache] **************************************************************************************************
ok: [web01]

TASK [Create index file] ***********************************************************************************************
ok: [web01]

TASK [Set port number] *************************************************************************************************
changed: [web01]

TASK [Start and Enable Apache] *****************************************************************************************
ok: [web01]

PLAY RECAP *************************************************************************************************************
web01                      : ok=5    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

```

You'll notice that the change will happen, but our web server does not restart and the port number is still 80 until we restart Apache.

Ideally we would have wanted Apache to restart.  So let's do this.

## Adding the handler

Edit the webservers.yml file and at the end of the file add the following code:

```yaml
  handlers:
    - name: Restart Apache
      ansible.builtin.systemd:
        name: httpd
        state: restarted
```

To call the handler when we make a change to the configuration we need to update the **Set port number** task we just created by adding notify.  See the full task code below:

```yaml
    - name: Set port number
      ansible.builtin.lineinfile:
        path: /etc/httpd/conf/httpd.conf
        regexp: "^Listen 80"
        line: "Listen {{ portno }}"
      notify:
        - Restart Apache
```

**NOTE:** How the **notify** value matches the name of the **handler**.

To make this happen we need to change the **portno** value from 8080 back to 80 so that the change happens.  Do this and then run the playbook.

```yaml
    portno: 8080
```

```sh
$ ansible-playbook webservers.yml

[WARNING]: Found both group and host with same name: controller

PLAY [webservers] ******************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [web01]

TASK [Install Apache] **************************************************************************************************
ok: [web01]

TASK [Create index file] ***********************************************************************************************
ok: [web01]

TASK [Set port number 80] **********************************************************************************************
changed: [web01]

TASK [Start and Enable Apache] *****************************************************************************************
ok: [web01]

RUNNING HANDLER [Restart Apache] ***************************************************************************************
changed: [web01]

PLAY RECAP *************************************************************************************************************
web01                      : ok=6    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

Notice the extra **RUNNING HANDLER** step in our output.

To ensure this worked, let's change the **portno** variable back to 8080 and run the playbook.

You should see 1 change.

Log on to the webserver, or point your web browser at the webserver and add port 8080, e.g.:

```
curl webserverIP:8080
```

## The complete webserver.yml

```yaml
- hosts: webservers
  vars:
    web_page_content: Welcome to my Ansible built web server, using Apache. Part Duex
    portno: 8080

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

  handlers:
    - name: Restart Apache
      ansible.builtin.systemd:
        name: httpd
        state: restarted
```