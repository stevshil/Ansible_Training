# Sensitive data

Since we are building and maintaining nodes and their software through code it is important to ensure that we do not leak:

* passwords
* SSL certificates
* SSH keys
* and other private data

into our Git repositories.

There are various solutions around this issues.  Some people prefer to keep their code and secrets together, but that means writing your own process to decode or decrypt the secret before the code can be ran.  Others may prefer to use a 3rd party service to store the secrets and have the system being configured call the service to obtain the secret when needed.

## Using a 3rd part service

If you are using the cloud then Amazon, Google and Microsoft all provide secret storage services within your cloud offering.  

* Amazon has KMS and AWS Secrets Manager
  * https://aws.amazon.com/secrets-manager/
* Google has Secret Manager
  * https://cloud.google.com/security/products/secret-manager
* Microsoft has Azure Key Vault
  * https://azure.microsoft.com/en-us/products/key-vault

With these services you integrate them into your system and set up variables within the service to obtain the secret during run time.  Most of these services tend to require the use of their own pipeline, an agent or API to access the service or some role based access control (RBAC) or policy applied to the system wishing to access the vault.

There are also non-cloud based services that you can build yourself such as:

* Hashicorp Vault
* Infiscal
* Cyberark

These systems require you to have some form of authentication between the server wishing to obtain the secret and the secret server itself.

Should I store my Ansible secrets in a remote Git repository, even if they're encrypted?

* If your repository is public you might choose not to store the secrets
  * People will attempt to brute force decrypt the files using ansible-vault
* If you repository is private but on the cloud
  * Check the legal bit to see what **private** actually entails
  * If the Git provider guarantees secrecy of your repository then you might choose to store them
* You have no faith in cloud provided storage
  * Use a locally hosted Git service such as GitLab
  * Make use of a service such as Hashicorp Vault hosted in your own infrastructure
    * Call the variables at runtime
    * Means you need to code this into your Ansible playbooks/roles
  * Have the controller pull all secrets during a play and destroy them after
    * Risky as all secrets would be stored on the server during run time
    * Perhaps only store those for the relevant play