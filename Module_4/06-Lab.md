# On your own

Revist the playbooks for:

* databases.yml
* webservers.yml

For each of the playbooks create an agnostic version for the packages to be installed.

* Debian
  * apache2
    * This is also the same name for the service too
  * MariaDB
    * PyMySQL
      * python3-pymysql
    * mariadb-server
    * mariadb-client
* RHEL
  * httpd
    * Also the name of the service
  * MariaDB
    * PyMySQL
      * python3-PyMySQL
    * mariadb-server
    * mysql
      * For the client tools

For the Database RHEL will use /etc/my.cnf instead of /etc/mysql/mariadb.conf.d/50-server.cnf for the **bind-address** directive.  Although better still, is RHEL will default to all IPs, so you only need to set the **bind-address** if the system is of Debian os-family.  So create a condition that if the os-family is Debian that you set the bind-address.

For RHEL you will need to start the Database service as it will not do so by default.  Debian system do start by default.

## Optional extra

If you feel daring enough and think your playbook is good, then run the playbooks against both servers.

## Optional optional extra

Create the playbooks that will decomission your servers, removing the software for the database and webserver and removing any configuration files and directories.

Tag some of the actions so that you can call them separately if there are failures, e.g.

* configuration
  * To remove files and directories associated to the install
* packages
  * To remove the packages only