# Install Controller

Now it's your turn.

Setting up a controller is the same as setting up the previous machine.  The key difference is that we will not do development directly on this system.  Instead we will use a Git repository, or copy our Ansible code base on to this server before running.

Use the previous exercise to remind yourself of the commands and steps.

## The steps

* Check if Python is already installed.
  * Install Python 3 if it is not installed
* Install git and pip
* Ensure that /usr/bin/python is linked to /usr/bin/python3
* Check that the commands are all installed and working by using the **--version** option to the commands
* Install Ansible
  * HINT:
    * Use apt for Debian systems
    * Use pip for RHEL systems
* Run the Ansible **ping** module to test Ansible is working and you receive the **pong** output.

## New steps

We now need to ensure that our server is capable of logging on to the other VMs that will be our nodes to be under Ansible orchestration.

### Create a new SSH key pair

### RHEL systems only

RHEL derived systems may not already have a **.ssh** directory for storing keys, so create one if it does not already exist;

```bash
mkdir ~/.ssh
chmod 700 ~/.ssh
```

### All systems

We need an SSH key pair that can be used by our user on the other servers.  Run the following command to generate the key pair;

```bash
ssh-keygen -f .ssh/ansible
```

**NOTE:** You will be prompted for a passphrase, so just press ENTER twice to set an empty passphrase.  The reason for no passphrase on the key is to make it easier for Ansible to work without having to set up agents first.  If we use automation servers such as Jenkins we can supply the SSH private key and password for it to work nicely.

2 files will be created in the ~/.ssh directory;
* ansible
  * This is the private key and should be kept safe at all costs
* ansible.pub
  * The public key that will be copied to all servers

### Configure SSH to ignore fingerprints

Ansible will fail to connect to new SSH hosts if the SSH fingerprint request is prompted.  To prevent this from happening and to enable new hosts to be managed do the following;

* Create a file called **~/.ssh/config**
  * This file allows you to configure the SSH client
* Our system may not have an editor, so we'll install one now;
  * Using the **nano** command we'll edit the configuration file.  However, nano is probably not installed.  If you prefer **vim** you can install that instead.
  
    ```bash
    sudo apt -y install nano # Debian
    sudo dnf -y install nano # RHEL
    ```
* Now create the file
    ```bash
    nano ~/.ssh/config
    ```
* In this file add the following lines
    ```
    HOST *
      StrictHostKeyChecking no
      UserKnownHostsFile /dev/null
      User ansible
      IdentityFile ~/.ssh/ansible
    ```
    * The above line prevent the SSH fingerprint, do not add hosts to known_hosts file, uses **ansible** username by default and uses the **~/.ssh/ansible** ssh key for the connection.

### Configuring the managed nodes

We need to have a user on the nodes we will be managing with Ansible that will run on behalf of the Ansible service and have **sudo** access.

Log on to each of the final 2 machines in turn and perform the following commands;

* Add the user **ansible**

    ```bash
    sudo useradd -m ansible
    sudo passwd ansible
    # Set the ansible password to secret123
    ```
* Create the .ssh directory for the **ansible** user

    ```bash
    sudo mkdir /home/ansible/.ssh
    sudo chown ansible:ansible /home/ansible/.ssh
    sudo chmod 700 /home/ansible/.ssh
    ```
* Now allow the user unrestricted sudo access
  * Using the **nano** command we'll edit the configuration file.  However, nano is probably not installed.  If you prefer **vim** you can install that instead.
  
    ```bash
    sudo apt -y install nano # Debian
    sudo dnf -y install nano # RHEL
    ```

  * Now we can edit a new file called **/etc/sudoers.d/90-ansible**
    ```bash
    sudo nano /etc/sudoers.d/90-ansible
    ```
  * In the file add the following line;
    ```
    ansible ALL = (ALL) NOPASSWD: ALL
    ```
  * Save the file using
    * CTRL+X
    * Y
    * Press the ENTER key to accept the default filename

&#x26a0;&#xfe0f; **NOTE:** Make sure you type in the file content exactly otherwise you'll lock yourself out.

Repeat for the other machine and then return to your Ansible controller system.

### Now we copy the key to the other servers

Back on our Ansible controller.

This command will copy your SSH public key to the other servers.  For this we need to make sure that our user is already configured on the remote servers and has a password we can use.

```bash
ssh-copy-id -i ~/.ssh/mykey ansible@node1
```

Replace **node1** with the hostname or IP address of one of the managed nodes, then repeat the command for the other node.

You will be prompted for the ansible user password that you created on the other 2 nodes.

### Check that ssh works with the key

Do the following for both of your managed nodes.

```bash
ssh ansible@node1
```

There should be no password prompt and you should log on to the other host.

Type **exit** to leave that host and try with the other node.

You should also be able to ssh without specifying the username based on our ~/.ssh/config file, so try;

```bash
ssh node1
```

Exit from this node so you are back on your controller.