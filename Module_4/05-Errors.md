# Error Handling

Often when writing playbooks you will come across the need to capture and handle errors.

Error handling in Ansible is referenced at https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_error_handling.html, and can be searched by typing "ansible error" into your search engine.

From the documentation you can see we have different types of error actions:

* ignore_errors
  * The original and classic method of ignoring errors and continuing
  * True or False value
  * Only need to supply if True as False is the default
* ignore_unreachable
  * If we cannot connect to the host
* failed_when
  * This is what we could use in our previous example
  * Used with a condition to define the failure
  * Causes Ansible to fail if true

Ansible also allows you to define a percentage of failures in your playbook to decide when to abort execution using the **max_fail_percentage** as a top level attribute.

Let's now revisit our playbook from the last section.

```yaml
- name: Condition based on command output
  hosts: controller

  tasks:
  - name: Run python script
    ansible.builtin.shell:
      cmd: ./mypy.py NOK
    register: output

  - name: Run this only if we get OK
    ansible.builtin.debug:
      msg: The command was successful doing this stage
    when: output.stdout == "Success"
```

Here we have set the value for the Python script to NOK, so we want it to stop.  However, our Python script exits with failure too.

For simple purposes, let us add the **ignore_errors: true** after the **register**, since this is the section that is failing.

```yaml
- name: Condition based on command output
  hosts: controller

  tasks:
  - name: Run python script
    ansible.builtin.shell:
      cmd: ./mypy.py NOK
    register: output
    ignore_errors: true

  - name: Run this only if we get OK
    ansible.builtin.debug:
      msg: The command was successful doing this stage
    when: output.stdout == "Success"
```

Notice now that the failing code shows **...ignoring**, to let us know that it is not a problem.  Our **debug** is then skipped as our condition is not met.

We could then check to see if the command failed by using the **register** **rc** attribute, which is the exit status of the shell command.

```yaml
- name: Condition based on command output
  hosts: controller

  tasks:
  - name: Run python script
    ansible.builtin.shell:
      cmd: ./mypy.py NOKa
    register: output
    ignore_errors: true

  - name: Run this only if we get OK
    ansible.builtin.debug:
      msg: The command was successful doing this stage
    when: output.stdout == "Success"

  - name: Clean up if the exit status is 3
    ansible.builtin.debug:
      msg: Cleaning up
    when: output.rc == 3
```

In this play we have changed the argument to the Python script to **NOKa**, forcing the exit status of 3, causing our clean up to run.  If we wanted Ansible to fail at this point we would change **when** with **failed_when** which we would only need if we ignored the error of the original failing command.

Using this technique we can control what happens based on different exit status or messages that we receive from commands.