.. _encrypting_single_table

================================================================================
Encrypting a Single Table
================================================================================


Percona Server supports the ability to encrypt a single table in the InnoDB storage engine. The tablespace keys comes directly from the keyring. This configuration does not require the Master Key. In this configuration, you decide the table to be encrypted with from the keyring.

You encrypt a specific table using the `encryption='KEYRING' command. An example of the option follows:

.. code-block:: MySQL

    $ CREATE TABLE t1 (a varchar(255)) encryption='KEYRING';

A key_ID is associated with the table. The keyring value is from `innodb_default_ENCRYPTION_KEY_ID=0`, which is from the session scope.

You can also assign an encryption key ID when you create or alter a table.

.. code-block:: MySQL

    $ CREATE TABLE t1(a varchar(255)) encryption='KEYRING' ENCRYPTION_KEY_ID=X;

    $ ALTER TABLE t1 ENCRYPTION_KEY_ID=Y;

The options create a `percona_innodb-Y:('N')` value. You can also rotate the keys, if needed.
