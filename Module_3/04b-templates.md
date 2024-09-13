# Template loops

Let's take a look at a different example.  Let's work with the /etc/hosts file and add our hosts to it.

For this to work we will need to obtain the IP addresses and host names from our inventory.  These are known as **hostvars**, for when you're searching the web.

* https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_vars_facts.html

In the inventory we have our hostgroups and each group has a node definition of which we have used or created attributes associated to that host.

To create an /etc/hosts file we need to obtain the **ansible_host** value which is the IP address for each node.  Our controller though is localhost, so we may need to use a different method for that, we'll deal with this later.

Jinja2 supports a **for** loop, where the syntax is:

```jinja2
{% for item in seq -%}
  Raw text here.
  {{ item }}
{%- endfor %}
```

You'll notice the use of the {% %} again, and the use of the control variable called **item**.  **item** can be called what ever you like, but ideally should be meaningful to what you are looping through, e.g. if I have a list of hosts, then I'd use host, if it's a list of users, then user.

You'll notice with Jinja2 that constructs with a body will have and **end** which is conjoined with the construct, so:

* if = endif
* for = endfor

## Change to our inventory

For our /etc/hosts to obtain all the relevant IPs for all hosts we should ensure that the IP address are in the inventory file under ansible_host attribute.

Our file will now look something like:

```ini
[controller]
controller ansible_host=192.168.1.225 ansible_connection=local os=ubuntu

[webservers]
web01 ansible_host=192.168.1.186 ansible_user=ansible ansible_ssh_private_key_file=~/.ssh/ansible os=rhel ansible_become=true ansible_become_user=root

[databases]
db01 ansible_host=192.168.1.222 ansible_user=ansible ansible_ssh_private_key_file=~/.ssh/ansible os=ubuntu become=true become_user=root
```

In this case we have changed the **ansible_host** value of the controller from **localhost** to it's actual IP.

## The template file

Create a file in the templates directory called **etc_hosts.j2**.

In the file type in the following:

```jinja2
# This hosts file is created by Ansible, do not edit!

127.0.0.1 localhost
{% for host in groups["all"] -%}
{{ hostvars[host]["ansible_host"] }}    {{ host }}
{% endfor -%}
```

The above file loops through **all** of the hosts in the inventory.ini file and then within the loop we use the **ansible_host** value, which is the IP address to create the relevant line in the hosts file and the host name from the {{ host }} variable.

**NOTE:** The use of **all** will always get all hosts in the inventory regardless of host groups.

## The playbook

In the webservers.yml play book we need to add a new task that will create our hosts file.

Add the following code before the **handlers** section.

```yaml
    - name: Edit hosts file
      ansible.builtin.template:
        src: templates/etc_hosts.j2
        dest: /etc/hosts
        group: root
        owner: root
        mode: 0644
      tags:
        - hosts
```

The above code uses the template module and again specifies the source and destination files.  The template is what is doing the work.

However, you'll notice I've added a **tags** section here.  This will allow us to run just this section of the playbook without having to run the rest.

Tags are useful for when you only need to run groups of tasks from within a playbook, and you can use the same tags across tasks, and assign multiple tags to tasks, since it is an array.

Now let's run the playbook to update the hosts file:

```sh
ansible-playbook webservers.yml --tags "hosts"
```

Log on to the web server with SSH and run:

```sh
cat /etc/hosts
```

You should now see the controller, web01 and db01 with the assigned IP addresses.

## Conditions in templates

As well as loops you can also place conditions into templates too, using **if**.

Let's use the /etc/hosts example and target the controller, since we don't need our nodes to know about this server.

The if statement in jinja2 is as follows:

```jinja2
{% if condition %}
   {# Code to run if true }
{% endif %}
```

```jinja2
# This hosts file is created by Ansible, do not edit!

127.0.0.1 localhost
{% for host in groups["all"] -%}
{% if host != "controller" -%}
{{ hostvars[host]["ansible_host"] }}    {{ host }}
{% endif -%}
{% endfor -%}
```

In the above example we have told Jinja2 to ignore the host called **controller** from our inventory file.

Change your code and run the playbook.