# MySQL Installation Instructions
**Last Update: 12-28-2022**


Guide: https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04

1. Install MySQL

```
sudo apt install mysql-server
```

2. login as root

```
sudo mysql
```

3. Change the root account to use a password

```
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
exit;
```

4. Perform MySQL Secure installation process as sudo

```
sudo mysql_secure_installation
```

5. log back in as root using the temp password

```
mysql -u root -p
```

6. switch the root account back to auth_sockets so that you have to ssh into the server in order to perform admin functions with MySQL.

```
ALTER USER 'root'@'localhost' IDENTIFIED WITH auth_socket;
```

7. Edit the /etc/mysql/mysql.conf.d/mysqld.cnf file to allow external users to login to the SQL Server

8. Add user accounts and grant privileges.
