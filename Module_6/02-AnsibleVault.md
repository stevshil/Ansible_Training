# Ansible Vault

Ansible has created a method to encrypt playbooks that contain sensitive data and decrypt for execution.

* https://docs.ansible.com/ansible/latest/vault_guide/index.html
* https://docs.ansible.com/ansible/2.8/user_guide/vault.html
* https://docs.ansible.com/ansible/latest/cli/ansible-vault.html
* https://www.digitalocean.com/community/tutorials/how-to-use-vault-to-protect-sensitive-ansible-data

Ansible Vault is a mechanism that allows encrypted content to be incorporated transparently into Ansible workflows.  A utility called ansible-vault secures confidential data, called secrets, by encrypting it on disk.

The **ansible** and **ansible-playbook** integrate decryption of content at runtime.

Ansible Vault works at the file level, encrypting the content of the entire file.  For the most part this should be files containing variables, and more improtantly those with variables.

Although many sites and organisations state that it is safe to commit your code to Git repositories after being encrypted with Ansible Vault, you should still decide how safe that is.

## Using Ansible Vault with password

First let's look at creating an encrypted secret.

Let's say we have a variables file called **db01.yml**, and in that file is the following:

```yaml
dbuser: root
dbpass: secret123
```

Now, we don't want these to be visible to anyone, so we can use Vault to encrypt the file as follows:

```sh
$ ansible-vault encrypt db01.yml
New Vault password:
Confirm New Vault password:
Encryption successful
```

At the password prompts we typed in and confirmed the password.  We are told encryption was successful.  The content of the file is now:

```sh
$ cat db01.yml
$ANSIBLE_VAULT;1.1;AES256
31373435663435373661363866363765313066343164363731626565363135363262616162363032
3038396564313266626566343334323639306133653138330a313938346431353831356236303033
33353833373466376163666435326238623536623666373262623836346536363236376237613365
6439383036653336660a656266626331396461386438663665313662613431336430326365343862
32343866346365383265356132653864393434613330663866643532393662613233
```

Totally unreadable and someone needs to know the password that the file was encrypted with.

To decrypt the file so that we can make a change to it we would:

```sh
$ ansible-vault decrypt db01.yml
Vault password:
Decryption successful
```

When you **cat** the file now you will see it unencrypted.

## Using Vault without a password

It would be tedious having to keep typing in the password, so you can create a file to store the password secret, and set a variable to where the secret password is stored.

Ansible vault will look in the current directory where the ansible commands are ran by default.

```sh
$ export ANSIBLE_VAULT_PASSWORD_FILE=~/.vaultpw
```

You would need to make sure that you set the password in the file that you specify, in plain text and make the permission **0600**.

Once this is done then running the **encrypt** and **decrypt** will not prompt for passwords.

**NOTE:** Do not store this file in Git.

## Let's do this for real

Now let's go and encrypt our **databases.yml** file in the **oursite/environment/dev/group_vars** directory.

1. Make sure you have created the **~/.vaultpw** file and added a password to it.
2. Export the ANSIBLE_VAULT_PASSWORD_FILE with your file containing the password.
3. Encrypt the file
    ```sh
    $ cd ~/oursite/environment/dev/group_vars
    $ ansible-vault encrypt databases.yml
    ```

4. Check that the file is encrypted
    ```sh
    cat databases.yml
    ```
5. Now run the playbook
    ```sh
    $ cd ~/oursite
    $ ansible-playbook -i environments/dev site.yml
    ```

You'll notice that the playbook runs as though we had not encrypted the file.  This is because Ansible have included the decrypt and encrypt features into the ansible commands, as mentioned earlier.

To prove this let's unset the ANSIBLE_VAULT_PASSWORD_FILE and run the playbook.

```sh
$ unset ANSIBLE_VAULT_PASSWORD_FILE
$ ansible-playbook -i environments/dev site.yml

......

TASK [apache : Edit hosts file] ****************************************************************************************
An exception occurred during task execution. To see the full traceback, use -vvv. The error was: ansible.errors.AnsibleParserError: Attempting to decrypt but no vault secrets found
fatal: [web01]: FAILED! => {"changed": false, "msg": "AnsibleParserError: Attempting to decrypt but no vault secrets found"}

PLAY RECAP *************************************************************************************************************
web01                      : ok=7    changed=0    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0
```

Ansible fails to decrypt as the password is not set.

We could pass the password at run time, which most organisations would prefer rather than leaving password files on servers.  The password is asked through a prompt, so won't be supplied on the command line.

If you wish to pass the password, then run the playbook as follows:

```sh
$ ansible-playbook --ask-vault-password -i environments/dev site.yml
Vault password:
```