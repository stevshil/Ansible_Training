# Templates

Ansible allows you to also create dynamic files on your node.

The idea of templates is that the majority of the file is static content, but there will be parts of the file that will need to be updated based on variables.

Some examples of using templates:

* The DNS /etc/resolv.conf file
  * Adding nameservers to the file
* Adding or deleting hosts to /etc/hosts file or DNS files
* File configurations
* Content files

To first demonstrate a simple template, we will change our HTML file so that it shows the IP address of the host that the file is on.

## Ansible templates

The templating language for Ansible is Jinja2.

* https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_templating.html
* https://docs.ansible.com/ansible/latest/collections/ansible/builtin/template_module.html
* https://docs.ansible.com/ansible/2.9/user_guide/playbooks_templating.html
* https://jinja.palletsprojects.com/en/3.1.x/

We have seen part of the Jinja2 language already where we used our variables in the playbook and the use of the double curly brackets.

The Jinja2 language has programming constructs such as:

* if
* for
* variables
* filters

Templates are called from a playbook by using the **template** module which in turn looks for a directory called **templates**.  All templates must have the extension of **.j2**.

As we are working with templates, the majority of the file could be static text, so the code has to be encased within {% %}.  If you are familiary with ASP, ASP.NET, PHP or JSP then you'll find the syntax very similar.

### Template layout

```jinja2
This is regular text for the file.

My DNS server is: {{ some_variable_name }}

{% if condition -%}
Show this output
{% endif -%}
```

We'll work through if and for in this course, but you should be comfortable in trying out writing your code by using the Jinja2 documentation at [https://jinja.palletsprojects.com/en/3.1.x/](https://jinja.palletsprojects.com/en/3.1.x/) and [https://jinja.palletsprojects.com/en/2.11.x/templates/](https://jinja.palletsprojects.com/en/2.11.x/templates/).

## Basic example

Let's work on having a single changable value in a file.  In this case we will change the index.html file to include the hosts IP address at the time of the Ansible playbook run.

This example will also make user of Ansible variables.  If you remember back to the ad-hoc commands we used **setup** module to list host variables, also referred to as hostvars.

### The template file

First we will create the template files.  To do this we will need to create a directory called **templates** which Ansible looks for when a template is used in the tasks.

Create the directory called **templates** in the directory where your inventory.ini, ansible.cfg and the files drectory are.

```sh
mkdir templates
```

Create the file **index.html.j2**.  Using this naming convention we know that this is the index.html file, but with a modifiable attribute.

```jinja2
<html>
  <body>
    <h1>Welcome to Ansible</h1>
    <h3>Hosted on {{ ansible_facts['default_ipv4']['address'] }}
    <p>This is the static index file</p>
  </body>
</html>
```

**NOTE:** The dictionary element **default_ipv4** is actually **ansible_default_ipv4** from the **-m setup** command.  This means that the **ansible_** is dropped from the keys if you are using the **setup** command to find the variables.

We can also use **ansible_facts['all_ipv4_addresses'][0]** to obtain the IP address too.  Again, the **ansible_** is dropped from the variable name.

The **default_ipv4** is the better option to use as it takes the primary external IP address of the host.  The **all_ipv4_addresses** as you might tell is an array of addresses where your node may have multiple network interfaces. You could use this in a loop rather than specifying a single element, which might give you the wrong address.

### The task

To make the index.html file we need to modify our webservers.yml file.  For this example we will replace the **copy** module for a **template** module.

Edit the **webservers.yml** file and locate the following section:

```yaml
    - name: Create index file
      ansible.builtin.copy:
        src: files/index.html
        dest: /var/www/html/index.html
        group: root
        owner: root
        mode: 0644
```

Here we will change the code to:

```yaml
    - name: Create index file
      ansible.builtin.template:
        src: templates/index.html.j2
        dest: /var/www/html/index.html
        group: root
        owner: root
        mode: 0644
```

The changes made are:

* ansible.builtin.template
  * The module required to execute and use a template
* src
  * The location of the template and its name
  * NOTE: This time we specify the **templates** directory


Save the file and run the playbook.

This time when you view the file you'll see the IP address of the host.

You can check the output either by using curl or your web browser with the IP address of the webserver, or ssh on to the web server.

Using SSH on to the web server will allow us to compare the IP address to check it is correct:

* Log on to the web server, lets' say it's IP is 192.168.1.186
    ```sh
    ssh 192.168.1.186
    ```

* Check the index.html file
    ```sh
    cat /var/www/html/index.html
    ```

    You should see the actual IP address in the file where the variable was in the template

* Check the IP address of the actual host to make sure they match
    ```sh
    ip a
    ```

    Check the **inet** addresses and the 192.168 one should match.
