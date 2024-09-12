# Follow the instructions

It's now your turn.  This time we'll provide typed instructions and let you know what happend.

1. Run the following command to add a line to the /tmp/hello_world that we created earlier
    
    ```bash
    ansible localhost -m lineinfile -a "line='Hello Again' path=/tmp/hello_world insertafter='Hello World'"
    ```

    * This time we've removed **create** as the file exists.  If we leave **create** in it will fail.
    * We have changed **line** so that we add new text to the file.
    * We have added **insertafter** to tell Ansible which line of text to insert after.  This can be a regular expression (regex).

    View the content of the file;
    ```bash
    $ cat /tmp/hello_world
    Hello World
    Hello Again
    ```

2. Let's use a regex to do a replacement;

    ```bash
    ansible localhost -m lineinfile -a "line='My reg ex' path=/tmp/hello_world insertafter='o.ld'"
    ```

    * This time we have included a full stop (period) between o and l to mean any single character in the **insertafter**.
    * This places the **My reg ex** line between Hello World and Hello Again since we're matching W**o**r**ld**

    View the content of the file;
    ```bash
    $ cat /tmp/hello_world
    Hello World
    My reg ex
    Hello Again
    ```

3. Change the permissions on the file /tmp/hello_world to rwxr--r--

    ```bash
    ansible localhost -m ansible.builtin.file -a "path=/tmp/hello_world mode=744"
    ```

    For this you'll receive the following output if it worked;

    ```json
    localhost | CHANGED => {
        "changed": true,
        "path": "/tmp/hello_world",
        "state": "absent"
    }
    ```

    Run the command;
    ```bash
    $ ls -l /tmp/hello_world
    -r-xr--r-- 1 anisble ansible 31 May  4  18:00 /tmp/hello_world
    ```

    **NOTE:** the data and time will be different, but we are interested in the permissions.

4. Install the package that will allow **netstat** to be used.  This is normally in net-tools package.  For this we will use the Ansible **package** command, which is platform agnostic, so as long as the package name is the same it will work on Ubuntu/Debian, Red Hat, etc.

    ```bash
    ansible localhost -m ansible.builtin.package -a "name=net-tools state=latest" --become
    ```

    &#x26a0;&#xfe0f; **NOTE:** We have used the **--become** for this to elevate our privilege to root.

    You should now be able to run the **netstat** command on the system, e.g.;

    ```bash
    netstat -tln
    ```