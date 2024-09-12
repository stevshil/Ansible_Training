# Local server installation

This node will be used for performing localhost Ansible runs and trying things out generally on a machine.

In most cases we would create a development environment and run our modifications from a Git branch to ensure there are no errors.  If our Ansible run in Developement works then we would submit our Git Pull Request to merge the UAT or Production depending on your process.

## Preparing the host

Pick one of your nodes to be your trial machine where you'll be able to code and test things against that host without having to apply SSH keys, etc.

Log in to this host with the user that has **SUDO** access as instructed by your trainer.

Now we will install Python, Pip and Ansible.

These labs are for Debian/Ubuntu and Red Hat (RHEL) derived Linux systems, so where the commands differ we will specify the operating system before.

## Installing Python

Most Linux cloud VMs generally have Python 3 installed, but just to ensure it is and up to date we will still go through the motions.

If you're using Ansible on-premise then you would add the Python and Pip install steps into your Kickstart process or disk image to save having to install it on your Ansible servers.

First check if Python is installed with;
```bash
which python3
```

### Debian

Most Ubuntu servers and systems will have Python 3 installed by default.

```bash
sudo apt -y install python3
sudo apt -y install git python3-pip
```

### RHEL

```bash
sudo dnf -y install python3.11 # For RHEL system you'll need to specify the version
# Use dnf search python to find available versions
sudo dnf -y install git python3.11-pip
```

### All systems

Check that Python, pip and Git are working.

Ideally Ansible will want to call **python** rather than **python3**.  To do this we need to create a link to the python3 command.

First find where Python3 is installed

```bash
which python3
```

This should return something similar to
```bash
/usr/bin/python3
```

Create the symbolic link
```bash
sudo ln -s /usr/bin/python3 /usr/bin/python
```

### RHEL only
The pip command is not linked by default.
```bash
sudo ln -s /usr/bin/pip3.11 /usr/bin/pip
```

Check the command works
```bash
python --version
```

Will return something similar to
```bash
Python 3.11.6
```

Check that pip works
```bash
pip --version
```

Should return something similar to;
```bash
pip 23.2 from /usr/lib/python3/dist-packages/pip (python 3.11)
```

Check that git works;
```bash
git --version
```

Returns something similar to;
```bash
git version 2.40.1
```

## Install Ansible

### Debian

For Debian based system you will get a warning if you try to sudo install ansible, warning about package issues.  Instead we will install it with **apt**.

```bash
sudo apt -y install ansible
```

### RHEL

```bash
sudo pip3 install ansible
```

### All systems

Check the installation;

```bash
ansible --version
```

This should return something similar to below;
```
ansible [core 2.14.9]
  config file = None
  configured module search path = ['/home/ansible/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python3/dist-packages/ansible
  ansible collection location = /home/ansible/.ansible/collections:/usr/share/ansible/collections
  executable location = /usr/bin/ansible
  python version = 3.11.6 (main, Oct  8 2023, 05:06:43) [GCC 13.2.0] (/usr/bin/python3)
  jinja version = 3.1.2
  libyaml = True
```

## A quick Ansible command

We'll discuss this in more detail later, but let's just try the **ansible** command to perform a ping against localhost.

```bash
ansible localhost -m ping
```

The above can also be written as;

```bash
ansible localhost -m ansible.builtin.ping
```

The output will be;
```json
localhost | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```

The second version can only be used from Ansible version 2.10 onward, where as the first method can be used on all versions.