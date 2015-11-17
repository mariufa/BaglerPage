# BaglerPage
- First a credentials.txt is required in the project root, and should look like:
``` 
 user:username
 db:databasName
 table:tableName
```
- Postgresql: 
``` 
$ sudo apt-get install postgreql
```
- Optional remove startup scripts for postgresql:
``` 
$ sudo update-rc.d -f postgresql remove
```
- The database script is set to use a user with no password. Hence the database can only be accessed locally. The postgresql might require username to be the same as unix username.
- baglerPage.py is the script with the flask part. To run on local network: $ python baglerPage.py.
- To reset database table, run: $ python resetDb.py
