.. _enabling-threads:

===============================================================================
Enabling Encryption Threads
===============================================================================

When the :variable:`default_table_encryption` system variable is set to ``ON``,
|InnoDB| tablespaces and schemas are encrypted. For single tablespaces, verify the ``ENCRYPTION`` option using the ``INFORMATION_SCHEMA.TABLES`` and ``CREATE_OPTIONS`` settings.

.. code-block:: MySQL

    mysql> SET GLOBAL innodb_encryption_threads=10;

    mysql> SET default_table_encryption=ON;

    mysql> CREATE TABLESPACE `ts_sample`
           ADD DATAFILE '/Volumes/ext1/mysql_datafiles/ts_sample.ibd'
           ENGINE=InnoDB;

    mysql> CREATE TABLE t1 (
        id int PRIMARY KEY,
        str varchar(50)
        );

    mysql> SELECT TABLE_SCHEMA, TABLE_NAME, CREATE_OPTIONS FROM INFORMATION_SCHEMA.TABLES WHERE CREATE_OPTIONS LIKE '%ENCRYPTION%';

    +---------------------------+------------------+--------------------+
    | TABLE_SCHEMA              | TABLE_NAME       | CREATE_OPTIONS     |
    +---------------------------+------------------+--------------------+
    | ts_sample                    | t1               | ENCRYPTION="Y"     |
    +---------------------------+------------------+--------------------+


When :variable:`default_table_encryption` system variable is set to ``ON``, you
can create unencrypted tables by adding ``ENCRYPTION="N" to the ``CREATE
TABLE`` statement or ``ALTER TABLE`` statement.

.. code-block:: MySQL

    mysql> SET GLOBAL innodb_encryption_threads=10;

    mysql> SET default_table_encryption=ON;

    mysql> CREATE TABLESPACE `ts_sample`
           ADD DATAFILE '/Volumes/ext1/mysql_datafiles/ts_sample.ibd'
           ENGINE=InnoDB;

    mysql> CREATE TABLE t1 (
        id int PRIMARY KEY,
        str varchar(50)
        ) ENCRYPTED=N;

    mysql> SELECT TABLE_SCHEMA, TABLE_NAME, CREATE_OPTIONS FROM INFORMATION_SCHEMA.TABLES WHERE CREATE_OPTIONS LIKE '%ENCRYPTION%';

    +---------------------------+------------------+--------------------+
    | TABLE_SCHEMA              | TABLE_NAME       | CREATE_OPTIONS     |
    +---------------------------+------------------+--------------------+
    | ts_sample                    | t1               | ENCRYPTION="N"     |
    +---------------------------+------------------+--------------------+

.. note::

    When `default_table_encryption` is set to ``ON``, you must set the
    `innodb_encryption_threads` to a non-zero value.

