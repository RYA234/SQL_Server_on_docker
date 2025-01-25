-- Create Date: 2020-12-22 16:00:00
-- 第一引数の入力値を第二引数の出力値に設定するストアド
-- ストアドに追加する方法
-- /opt/mssql-tools18/bin/sqlcmd -U sa -P user@12345 -C -i /usr/src/docker/src/main/sample/input_output.sql
-- ↓↓テストの実行コマンド
-- /opt/mssql-tools18/bin/sqlcmd -U sa -P user@12345 -C -Q "USE [tSQLt_Example] EXEC tSQLt.Run 'testApp'"
-- 

USE [main]
GO

CREATE OR ALTER PROCEDURE dbo.input_pass_output
    @inputValue int,
    @outputValue int OUTPUT
AS
BEGIN
 SET @outputValue = @inputValue;
END
GO