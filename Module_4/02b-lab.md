# Facts lab

In module 3 we looked at **ansible_facts** and how we could extract data from the host we are currently processing.

In this lab we will create variables for the following **ansible_facts** and then process this for the **database** host.

Create a file called **anfacts.yml** and add the following to the beginning of the file:

```yaml
- name: Creating variables
  hosts: databases

  tasks:
```

Create a task that will create the following variables for the corresponding Ansible facts:

* host_ip
  * ansible_all_ipv4_addresses[0]
* arch
  * ansible_architecture
* bios_date
  * ansible_bios_date
* bios_version
  * ansible_bios_version
* os_dist
  * ansible_distribution
* os_dist_version
  * ansible_distribution_version
* os_family
  * ansible_os_family
* kernel
  * ansible_kernel

Start with 3 of the variables to get your code working first, and then add the rest.  For this you'll need the **set_facts**.  Use the main bullet as the name of the fact, the sub-bullet is the name of the Ansible fact.

To check that you have captured the variable use the **debug** module to print out the variables you have created in your set_facts.

## Optional extra

Create a file containing the content of the variables obtained.  You can use either **lineinfile** module, or **copy** using the **content** attribute.

If you use the **copy** module you can use content to write lines as follows:

```yaml
  - name: Write data
    ansible.builtin.copy:
      dest: /tmp/mydata
      content: |
        "{{ variable1 }}"
        "{{ variable2 }}"
```

The above code would write the data to the database server, so the /tmp/mydata would be on that server.  Let's change that so that the data is written back to the controller.

To do this Ansible has a directive called **delegate_to:** where you can supply an IP address or hostname to delegate to.  However, you will need to have SSH access to the host to perform the delegate to.  The **controller** will be localhost in the event of our running the code, so we can delegate to 127.0.0.1 to have the file written to the controller as follows:

```yaml
  - name: Write data
    ansible.builtin.copy:
      dest: /tmp/mydata
      content: |
        "{{ variable1 }}"
        "{{ variable2 }}"
    delegate_to: 127.0.0.1
```

The above will write the /tmp/mydata file on the server that is running the playbook.  The 127.0.0.1 refers to the server running the playbook not the server you are provisioning.