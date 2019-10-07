.. _innodb_encryption:

========================================================
InnoDB Encryption
========================================================

|Percona Server| provides tools to protect data with tablespace encryption. These tools are a part of the data-at-rest encryption feature.

InnoDB System Tablespace Encryption
================================================================================

:Availabiliity: This feature is **Experimental** quality

The InnoDB system tablespace is encrypted with the master key encryption. If the variable :variable:`innodb_sys_tablespace_encrypt` is set to ON and the
server is started with the ``--bootstrap`` option, you may create an encrypted table as follows:

.. code-block:: guess

   mysql> CREATE TABLE ... TABLESPACE=innodb_system ENCRYPTION='Y'

.. note::

   Any tables in the System tablespace before this command is issued cannot be encrypted.

After a system tablespace is encrypted, you cannot convert the tablespace to unencrypted and an unencrypted system tablespace cannot be converted to encrypted. A new instance should be created and the user tables are transferred to the instance.

.. rubric:: Rotating the Master Key

To allow for Master Key rotation, you can encrypt an already encrypted InnoDB system tablespace
with a new master key by running the following ``ALTER INSTANCE`` statement:

.. code-block:: guess

   mysql> ALTER INSTANCE ROTATE INNODB MASTER KEY


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


.. _innodb_general_tablespace_encryption:

InnoDB General Tablespace Encryption
================================================================================

A general tablespace can be either encrypted, all the tables are encrypted, or not encrypted.
You cannot encrypted only some of the tables in a general tablespace.

This feature extends the  `CREATE TABLESPACE <https://dev.mysql.com/doc/refman/8.0/en/create-tablespace.html>`_
statement to accept the ``ENCRYPTION='Y/N'`` option.

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

Verifying the Encryption Setting
================================================================================

If a general tablespace includes tables, you cna check the table info to verify the tablespace setting.

If a general tablespace does not include tables, to verify the the encryption setting, you can check the ``flag`` field in the ``INFORMATION_SCHEMA.INNODB_TABLESPACES``. This field has bit
number 13 set if tablespace is encrypted. You can ckeck the setting with the
``flag & 8192`` expression in the following way:

.. code-block:: mysql

  SELECT space, name, flag, (flag & 8192) != 0 AS encrypted FROM INFORMATION_SCHEMA.INNODB_TABLESPACES WHERE name in ('foo', 'test/t2', 'bar', 'noencrypt');

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

System Variables
----------------

.. variable:: innodb_encrypt_tables

  :cli: ``--innodb-encrypt-tables``
  :removed: version 8.0.16-7
  :dyn: Yes
  :scope: Global
  :vartype: Text
  :default: ``OFF``

The variable is considered **deprecated** and removed in version 8.0.16-7.

.. seealso::

   |MariaDB| Documentation: ``innodb_encrypt_tables`` Option
      https://mariadb.com/kb/en/library/xtradbinnodb-server-system-variables/#innodb_encrypt_tables

This variable is implemented in |Percona Server| version 8.0.16-7.

.. variable:: default_table_encryption

    :cli: default-table-encryption
    :implmemented: version 8.0.16-7
    :dyn: Yes
    :scope: Global
    :vartype: Boolean
    :default: OFF

The  variable describes the default encryption setting for general tablespaces. If the ``ENCRYPTION`` option is not explicitly stated, the ``CREATE TABLE`` statement uses the `default_table_encryption` setting.

The ``default_table_encryption`` settings are as follows:

.. tabularcolumns:: |p{5cm}|p{5cm}|

.. list-table::
    :header-rows: 1

    * - Option
      - Description
    * - ON
      - Tables are created encrypted. Setting ``ENCRYPTION=NO`` clause in the ``CREATE TABLE`` or ``ALTER TABLE`` statement creates an encrypted table.
    * - OFF
      - Tables are created without encryption. Setting ``ENCRYPTION=YES`` clause in the ``CREATE TABLE`` or ``ALTER TABLE`` statement creates an encrypted table.
    * - FORCE
      - Tables are created encrypted with the master key. Setting ``ENCRYPTION=NO`` to ``CREATE TABLE`` or ``ALTER TABLE`` generates an error and the table is not created or altered.
    * - KEYRING_ON
      - This value is **Experimental** quality. Tables are created encrypted with the keyring as the default encryption. You must specify a numeric key identifer and use a specific ``percona-innodb-`` key from the keyring instead of the default key.
    * - FORCE_KEYRING
      - This value is **Experimental** quality. Tables are created and keyring encryption is enforced.
    * - ONLINE_TO_KEYRING
      - This value is **Experimental** quality. Tables created or altered without the ``ENCRYPTION=NO`` clause are encrypted with the latest version of the default encryption key. If you alter a table is already encrypted with the master key, the table is recreated encrypted with the latest version of the default encryption key.
    * - ONLINE_TO_KEYRING_FORCE
      - This value is **Experimental** quality. It only possible to apply the keyring encryption when creating or altering tables.

.. note::

    The ``ALTER TABLE`` statement changes the current encryption mode only if you use the ``ENCRYPTION`` clause.

An example of ``KEYRING`` value is the following:

.. code-block:: mysql

    mysql>CREATE TABLE ... ENCRYPTION='KEYRING' ENCRYPTION_KEY_ID=NEW_ID

In the example, the ``NEW_ID`` is an unsigned 32-bit integer and refers to the numerical part of the ``percona_innodb-`` key. When you assign a numerial identifier in the ``ENCRYPTION_KEY_ID`` clause, the server uses the latest version of the corresponding key. If you assigned the ``ENCRYPTION_KEY_ID=2``, the "2" refers to the latest version of the ``percona_innodb-2`` key from the keyring.

If the requested ``percona-innodb-`` does not exist in the keyring, |Percona Server| creates the key with version 1. If a ``percona-innodb-`` key cannot be created with the requested ID, the ``CREATE TABLE`` statement fails.

.. seealso::

    MySQL Documentation: ``default_table_encryption``
    https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_default_table_encryption

.. variable:: table_encryption_privilege_check

  :cli: table-encryption-privilege-check
  :implemented: version 8.0.16-7
  :dyn: Yes
  :scope: Global
  :vartype: Boolean
  :default: OFF

The variable is used when creating or altering a general tablespace or table with an encryption setting different than the :variable:`default_table_encryption`. The default value is `OFF`.

.. seealso::

  MySQL Documentation: ``table_encryption_privilege_check``
  https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html

.. variable:: innodb_encryption_threads

   :cli: ``--innodb-encryption-threads``
   :dyn: Yes
   :scope: Global
   :vartype: Numeric
   :default: 0

This variable works in combination with the :variable:`default_table_encryption`
variable set to ``ONLINE_TO_KEYRING``. This variable configures the number of
threads for background encryption. For the online encryption to work, this
variable must contain a value greater than **zero**.

.. variable:: innodb_online_encryption_rotate_key_age

   :cli: ``--innodb-online-encryption-rotate-key-age``
   :dyn: Yes
   :scope: Global
   :vartype: Numeric
   :default: 1

By using this variable, you can re-encrypt the table encrypted using
KEYRING. The value of this variable determines how frequently the encrypted
tables should be encrypted again. If it is set to **1**, the encrypted table is
re-encrypted on each key rotation. If it is set to **2**, the table is encrypted
on every other key rotation.

.. variable:: innodb_encrypt_online_alter_logs

   :cli: ``--innodb-encrypt-online-alter-logs``
   :dyn: Yes
   :scope: Global
   :vartype: Boolean
   :default: OFF

This variable simultaneously turns on the encryption of files used by InnoDB for
full text search using parallel sorting, building indexes using merge sort, and
online DDL logs created by InnoDB for online DDL. Encryption is available for file merges used in queries and backend processes.

Undo Tablespace Encryption
==============================================================================

Implemented in :rn:`8.0.16-7`, the undo tablespace data encryption is available as an option. The undo data encryption must be enabled; the feature is disabled by default. When the undo log data is written to disk, the data is encrypted using the tablespace encryption key. The undo log data is decrypted when read.



.. seealso::

   |MySQL| Documentation
      https://dev.mysql.com/doc/refman/8.0/en/innodb-tablespace-encryption.html#innodb-tablespace-encryption-undo-log

Redo Log Encryption
==============================================================================

Implemented in :rn:`8.0.16-7`, the supported values for :variable:`innodb_redo_log_encrypt` are the following:

  * ON
  * OFF
  * master_key
  * keyring_key

.. note::

  The keyring_key is **Experimental** for :rn:`8.0.16-7`.

After starting the server, an attempt to encrypt the redo log fails in the following conditions:

  * Server started with no keyring specified
  * Server started with a keyring, but a different redo log encryption method is specified

Temporary File Encryption
================================================================================

:Availability: This feature is of **Experimental** quality.

The encryption of temporary files is triggered by the :variable:`encrypt-tmp-files` option.

The `default_table_encryption` setting determines if a temporary table is encrypted. If the `innodb_temp_tablespace_encrypt`=OFF and the `default_table_encryption`=ON the temporary tables are encrypted. For the Innodb user-created temporary tables created in a temporary tablespace file use the `innodb_temp_tablespace_encrypt` variable.

.. variable:: innodb_temp_tablespace_encrypt

  :cli: ``--innodb-temp-tablespace-encrypt``
  :dyn: Yes
  :scope: Global
  :vartype: Boolean
  :default: ``OFF``

When this option is set to ``ON``, the server encrypts the global temporary tablespace (:file:`ibtmp*` files) and the session temporary tablespaces (:file:`#innodb_temp/temp_*.ibt` files). This option does not enforce the encryption of temporary tables which are currently open, and it does not rebuild the system temporary tablespace to encrypt data which are already written.

The ``ENCRYPTION`` option is not allowed in the ``CREATE TEMPORARY TABLE`` statement. The ``TABLESPACE`` option cannot be set to `innodb_temporary`. The global temporary tablespace datafile ``ibtmp1`` holds temporary table undo logs while intrinsic temporary tables and user temporary tables go to the encrypted session temporary tablespace.

Since the global temporary tablespaces are created fresh at each server startup, it will not contain unencrypted data if this option is specified as a server argument.

Setting :variable:`innodb_temp_tablespace_encrypt` to ``OFF`` with :variable:`default_table_encryption` set to ``OFF`` at runtime makes the server create new temporary tablespaces unencrypted. Existing encrypted user temporary and intrinsic temporary tables remain in encrypted session. Temporary tablespaces are only destroyed when the session is disconnected.

When :variable:`innodb_temp_tablespace_encrypt` is ``OFF`` while :variable:`default_table_encryption` is ``ON`` at startup, the temporary tablespace datafile ``ibtmp1``, which only contains undo logs, is not encrypted. However, user-created and intrinsic temporary tables go to the encrypted session temporary tablespace.

Setting the encryption to ``ON`` for the system tablespace generates an encryption key and encrypts the system temporary tablespace pages. Resetting the encryption to ``OFF``, all subsequent pages are written to the tablespace without encryption. The generated keys are not erased, to allow any encrypted tables to be decrypted.

This feature is considered **Experimental** quality.

.. important::

To use this option, a keyring plugin must be loaded, otherwise the server produces an error message and refuses to create new temporary tables.

.. seealso::

  |MySQL| Documentation
  https://dev.mysql.com/doc/refman/8.0/en/create-temporary-table.html

Temporary files are currently used in |Percona Server| for the following purposes:

  * filesort (for example, ``SELECT`` statements with ``SQL_BIG_RESULT`` hints),
  * binary log transactional caches,
  * Group Replication caches.

For each temporary file, an encryption key is generated locally, only kept in memory for the lifetime of the temporary file, and discarded afterwards.

System Variables
----------------

.. variable:: encrypt-tmp-files

    :cli: ``--encrypt-tmp-files``
    :dyn: No
    :scope: Global
    :vartype: Boolean
    :default: ``OFF``

The option turns on encryption of temporary files created by |Percona Server|.

.. rubric:: Doublewrite Buffers

The two types of doublewrite buffers used in |Percona Server| are encrypted differently.

When the InnoDB system tablespace is encrypted, the ``doublewrite buffer`` pages
are encrypted as well. The key which was used to encrypt the InnoDB system
tablespace is also used to encrypt the doublewrite buffer.

|Percona Server| encrypts the ``parallel doublewrite buffer`` with the respective
tablespace keys. Only encrypted tablespace pages are written as encrypted in the
parallel doublewrite buffer. Unencrypted tablespace pages will be written as
unencrypted.

.. important::

   A server instance bootstrapped with the encrypted InnoDB system tablespace
   cannot be downgraded. It is not possible to parse encrypted InnoDB system
   tablespace pages in a version of |Percona Server| lower than the version
   where the InnoDB system tablespace has been encrypted.

.. variable:: innodb_parallel_dblwr_encrypt

   :cli: ``--innodb-parallel-dblwr-encrypt``
   :dyn: Yes
   :scope: Global
   :vartype: Boolean
   :default: ``OFF``

Enables the encryption of the parallel doublewrite buffer. For encryption, uses
the key of the tablespace where the parallel doublewrite buffer is used.
