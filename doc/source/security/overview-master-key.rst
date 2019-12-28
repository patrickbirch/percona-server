.. _overview-master-key:

==============================================================================
Master Key Encryption Overview
==============================================================================

Master key encryption, which is symmetric encryption, uses a single key to
encrypt and decrypt. The advantage of symmetric encryption is the key manages many other keys with little overhead and is fast. The security of
symmetric encryption is the security and integrity of the keys. All keys
require protection throughout the lifetime of the key. A key replaces another
key in almost all operations.

The Master key is the root of the encryption hierarchy and is used to encrypt
multiple tablespace keys. Tablespaces are encrypted by tablespace keys.  The
Master key remains in the keyring. Each tablespace keys is located in each tablespace header. An InnoDB tablespace file
is comprised of multiple logical and physical pages. Page 0 is the tablespace
header page and keeps the metadata for the tablespace. The encryption
information is stored on page 0, and the tablespace key is
encrypted.

To enable Master key encryption for tablespaces and schemas, the MySQL keyring plugin stores the InnoDB master key. The Master key is used for encryption tablespaces and schemas, redo logs, and undo logs, along with the
tablespaces.

The InnoDB tablespace encryption has the following components:

    * The database instance has a master key for tablespaces and a master key
      for binary log encryption.

    * Each tablespace has a tablespace key. The key is used to encrypt the
      Tablespace data pages. Encrypted tablespace keys are written on
      tablespace header. In the master key implementation, the tablespace key
      cannot be changed unless you rebuild the table.

Two separate keys allow the master key to be rotated in a minimal operation.
When the master key is rotated, each tablespace key is decrypted and
re-encrypted with the new master key. Only the first page of every tablespace
(.ibd) file is read and written during the key rotation.


 Schema and General Tablespace Encryption
 ----------------------------------------

 rubric:: System Variables

.. variable:: default_table_encryption

    :cli: ``default-table-encryption``
    :dyn: Yes
    :scope: Session
    :vartype: Text
    :default: OFF
    :available values: OFF, ON, KEYRING_ON,
    ONLINE_TO_KEYRING, ONLINE_FROM_KEYRING_TO_UNENCRYPTED

Defines the default encryption setting for schemas and general tablespaces. The
variable allows you to create or alter schemas or tablespaces without defining
the ENCRYPTION clause. The default encryption setting applies only to schemas
and general tablespaces and cannot be applied to the MySQL system
tablespace.

This variable was implemented in |Percona Server| 8.0.16-7. If you are using an
earlier version of Percona Server, you must explicitly use the ``ENCRYPTION``
clause.

.. list-table::

    :widths: 15 30
    :header-rows: 1

    * - Value
      - Description
    * - OFF
      - By default, new tablespaces and schemas are not encrypted. To create
        encrypted tables add ``ENCRYPTION="Y"`` to ``CREATE TABLE`` or ``ALTER
        TABLE``.
    * - ON
      - New tablespaces and schemas are encrypted. To create unencrypted
        tablespaces and schemas
        add ``ENCRYPTION="N"`` to ``CREATE TABLE`` or ``ALTER TABLE``.
    * - KEYRING_ON
      - :Availablilty: This value is **Experimental** quality.

        New tables are created with the keyring as the default encryption. You
        may specify a numeric key identifier and use a specific
        `percona-innodb-` key from the keyring instead of the default key:

        .. code-block:: MySQL

            mysql> CREATE TABLE ... ENCRYPTION=`KEYRING`
            ENCRYPTION_KEY=ID=NEW_ID

        `NEW_ID` is an unsigned 32-bit integer that refers to the numerical
         part of the`percona-innodb-` key. When you assign a numerical
         identifier in the `ENCRYPTION_KEY_ID` clause, the server uses the
         latest version of the corresponding key. For example,
         `ENCRYPTION_KEY_ID=2` refers to the latest version of the
         `percona_innodb-2` key from the keyring.
    * - ONLINE_TO_KEYRING
      - :Availability: This value is **Experimental** quality.

        New tablespaces and schemas are created with ``ENCRYPTION="KEYRING"``
    * - ONLINE_FROM_KEYRING_TO_UNENCRYPTED
      - :Availability: This value is **Experimental** quality.

        A tablespace or schema are created with an implicit
        ``ENCRYPTION='N'`` assigned.

In versions before |Percona Server| 8.0.16-7, the
:variable:`innodb_encrypt_tables` is used. The variable is considered **deprecated** and was removed in version 8.0.16-7.

.. variable:: innodb_encrypt_tables

    :cli: ``--innodb-encrypt-tables``
    :removed: version 8.0.16-7
    :dyn: Yes
    :scope: Global
    :vartype: Text
    :default: ``OFF``

The default setting is "OFF".

The :variable:`table_encryption_privilege_check` variable enforces encryption
defaults. This variable was added in |Percona Server| 8.0.16-7.

.. variable:: table_encryption_privilege_check

    :cli:``--table-encryption-privilege-check``
    :dyn: Yes
    :scope: Global
    :vartype: Boolean
    :default: ``OFF``

This variable controls the encryption defaults. When the variable is ``ON``, the
following conditions trigger a warning:

    * Creating or altering a schema or general tablespace with an encryption
      setting that is different than the ``default_table_encryption``
    * Creating or altering a table with an encryption setting different than
      the default schema encryption.

When `table_encryption_priviliege_check` is ``ON``, the ``TABLE_ENCRYPTION_ADMIN
<https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_table-encryption-admin>`_
is required to override the default encryption settings.

.. note::

    The ``TABLE_ENCRYPTION_ADMIN`` privilege does not permit creating or
    altering a table with a different encryption setting than the general
    tablespace.

If you have not enabled the ``default_table_encryption``, you can define a
schema or general tablespace with the ``ENCRYPTION`` clause.

.. note::

    Prior to |Percona Server| 8.0.13, the ``ENCRYPTION`` clause was specific to
    the ``CREATE TABLE`` or ``SHOW CREATE TABLE`` statement.

    As of |Percona Server| 8.0.13, ``ENCRYPTION`` is a tablespace attribute and
    not allowed with ``CREATE TABLE`` or ``SHOW CREATE TABLE`` statements with
    the exception of file-per-table tablespaces.

An attempt to create an unencrypted table in an encrypted general tablespace
generates the following error:

.. code-block::

    mysql> CREATE TABLE t3 (a INT, b TEXT) TABLESPACE sample ENCRYPTION='N';

    ERROR 1478 (HY0000): InnoDB: Tablespace 'sample' can contain only ENCRYPTED
    tables.

An attempt to move a table, including a partitioned table, to a general
tablespace with an incompatible encryption setting is diagnosed and the process
is aborted.

If you must move a table between tablespaces with different encryption
settings, ceate a table with the same structure in the target tablespace and run
``INSERT INTO SELECT`` from the source table to the target table.

System Tablespace Encryption
-----------------------------

As of |Percona Server| 8.0.16-7, system tablespace encryption is supported.

.. rubric:: Limitations

    You cannot convert an encrypted system tablespace to an unencrypted
    tablespace or an unencrypted system tablespace to encrypted. If a conversion is needed, you must create a new instance with the system
    tablespace in the desired state and then transfer the user tables to that
    instance.

    A server instance initialized with the encrypted InnoDB system tablespace
    cannot be downgraded. It is not possible to parse encrypted InnoDB system
    tablespace pages in a version of |Percona Server| lower than the version
    where the InnoDB system tablespace has been encrypted.

    .. variable: innodb_sys_tablespace_encrypt

       :cli: ``--innodb-sys-tablespace-encrypt``
       :dyn: No
       :scope: Global
       :vartype: Boolean
       :default: ``OFF``

The variable enables the encryption of the InnoDB system tablespace.

Redo Log Encryption
--------------------

The Redo log can be encrypted with the :variable:`innodb_redo_log_encrypt`
variable. The Redo log uses the tablespace encryption key.

.. variable:: innodb_redo_log_encrypt

    :cli:  ``--innodb-redo-log-encrypt``
    :dyn: Yes
    :scope: Global
    :vartype: Text
    :default: OFF

Determines the encryption for redo log data for encrypted. The encryption of
redo log data, by default, is 'OFF'.

As implemented in :rn:`8.0.16-7`, the optional values for
:variable:`innodb_redo_log_encrypt` are the following:

* ON

* OFF

* MASTER_KEY

* KEYRING_KEY

The keyring_key option is an **Experimental** value.

.. seealso::

   For more information on the keyring_key - :ref:`encrypting-threads`

.. note::

    For `innodb_redo_log_encrypt`, the "ON" value is an alias for
    ``MASTER_KEY`` value.

The redo log data is encrypted when it is written to disk and decrypted when the
data is read from disk. Any redo log data in memory is unencrypted.

When `innodb_redo_log_encrypt` is enabled, any existing redo log pages stay
unencrypted, and new pages are encrypted.

If the redo log encryption is enabled, you must load the appropriate keyring
plugin and encryption key to perform a normal restart.

When `innodb_redo_log_encrypt` is
disabled, any existing pages remain encrypted, and new pages are not encrypted.

An attempt to encrypt the redo log fails if one of the following conditions is
true:

    * Server started with no keyring specified

    * A different redo log encryption method is defined then what was previously
    used on the same server.

Undo Log Encryption
--------------------

Undo log data is encrypted using the
:variable:`innodb_undo_log_encrypt` option. You can edit this variable
in the configuration file, as a startup parameter, or during runtime as a global
variable.

.. variable:: innodb_undo_log_encrypt

    :cli: ``--innodb_undo-log_encrypt``
    :dyn: Yes
    :scope: Global
    :vartype: Boolean
    :default: OFF

Defines if an undo log data is encrypted. The undo log data encryption is disabled by default.

Undo log data is encrypted when the data is read to disk. The data is decrypted
when the data is read from disk. When the undo log data is in memory, the data
is unencrypted.

The undo log data is encrypted and decrypted with the tablespace encryption key,
which is stored in the undo log file header.

.. note::

    If you disable encryption, any encrypted undo data remains encrypted. To
    remove this data, truncate the undo tablespace.

Binlog Encryption
------------------

Enable the ``binlog_encryption`` option to encrypt new binary log files and
relay
log files on disk. Only the data is encrypted.

.. variable:: binlog_encryption

    :cli: ``--binlog-encryption``
    :dyn: Yes
    :scope: Global
    :vartype: Boolean
    :default: ``OFF``

Enables encryption for binary log files and relay log files. The default value
is ``OFF``.

Replication master and slaves can use separate keyring storages and are able to
use different keyring plugins. The relay logs on a slave server can be encrypted even if the
slave server does not have a binary log.

Use the ``--read-from-remote-server`` option to read encrypted binlog files in
``mysqlbinlog``. You cannot use ``mysqlbinlog`` to read an encrypted file
directly.

.. note::

    The `--read-from-remote-server`  option only applies to the binary logs.
    Encrypted relay logs can not be dumped or decrypted with this option.

Attempting a  binary log encryption without the keyring generates a MySQL error.

The Binary log encryption uses two tiers:

    * File password

    * Binary log encryption key

The file password encrypts the content of a single binary file or relay log
file. The binary log encryption key is used to encrypt the file password and is
stored in the keyring.

To enable binlog encryption, set the :variable:`binlog_encryption` option to
``ON``. A keyring plugin must be
installed and configured.

If you enable encryption while the server is running, a new binary log
encryption key is generated, unless the encryption had been previously enabled
and then disabled on the server, in that case the binary log encryption key that
was in use is re-used. Binary log files and relay log files are rotated
immediately and any
new binary log files and relay log files are encrypted. Any existing binary log
files and relay log files remain not encrypted.

If you disable encryption, the binary log files and relay log files are rotated
immediately and all subsequent log files are not encrypted. The server is able
to read the encrypted files which remain.

The ``BINLOG_ENCRYPTION_ADMIN`` privilege is required to enable or disable
encryption while the server is running.

Binlog Encryption: Upgrading from |Percona Server| 8.0.15-5 to any Higher
Version
---------------------------------------------------------------------------------------

Starting from release :rn:`8.0.15-5`, |Percona Server| uses the upstream
implementation of binary log encryption. The variable `encrypt-binlog` is
removed and the related command line option `--encrypt-binlog` is not
supported. It is important to remove the `encrypt-binlog` variable from your
configuration file before you attempt to upgrade either from another release
in the |Percona Server| |version| series or from |Percona Server| 5.7.
Otherwise, a server boot error will be generated reporting an unknown
variable. The implemented binary log encryption is compatible with the older
format. The encrypted binary log used in a previous version of MySQL 8.0
series or Percona Server for MySQL series is supported.

.. variable:: encrypt_binlog

      :version-info:  removed in :rn:`8.0.15-5`
      :cli: ``--encrypt-binlog``
      :dyn: No
      :scope: Global
      :vartype: Boolean
      :default: ``OFF``

The variable turns on binary log and relay log encryption.

.. seealso::

    |MySQL| Documentation:
    `Encrypting Binary Log Files and Relay Log Files <https://dev.mysql.com/doc/refman/8.0/en/replication-binlog-encryption.html>`__

Master Key Rotation
--------------------

Rotate the master key on a schedule or if you
suspect the key is compromised. The master key rotation operation changes the
master
key, and each tablespace key is re-encrypted and updated in the tablespace
headers. The operation does not affect tablespace data. The rotation operation
must complete before starting any tablespace encryption operation.

.. note::

    The rotation re-encrypts each tablespace key, but the key is not
    changed. To change a tablespace key, you should disable and then
    re-enable encryption.

To rotate the master key, you must have the ``ENCRYPTION_KEY_ADMIN`` or
``SUPER`` privilege.

If the master key rotation operation is interrupted, the operation is rolled
forward when the server restarts. InnoDB reads the encryption data from the
tablespace header, and if the prior master key has encrypted specific tablespace
keys, InnoDB retrieves the prior master key from the keyring to decrypt the
tablespace key. InnoDB then re-encrypts the tablespace key with the new master
key.

Verifying Encryption
---------------------

If a general tablespace or schema contains tables, check the table information
to see if the table is encrypted. If the general tablespace or schema does not
contain tables, you must verify the tablespace or schema.

