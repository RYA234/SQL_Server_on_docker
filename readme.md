
# 


# 開発環境
名称|version|説明
---|-------|----
Windows|10|開発環境のOS
Docker|知らん|コンテナ型仮想環境
SQLServer|2022 developper Edition  | データべース
tSQLt|V1.0.8083.3529|SQLServerのテストフレームワーク
VisualStudio|2022 community| IDE


# 配置図





# 始め方


```bash
# コンテナ構築
docker-compose build

docker-compose up -d


# dockerコンテナ入り方
docker-compose exec -it sql_server_db bash


# バージョン確認　コンテナ内で実行
/opt/mssql-tools18/bin/sqlcmd　-q "SELECT @@VERSION"

# SQL_Serverに入る コンテナ内で実行
/opt/mssql-tools18/bin/sqlcmd -U sa -P user@12345 -C

# コマンドからクエリ文を実行する
/opt/mssql-tools18/bin/sqlcmd -U sa -P user@12345 -C -Q "SELECT @@VERSION"

#  sqlファイルからクエリを実行する
/opt/mssql-tools18/bin/sqlcmd -U sa -P user@12345 -C -i /usr/src/docker/src/sample.sql

```

# tSQLtの導入

```db-init.sh
/opt/mssql-tools18/bin/sqlcmd -U sa -P user@12345 -C -i /usr/src/docker/src/tSQLt_setting/PrepareServer.sql
/opt/mssql-tools18/bin/sqlcmd -U sa -P user@12345 -C -i /usr/src/docker/src/tSQLt_setting/Example.sql
/opt/mssql-tools18/bin/sqlcmd -U sa -P user@12345 -C -i /usr/src/docker/src/tSQLt_setting/tSQLt.class.sql
/opt/mssql-tools18/bin/sqlcmd -U sa -P user@12345 -C -i /usr/src/docker/src/tSQLt_setting/createClass.sql
/opt/mssql-tools18/bin/sqlcmd -U sa -P user@12345 -C -Q "CREATE DATABASE main;"

```



# 参考

https://qiita.com/nozakita/items/c55e5fac3fc0364f42f5

aliasコマンド
https://qiita.com/yukachin0414/items/1aff8f70809c80d96de0

tSQLt

https://tsqlt.org/