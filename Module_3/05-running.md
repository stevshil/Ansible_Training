# Running playbooks

As you have seen already we are able to run our playbook by simply specifying the name of the playbook to run.

```sh
ansible-playbook webservers.yml
```

There are many options we can also supply to the **ansible-playbook** command, most of which you can find out by running:

```sh
ansible-playbook --help
```

## Checking syntax

We can check the syntax of our playbook without running it using:

```sh
ansible-playbooks --syntax-check
```

This command will ensure that there is:

* YAML formatting
* Module names

It does not check:

* Attribute keys
* Variable brackets {{ }}

Handy for a quick check and to make sure the code is laid out correctly.  This command is useful in a GitHub actions or Jenkins pipeline to ensure syntax does not break the build.

## Checking what will happen

* https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_checkmode.html

If you have already ran a playbook and then made modifications, you can use **--check** to simultate what will happen if you actually run the playbook.

Check mode can allow tasks to still run based on setting the **check_mode** attribute in your playbook against those tasks that you want to actually run if **--check** is called.

When you run the command it will look like it has made the change, but it has not unless the **check_mode** has been set for a task to do so.

This command can also be useful if you want to run the playbook, but check for actual errors in the run.

```sh
$ ansible-playbook --check webservers.yml
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

TASK [Edit hosts file] *************************************************************************************************
ok: [web01]

RUNNING HANDLER [Restart Apache] ***************************************************************************************
changed: [web01]

PLAY RECAP *************************************************************************************************************
web01                      : ok=7    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

You'll notice from the output that it claims 2 changes, but because check was set the change was not made.  The 2 changes would have been the port number for Apache and the handler being triggered to restart the service.

## File content

What about file content?

**--check** only checks tasks, but if the content of a static or template file has changed you may also want to know what the difference is in those files.

For example, if we made a change to the **index.html.j2** file and added another line, then we would need to add **--diff** to our check to identify what would change.

Here is the command being ran against our webservers.yml playbook where an extra line has been added to the index.html.j2 file:

```sh
$ ansible-playbook --check --diff webservers.yaml
[WARNING]: Found both group and host with same name: controller

PLAY [webservers] ******************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************
ok: [web01]

TASK [Install Apache] **************************************************************************************************
ok: [web01]

TASK [Create index file] ***********************************************************************************************
--- before: /var/www/html/index.html
+++ after: /home/ansible/.ansible/tmp/ansible-local-10579i5ll381/tmppe2id_rz/index.html.j2
@@ -4,5 +4,6 @@
     <h3>Hosted on 192.168.1.186
     <p>192.168.1.186</p>
     <p>This is the static index file</p>
+    <p>One more line</p>
   </body>
 </html>

changed: [web01]

TASK [Set port number 80] **********************************************************************************************
--- before: /etc/httpd/conf/httpd.conf (content)
+++ after: /etc/httpd/conf/httpd.conf (content)
@@ -42,7 +42,7 @@
 # prevent Apache from glomming onto all bound IP addresses.
 #
 #Listen 12.34.56.78:80
-Listen 8080
+Listen 80

 #
 # Dynamic Shared Object (DSO) Support

changed: [web01]

TASK [Start and Enable Apache] *****************************************************************************************
ok: [web01]

TASK [Edit hosts file] *************************************************************************************************
ok: [web01]

RUNNING HANDLER [Restart Apache] ***************************************************************************************
changed: [web01]

PLAY RECAP *************************************************************************************************************
web01                      : ok=7    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

You'll notice in the output a file **diff** occuring and the output is very similar to running a Linux **diff** against 2 files.

## Deeper checking

You can perform more detailed scans of your Ansible playbooks by using **ansible-lint** command.  This command is not installed by default with Ansible.

This command requires Python3.9 or above.

Depending on how you installed Ansible, will depend on how you install ansible-lint.  If you installed using packages, using commands such as **apt**, **dnf** or **yum** then you should use these, e.g.

```sh
$ apt -y install ansible-lint
```

If you installed using Python **pip** then install with:

```sh
$ pip install ansible-lint
```

You can see what options ansible-lint has by using:

```sh
$ ansible-lint --help
```

Let's check our playbook for Ansible syntax and style.

```sh
$ ansible-lint -f full webservers.yaml
WARNING  Listing 5 violation(s) that are fatal
name[play]: All plays should be named.
webservers.yaml:1

yaml[trailing-spaces]: Trailing spaces
webservers.yaml:11

yaml[octal-values]: Forbidden implicit octal value "0644"
webservers.yaml:18

yaml[truthy]: Truthy value should be one of [false, true]
webservers.yaml:32

yaml[octal-values]: Forbidden implicit octal value "0644"
webservers.yaml:40

Read documentation for instructions on how to ignore specific rule violations.

                  Rule Violation Summary
 count tag                   profile rule associated tags
     1 name[play]            basic   idiom
     2 yaml[octal-values]    basic   formatting, yaml
     1 yaml[trailing-spaces] basic   formatting, yaml
     1 yaml[truthy]          basic   formatting, yaml

Failed: 5 failure(s), 0 warning(s) on 1 files. Last profile that met the validation criteria was 'min'.
```

As you can see, not perfect, but doesn't actually stop us, so the majority is styling and convention.

This is another command that if you are interested in keeping styling and having perfect playbooks, you should run in your CI system such as Jenkins or GitHub Actions, and if you have any failures you should fail the request to merge (pull request).

Let's fix these styling issues together in the class and then re-run the lint to clear the failures.

## Verbose

It is possible to get further information from Ansible by including **-v** or **--verbose**.

Verbose has multiple possible options depending on the detail you need.  From the help page:

Causes Ansible to print more debug messages. Adding multiple -v will increase the verbosity the builtin plugins currently evaluate up to -vvvvvv. A reasonable level to start is -vvv, connection debugging might require -vvvv.