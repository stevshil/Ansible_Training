# Files

In the earlier sections we saw how we could create a file or modify a file using the **lineinfile** module, and supplying it with different attributes depending on whether we were creating or modifying.

It is also possible to copy files on to the node and have content that is static, or might need to be changed as a file rather than a configuration.

Let's demonstrate this by making our index.html file and actual file instead of content.

## Using static file content

First let us set up a directory called **files**.

```sh
mkdir files
```

Inside this directory we will create the **index.html** file.

```sh
nano files/index.html
```

Add the following content to the file:

```html
<html>
    <body>
        <h1>Welcome to Ansible</h1>
        <p>This is the static index file</p>
    </body>
</html>
```

Save the file.  With nano it is **CTRL+X**, then follow the instructions.

Now we need to edit the webserver.yml file and change the following code:

```yaml
    - name: Create index file
      ansible.builtin.lineinfile:
        path: /var/www/html/index.html
        line: "{{ web_page_content }}"
        create: yes
        group: root
        owner: root
```

We will change this to using the **copy** module, https://docs.ansible.com/ansible/latest/collections/ansible/builtin/copy_module.html.

```yaml
    - name: Create index file
      ansible.builtin.copy:
        src: files/index.html
        dest: /var/www/html/index.html
        group: root
        owner: root
        mode: 0644
```

Save the playbook and run it.

You should now see that the original lines of text are not proper HTML.  Our file was copied from the files directory into the **dest** value on the node.