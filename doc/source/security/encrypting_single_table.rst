.. _encrypting_single_table

================================================================================
Encrypting a Single Table
================================================================================

.. rubric:: Encrypting a Single Table

Percona Server supports the ability to encrypt a single table in the InnoDB storage engine. The tablespace keys comes directly from the keyring. This configuration does not require the Master Key. In this configuration, you decide the table to be encrypted with from the keyring.

For this configuration, you can encrypt a table using the `encryption='KEYRING' command. An example of the option follows:

.. .. code-block:: MySQL

$ CREATE TABLE t1 (a varchar(255)) encryption='KEYRING';

A key_ID is associated with the table. The keyring vaule is from `innodb_default_ENCRYPTION_KEY_ID=0`, which is a value from session scope.

You can also assign an encryption key ID when you create or alter a table.

.. .. code-block:: MySQL

$ CREATE TABLE t1(a varchar(255)) encryption='KEYRING' ENCRYPTION_KEY_ID=X;

$ ALTER TABLE t1 ENCRYPTION_KEY_ID=Y;

These options create a `percona_innodb-Y:<version>` value. You can rotate the keys, if needed.


The keyring management is enabled for each tablespace separately when you set
the encryption in the ``ENCRYPTION`` clause, to `KEYRING` in the supported SQL
statement:

- CREATE TABLE .. ENCRYPTION='KEYRING`
- ALTER TABLE ... ENCRYPTION='KEYRING'
- CREATE TABLESPACE tablespace_name … ENCRYPTION=’KEYRING’

.. note::

   Running ``ALTER TABLE .. ENCRYPTION=’Y’`` on the tablespace created with
   ``ENCRYPTION=’KEYRING’`` converts the table back to the existing MySQL
   scheme.
