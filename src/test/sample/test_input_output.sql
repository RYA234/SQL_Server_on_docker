-- Create Date: 2020-12-22 16:00:00
-- 別データベース名のプロダクトコードを呼んでテストするためのスクリプト
-- ストアドに追加する方法
-- /opt/mssql-tools18/bin/sqlcmd -U sa -P user@12345 -C -i /usr/src/docker/src/test/sample/test_input_output.sql
-- ↓↓テストの実行コマンド
-- /opt/mssql-tools18/bin/sqlcmd -U sa -P user@12345 -C -Q "USE [tSQLt_Example] EXEC tSQLt.Run 'testApp'"
-- ;

USE [tSQLt_Example]
GO

CREATE OR ALTER PROCEDURE testApp.[test_input_output_success]
AS
BEGIN
	DECLARE	@expected int; SET @expected =1;
	DECLARE	@actual int;

	EXEC	productg.dbo.[input_pass_output]
			@inputValue = 1,
			@outputValue = @actual OUTPUT

	EXEC tSQLt_Example.tSQLt.AssertEquals @expected, @actual;
END
GO


USE [tSQLt_Example]
GO

CREATE OR ALTER PROCEDURE testApp.[test_input_output_failure]
AS
BEGIN
	DECLARE	@expected int; SET @expected =0;
	DECLARE	@actual int;

	EXEC	productg.dbo.[input_pass_output]
			@inputValue = 1,
			@outputValue = @actual OUTPUT

	EXEC tSQLt_Example.tSQLt.AssertNotEquals @expected, @actual;
END
GO