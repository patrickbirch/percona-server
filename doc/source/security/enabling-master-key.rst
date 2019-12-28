.. _enabling-master-key::

==============================================================================
Enabling Master Key Encryption
==============================================================================

To enable Master key vault encryption, the user must have
``SYSTEM_VARIABLES_ADMIN
<https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_system-variables-admin>`_
privileges.

Add the following statements to my.cnf:

.. code_block:: MySQL

    [mysqld]
    early-plugin-load="keyring_valut=keyring_valut.so"
    loose-keyring_value_config="/home/mysql/keyring_vault.conf"

Restart MySQL.

You can also use ``SET`` to configure the
:variable:``default_table_encryption`` variable.

.. code-block:: MySQL

    mysql> SET GLOBAL default_table_encryption=ON;

The file_per_table tablespace inherits the schema's default encryption
setting, unless you explicitly define encryption in the ``CREATE TABLE``
statement.

An example of the ``CREATE TABLE`` statement:

.. code-block:: mysql

   mysql> CREATE TABLE myexample (id INT, mytext varchar(255)) ENCRYPTION='Y';

An example of an ``ALTER TABLE`` statement.

.. code-block:: MySQL

    mysql> ALTER TABLE myexample ENCRYPTION='Y';

If the ``ENCRYPTION`` clause in the `ALTER TABLE` statement is not added, the
table's encryption state does not change.

.. seealso::

  |MySQL| Documentation:
  -  `File-Per-Table Encryption <https://dev.mysql.com/doc/refman/8.0/en/innodb-data-encryption.html#innodb-data-encryption-enabling-disabling>`__

  -   MySQL Documentation: default_table_encryption
      https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html

.. rubric:: Encrypting System Tablespace

To enable system tablespace encryption, edit the my.cnf file with the following:

    * Add ``innodb_sys_tablespace_encrypt``
    * Edit the ``innodb_sys_tablespace_encrypt`` value to "ON"

System tablespace encryption can only be enabled with the ``--initialize``
option.

You enable encryption for an undo log data by adding the following line to the
my.cnf file:

.. code-block:: MySQL

  [mysqld]
  innodb_undo_log_encrypt=ON

.. rubric:: Binary logs


.. code-block:: MySQL

    binlog_encryption=ON


Verifying the Encryption Setting
----------------------------------

For single tablespaces, verify the ENCRYPTION option using
`INFORMATION_SCHEMA.TABLES` and the `CREATE OPTIONS` settings.

.. code-block:: MySQL

    mysql> SELECT TABLE_SCHEMA, TABLE_NAME, CREATE_OPTIONS FROM
           INFORMATION_SCHEMA.TABLES WHERE CREATE_OPTIONS LIKE '%ENCRYPTION%';

    +----------------------+-------------------+------------------------------+
    | TABLE_SCHEMA         | TABLE_NAME        | CREATE_OPTIONS               |
    +----------------------+-------------------+------------------------------+
    |sample                | t1                | ENCRYPTION="Y"               |
    +----------------------+-------------------+------------------------------+

A ``flag`` field in the ``INFORMATION_SCHEMA.INNODB_TABLESPACES`` has the bit
number 13 set if the tablespace is encrypted. This bit can be checked with the
``flag & 8192`` expression with the following method:

.. code-block:: mysql

    SELECT space, name, flag, (flag & 8192) != 0 AS encrypted FROM
    INFORMATION_SCHEMA.INNODB_TABLESPACES WHERE name in ('foo', 'test/t2', 'bar',
    'noencrypt');

.. admonition:: Output

   .. code-block:: guess

      +-------+-----------+-------+-----------+
      | space | name      | flag  | encrypted |
      +-------+-----------+-------+-----------+
      |    29 | foo       | 10240 |      8192 |
      |    30 | test/t2   |  8225 |      8192 |
      |    31 | bar       | 10240 |      8192 |
      |    32 | noencrypt |  2048 |         0 |
      +-------+-----------+-------+-----------+
      4 rows in set (0.01 sec)

:Availabiliity: This feature is **Experimental**.

Encrypted table metadata is contained in the
``INFORMATION_SCHEMA.INNODB_TABLESPACES_ENCRYPTION`` table.

You must have the ``Process`` privilege to view the table information.

.. note::

    This table is **Experimental** and may change in future releases.

.. code-block:: MySQL

  >desc INNODB_TABLESPACES_ENCRYPTION:

  +-----------------------------+--------------------+-----+----+--------+------+
  | Field                       | Type               | Null| Key| Default| Extra|
  +-----------------------------+--------------------+-----+----+--------+------+
  | SPACE                       | int(11) unsigned   | NO  |    |        |      |
  | NAME                        | varchar(655)       | YES |    |        |      |
  | ENCRYPTION_SCHEME           | int(11) unsigned   | NO  |    |        |      |
  | KEYSERVER_REQUESTS          | int(11) unsigned   | NO  |    |        |      |
  | MIN_KEY_VERSION             | int(11) unsigned   | NO  |    |        |      |
  | CURRENT_KEY_VERSION         | int(11) unsigned   | NO  |    |        |      |
  | KEY_ROTATION_PAGE_NUMBER    | bigint(21) unsigned| YES |    |        |      |
  | KEY_ROTATION_MAX_PAGE_NUMBER| bigint(21) unsigned| YES |    |        |      |
  | CURRENT_KEY_ID              | int(11) unsigned   | NO  |    |        |      |
  | ROTATING_OR_FLUSHING        | int(1) unsigned    | NO  |    |        |      |
  +-----------------------------+--------------------+-----+----+--------+------+

To identify encryption-enabled schemas, query the
INFORMATION_SCHEMA.SCHEMATA table:

..  code-block:: MySQL

    mysql> SELECT SCHEMA_NAME, DEFAULT_ENCRYPTION FROM
    INFORMATION_SCHEMA.SCHEMATA WHERE DEFAULT_ENCRYPTION='YES';

    +------------------------------+---------------------------------+
    | SCHEMA_NAME                  | DEFAULT_ENCRYPTION              |
    +------------------------------+---------------------------------+
    | samples                      | YES                             |
    +------------------------------+---------------------------------+

.. note::

    The ``SHOW CREATE SCHEMA`` statement returns the ``DEFAULT ENCRYPTION``
    clause.

To verify if the binary log encryption option is enabled, run the following
statement:

.. code-block:: MySQL

    mysql>SHOW BINARY LOGS;

    +-------------------+----------------+---------------+
    | Log_name          | File_size      | Encrypted     |
    +-------------------+----------------+---------------+
    | binlog.00011      | 72367          | No            |
    | binlog:00012      | 71503          | No            |
    | binlog:00013      | 73762          | Yes           |
    +-------------------+----------------+---------------+

To allow for master Key rotation, you can encrypt an already encrypted InnoDB
system tablespace with a new master key by running the following ``ALTER
INSTANCE`` statement:

.. code-block:: guess

   mysql> ALTER INSTANCE ROTATE INNODB MASTER KEY;
