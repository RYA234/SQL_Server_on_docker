#start SQL Server, start the script to create/setup the DB
#wait for the SQL Server to come up
sleep 10s

echo "↓↓↓↓↓running set up script↓↓↓↓↓"

# tSQLt Setting
/opt/mssql-tools18/bin/sqlcmd -U sa -P user@12345 -C -i /usr/src/docker/src/tSQLt_setting/PrepareServer.sql
/opt/mssql-tools18/bin/sqlcmd -U sa -P user@12345 -C -i /usr/src/docker/src/tSQLt_setting/Example.sql
/opt/mssql-tools18/bin/sqlcmd -U sa -P user@12345 -C -i /usr/src/docker/src/tSQLt_setting/tSQLt.class.sql
/opt/mssql-tools18/bin/sqlcmd -U sa -P user@12345 -C -i /usr/src/docker/src/tSQLt_setting/createClass.sql
/opt/mssql-tools18/bin/sqlcmd -U sa -P user@12345 -C -Q "CREATE DATABASE main;"

echo "↑↑↑↑↑running set up script↑↑↑↑↑"