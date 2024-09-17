# Including playbooks

Reference: https://docs.ansible.com/ansible/5/collections/ansible/builtin/include_module.html

In the Playbook and Roles section we looked at how to create a role.  We made mention that it was possible to have more than just the **main.yml** file we could have other files that could be included into the main.yml file but provide a specific purpose.

The reason for separating out files in the tasks and handlers is to:

* Run sections based on a conditional outcome
  * You may have multiple tasks to execute and rather than place a condition on each task place the condition on the file
* Run based on different actions for different operating systems

The reason for different files is that there may be a lot of tasks you need to run.

We can include a full list of tasks, or individual tasks.

Includes execute at the point they are in the playbook or tasks files.

Let's revisit our Apache role, where we had the different package and directories for the different operating systems.  We could perform the operating system specific actions in different files.  Let's say ubuntu.yml and rhel.yml.

Here's the current **tasks** code:

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

The above shows our use of the variables to drive whether we install httpd or apache2.  Let's revisit this by using separate files to perform the **package** command, and also Ubuntu would need to perform an **apt update** before install, which we have not performed yet.

Change to ~/oursite/roles/apache/tasks directory.

Create a file called **ubuntu.yml** and add the following content:

```yaml
- name: Update apt cache
  ansible.builtin.apt:
    update_cache: true

- name: Install Apache
  ansible.builtin.package:
    name: apache2
    state: present
```

Create another file called **rhel.yml** and in that file add the following:

```yaml
- name: Install Apache
  ansible.builtin.package:
    package: httpd
    state: present
```

The files look similar, but we have the extra instruction in the Ubuntu.  We've also done away with the set_fact.

Now we change the **main.yml** file to conditionally include the **ubuntu.yml** and **rhel.yml** files based on the operating system.

Remove the following lines from **main.yml**

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
```

These are at the top of the file.

We will now insert the following:

```yaml
- name: Install for Ubuntu
  include: ubuntu.yml
  when: when: ansible_facts['os_family'] == 'Debian'

- name: Install for RHEL
  include: rhel.yml
  when: ansible_facts['os_family'] == 'RedHat'
```

Now when our role is executed it will run the tasks within the sub-task files.

Using this technique makes it easier to manage code changes.