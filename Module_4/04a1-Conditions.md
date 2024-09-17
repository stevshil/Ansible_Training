# Conditions in Ansible

So far with written playbooks that mostly work without issues.  However, this is not always the case.  Some times a module might not be idempotent if it is new or not been written to check values first.  Other problems may be to do with non-existant files, or data.

An example where this might cause a problem is if you use different Linux family distros, such as Debian and RHEL.  A typical example is the webserver playbook where Debian would use a package and service name of **apache2**, whilst RHEL uses **httpd**.

To deal with issues where we want to make our code platform agnostic we would need to make use of conditions.  Also deciding on whether the code should run on particular servers.  There are many reasons where we will need conditions, so let's take a look at a simple example first of using conditions.

Conditions in Ansible are performed using the **when** statement, and have their own logical comparitors.  The documentation for Ansible conditions is at:

* https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_conditionals.html

## Simple example

Here we will create a simple playbook that will output a message based on which server is being provisioned.

```yaml
- name: Ansible conditions
  hosts: all

  tasks:
    - name: Show message for Controller
      ansible.builtin.debug:
        msg: I am the Ansible Controller - I conduct the symphony
      when: inventory_hostname == "controller"
```

To find the variable for the currently processed hostname you can search for "ansible current hostname".

You'll notice in the code above that we are not using **{{ }}** around the variable.  The **when** clause is a special case where we can use the Ansible variables directly.

As you can see from the output when you run the code, it will only happen on the **controller** node and not the database or webserver node.  This means that we can perform different checks, including from previous tasks and determine if we should run the code.

## Platform agnostic code

Let's revisit our webserver playbook and make it platform agnostic.

Since the package name is what varies between Debian and RHEL, we can make use of a **variable** to be set at runtime to store the package name.

What is the module name we use to create variables at runtime?

[Next >>](04a2-Conditions.md)