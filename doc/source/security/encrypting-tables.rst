.. encrypting-tables:

=========================================================
Encrypting Tables
=========================================================

You can only encrypt individual InnoDB tables stored in ``innodb_file_per_table`` tablespaces. In this tablespace configuration, each table is stored in an .ibd file.

The architecture for data at rest encryption is two tier: master key and tablespace keys.

For encryption, edit the my.cnf file to activate the keyring.

.. code-block:: MySQL

  early-plugin-load=keyring_file.so
  keyring_file_data=/usr/local/mysql/data/keyring

Restart the server.

Create the encrypted table.

.. code-block:: mysql

   mysql> CREATE TABLE myexample (id INT, mytext varchar(255)) ENCRYPTION='Y';

If the table already exists, you can encrypt the table with an ``ALTER TABLE`` statement.

.. code-block:: MySQL

    mysql> ALTER TABLE myexample ENCRYPTION='Y';

If you do not add the ``ENCRYPTION`` option, the table is not encrypted when created or altered.

.. seealso::

  |MySQL| Documentation:
  -  `File-Per-Table Encryption <https://dev.mysql.com/doc/refman/8.0/en/innodb-tablespace-encryption.html#innodb-tablespace-encryption-enabling-disabling>`__
