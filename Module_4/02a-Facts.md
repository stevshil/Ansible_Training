# Ansible Facts and Register

It is possible to create your own variables in Ansible using the **set_fact** module.  Unlike the **vars** section, **set_fact** is a runtime variable declaration, so it is a task rather than a special section.

Let's do a simple set_fact, to see how it is configured.

## Simple set_fact

Here we will create a simple playbook that will allow us to set a fact with a static value and then display that using **debug** module.

```yaml
- name: Working with Facts
  hosts: controller

  tasks:
    - name: Set the fact for my_name
      ansible.builtin.set_fact:
        my_name: Steve
        hobbies:
          - cycling
          - squash
          - reading

    - name: Show name
      ansible.builtin.debug:
        msg: 
          - "Your name is {{ my_name }}"
          - "Your hobbies are {{ hobbies }}"
```

Here we can see that we have a single value variable and a list.  Both of which are printed out using the **debug** **msg** action.

## Dynamic variables

You may often require the creation of a variable from a value captured from another module that you have already executed which returned output that you need to fulfil further modules.

Let's take a look at how this can be achieved.

For this to work we need a command that will return some output.  A command that allows us to do this is **shell**.  The **shell** command allows us to run command line commands in Ansible.

* https://docs.ansible.com/ansible/latest/collections/ansible/builtin/shell_module.html

For the example we will use the id command to grab user details and then create a **uid** and **gid** fact.

```yaml
- name: Create dynamic variabls
  hosts: controller

  tasks:
    - name: Run id command
        ansible.builtin.shell:
          cmd: id -a
        register: id_data

    - name: Show captured data
        ansible.builtin.debug:
          msg: "Showing {{ id_data }}"
```

The above shows how the data is captured in the variable **id_data**.  This variable contains the output of what Ansible returns.  From the output we can see that the **shell** module returns the following attributes (also shown in the documentation):

* changed
* stdout
* stderr
* rc
* cmd
* start
* end
* delta
* msg
* stdout_lines
* stderr_lines
* failed

The stdout and stderr are strings, whilst stdout_lines and stderr_lines are arrays of strings, where each line of output is an element of the array.

We can change our code so that our **id_data** variable contains only the **stdout** data, which is what we are interested in.

```yaml
- name: Create dynamic variabls
  hosts: controller

  tasks:
    - name: Run id command
        ansible.builtin.shell:
          cmd: id -a
        register: id_data

    - name: Show captured data
        ansible.builtin.debug:
          msg: "{{ id_data.stdout }}"
```

You'll notice this time we include the **stdout** after the **id_data** in object notation form, using the dot.  We also removed the **Showing** as we're about to manipulate the string to get the data we need.

Let's now split the **stdout** based on spaces.  The code following is only the last task:

```yaml
    - name: Show captured data
        ansible.builtin.debug:
          msg: "{{ id_data.stdout | split(' ') }}"
```

Notice the use of the pipe symbol | which allows us to use filters after the variable to perform certain actions.

The following Ansible documentation shows different methods for manipulating data:

* https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_filters.html
* https://docs.ansible.com/ansible/latest/playbook_guide/complex_data_manipulation.html

In our above example we have made use of the **split** function, which has broken down our output into separate lines.  The output will now look like:

```sh
TASK [Show captured data] **********************************************************************************************
ok: [controller] => {
    "msg": [
        "uid=1000(ansible)",
        "gid=1000(ansible)",
        "groups=1000(ansible),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),105(lxd)"
    ]
}
```

You'll notice now that we have **uid=**, **gid=**, etc as separate values.

We can now break this down further, and given that we know that **uid** will always be first make use of that array index and split based on the **=**:

```yaml
    - name: Show captured data
      ansible.builtin.debug:
        msg: "{{ ((id_data.stdout | split(' '))[0] | split('='))[1] }}"
```

Above we have made use of brackets to order the precedence of execution.  You'll notice that our original command with the split is encased in ( ) and has [0] following it to grab just the **uid** data.  We then split the **uid** based on the **=** symbol and grab the 2nd element which is the id and name.

To get just the user ID we would do:

```yaml
    - name: Show captured data
      ansible.builtin.debug:
        msg: "{{ (((id_data.stdout | split(' '))[0] | split('='))[1] | split('('))[0] }}"
```

This looks very complicated and we could make it easier by assigning each phase to a variable.  This will return the value 1000.

Now we know how to obtain the values we can create the facts.

Here is the code to create the **uid** and **gid** facts:

```yaml
- name: Create dynamic variabls
  hosts: controller

  tasks:
    - name: Run id command
        ansible.builtin.shell:
          cmd: id -a
        register: id_data
    
    - name: Set uid variable
      set_fact:
        uid: "{{ (((id_data.stdout | split(' '))[0] | split('='))[1] | split('('))[0] }}"
        gid: "{{ (((id_data.stdout | split(' '))[1] | split('='))[1] | split('('))[0] }}"

    - name: Show captured data
        ansible.builtin.debug:
          msg:
            - "User ID: {{ uid }}"
            - "Group ID: {{ gid }}"
```

The above is the complete code to obtain the 2 values we required at run time.