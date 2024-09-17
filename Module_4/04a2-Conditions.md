We use the **set_fact** to create runtime variables.

Let's have a look at some code that will detect the operating system family and then set's the correct fact for the package to be installed.

```yaml
- name: Agnostic Apache install
  hosts: all

  vars:
    portno: 80
    nameservers:
      - 8.8.8.8
      - 1.1.1.1

  tasks:
    - name: Set package if Debian
      ansible.builtin.set_fact:
        package_name: apache2
      when: ansible_facts['os_family'] == 'Debian'

    - name: Set package if RHEL
      ansible.builtin.set_fact:
        package_name: httpd
      when: ansible_facts['os_family'] == 'RedHat'

    - name: Show selected package
      ansible.builtin.debug:
        msg: "The chosen package is {{ package_name }}"
```

If you're lucky enough to have different operating systems for each machine you'll notice that the package will be different if the operating system family changes.

Making use of the **shell** module can help you perform checks if the Ansible module does not, or if you want to detect something yourself before deciding to run the modules.  What we're saying is you can obtain the output of a command in a **register** variable and make use of that in the **when** too.

Let's say that you have a new program that you wish to control with Ansible, and there is no module to set that program up, or you need to run a program that is your own Python program.

First let's create a Python script to run.

### Python script to control with Ansible

Create a new file called **mypy.py**.

```python
#!/usr/bin/env python3

import sys

if len(sys.argv) < 2:
  print("ERROR first")
  sys.exit(1)

if sys.argv[1] == "OK":
  print("Success")

if sys.argv[1] == "NOK":
  print("Failed")
  sys.exit(2)

if sys.argv[1] != "OK" and sys.argv[1] != "NOK":
  print("Unknown")
  sys.exit(3)
```

The code has different exit states too, to enable automation of the code as well.

Let's now build an Ansible playbook that will call our command and perform actions based on the output first.

```yaml
- name: Condition based on command output
  hosts: controller

  tasks:
  - name: Run python script
    ansible.builtin.shell:
      cmd: ./mypy.py OK
    register: output

  - name: Run this only if we get OK
    ansible.builtin.debug:
      msg: The command was successful doing this stage
    when: output.stdout == "Success"
```

Running this playbook will result in the script running and the word **Success** being picked up by the **when** clause, and priting the debug message.

If we change OK to NOK, or forget to put it then the debug statement will be skipped.  Try it.

OUCH!!!!

Our command failed.  Why was this?

Time for our next installment.  Handling errors.