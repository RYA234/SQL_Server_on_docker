-- Create Date: 2020-12-22 16:00:00
-- Assertionのみのテスト　tSQLtが実行できるかを確認するためのスクリプト
-- ストアドに追加する方法
-- /opt/mssql-tools18/bin/sqlcmd -U sa -P user@12345 -C -i /usr/src/docker/src/test/sample/assertion_check.sql
-- ↓↓テストの実行コマンド
-- /opt/mssql-tools18/bin/sqlcmd -U sa -P user@12345 -C -Q "USE [tSQLt_Example] EXEC tSQLt.Run 'testApp'"
-- ;

USE [tSQLt_Example]
GO

CREATE OR ALTER PROCEDURE testApp.[test_give_test]
AS
BEGIN
	DECLARE	@expected int; SET @expected =0;
	DECLARE	@actual int;SET @actual =0;
	EXEC tSQLt_Example.tSQLt.AssertEquals @expected, @actual;
END
GO