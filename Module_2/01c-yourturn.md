# Now it's your turn

This time you get to work out how to do it yourself.  You've seen how to find the documentation for the modules, and how to construct the arguments for the modules.  We will tell you what we want, and you'll do the rest.

1. Remove the file **/tmp/hello_world**.
2. Download from the stephen-king-api books using [https://stephen-king-api.onrender.com/api/books](https://stephen-king-api.onrender.com/api/books) as the url and store the data in a file called **/tmp/stephen_king**
3. Replace all occurances of stephen-king with Stephen-King in the /tmp/stephen_king file that you have just downloaded
    * HINT: You'll need the **replace** module
4. Install the package **cowsay** or **emacs**
    Check that the package is installed;

    ```bash
    $ dpkg -l | egrep 'cowsay|emacs'  # For Debian based
    # or
    $ rpm -qa | egrep 'cowsay|emacs'  # For RHEL based
    ```

5. Add a new user to the system called **student** with the following attributes;
    * Home directory **/home/student**
    * Login shell/program **/bin/bash**
    * Add the user to the **training** group as a subsequent group

    **HINT:** Check that the user exists in /etc/passwd;
    ```bash
    grep student /etc/passwd
    ```
6. Uninstall emacs or cowsay
7. Delete the **student** user
8. Delete the training group