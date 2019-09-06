.. encrypting-tablespaces:

======================================================
Encrypting Tablespaces
======================================================

.. _innodb_general_tablespace_encryption:

Setting the General Tablespace Encryption Default
================================================================================


A general tablespace can be either encrypted, all the tables are encrypted, or not encrypted. You cannot encrypted only some of the tables in a general tablespace.

The general tablespaces use the :variable: ``default_table_encryption`` variable to configure the encryption settings. If the ``ENCRYPTION`` clause is not specified in the CREATE TABLE statement, the statement applies the variable setting. 

This feature extends the  `CREATE TABLESPACE <https://dev.mysql.com/doc/refman/8.0/en/create-tablespace.html>`_ statement to accept the ``ENCRYPTION='Y/N'`` option.

.. note::

   Prior to |Percona Server| 8.0.13, the ``ENCRYPTION`` option was specific to
   the ``CREATE TABLE`` or ``SHOW CREATE TABLE`` statement.  In |Percona Server|
   8.0.13, this option becomes a tablespace attribute and is not allowed with
   the ``CREATE TABLE`` or ``SHOW CREATE TABLE`` statement except for
   file-per-table tablespaces.

   .. variable:: default_table_encryption

       :cli: ``default-table-encryption``
       :dyn: Yes
       :scope: Session
       :vartype: Text
       :default: OFF

Defines the default encryption setting for general tablespaces. The variable allows you to create or alter tables without specifying the ENCRYPTION clause.

.. seealso::

    MySQL Documentation: default_table_encryption
    https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html


Usage
================================================================================

General tablespace encryption is enabled by the following syntax extension:

.. code-block:: mysql

   mysql> CREATE TABLESPACE tablespace_name ... ENCRYPTION='Y'
An attempt to create or to move tables, including partitioned ones, to a general
tablespace with an incompatible encryption setting are diagnosed and and the process is aborted.

If you must move tables between encrypted and unencrypted tablespaces,
create another table with the same structure in another tablespace and run
``INSERT INTO SELECT`` from the table from your source table to the destination table.  This procedure will
give you an encrypted table or decrypted table with your desired content.

Example
================================================================================

To create an encrypted tablespace run: :mysql:`CREATE TABLESPACE foo ADD DATAFILE 'foo.ibd' ENCRYPTION='Y';`

To add an encrypted table to that table space run: :mysql:`CREATE TABLE t1 (a INT, b TEXT) TABLESPACE foo ENCRYPTION="Y";`

If the tablespace is encrypted, attempting to add an unencrypted table results in the following error:

.. code-block:: mysql

   mysql> CREATE TABLE t3 (a INT, b TEXT) TABLESPACE foo ENCRYPTION="N";
   ERROR 1478 (HY000): InnoDB: Tablespace `foo` can contain only an ENCRYPTED tables.

.. note::

   |Percona XtraBackup| version 8 supports the backup of encrypted general
   tablespaces. Any features which are not GA are not supported in version 8.

System variables
--------------------------------------------------------------------------------

.. variable:: innodb_sys_tablespace_encrypt

   :cli: ``--innodb-sys-tablespace-encrypt``
   :dyn: No
   :scope: Global
   :vartype: Boolean
   :default: ``OFF``

Enables the encryption of the InnoDB System tablespace. It is essential that the
server is started with the ``--bootstrap`` option.

.. seealso::

   |MySQL| Documentation: ``--bootstrap`` option
      https://dev.mysql.com/doc/refman/8.0/en/server-options.html#option_mysqld_bootstrap
