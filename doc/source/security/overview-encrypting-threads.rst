.. _overview_encrypting-threads:

===============================================================================
Background Encryption Threads Overview
===============================================================================

:Availability: This feature is **Experimental** quality.

|InnoDB| uses background encryption threads to perform encryption and
decryption operations.

System Variable
---------------------

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

.. note::

    You can only apply the keyring encryption when creating or alterin tables.


When the :variable:`default_table_encryption` system
variable is set to ``ONLINE_TO_KEYRING``

.. variable:: innodb_encryption_threads

    :cli: ``--innodb-encryption-threads``
    :dyn: Yes
    :scope: Global
    :vartype: Numeric
    :default: 0

This variable works in combination with the
:variable:`default_table_encryption` variable set to ``ONLINE_TO_KEYRING``. This variable
configures the number of threads for background encryption. For the online
encryption, the value must be greater than **zero**.

.. variable:: innodb_online_encryption_rotate_key_age

    :cli: ``--innodb-online-encryption-rotate-key-age``
    :dyn: Yes
    :scope: Global
    :vartype: Numeric
    :default: 1

Defines the rotation for the re-encryption of a table encrypted using KEYRING.
The value of this variable determines how frequently encrypted tables
are re-encrypted.

For example, the following values would trigger a re-encryption in the
following intervals:

*  The value is **1**, the table is re-encrypted on each key rotation.
*  The value is **2**, the table is re-encrypted on every other key rotation.
*  The value is **10**, the table is re-encrypted on every tenth key rotation.

You should select the value which best fits your operational requirements.

Using Keyring Encryption
-------------------------------------------

:Availability: This feature is **Experimental** quality.

Keyring management is enabled for each table, per file table, separately when
you set encryption in the ``ENCRYPTION`` clause to ``KEYRING`` in the supported
SQL statement.

* CREATE TABLE ... ENCRYPTION='KEYRING'
* ALTER TABLE ... ENCRYPTION='KEYRING'

.. note::

    Running an ``ALTER TABLE ... ENCRYPTION='N'`` on a table created with
    ``ENCRYPTION='KEYRING'`` converts the table to the existing MySQL schema,
    tablespace, or table encryption state.

.. seealso::

    :ref:`enabling_encryption_threads`

.. rubric:: Encrypting Temporary Files

:Availability: This feature is **Experimental** quality.

To encrypt InnoDB user-created temporary tables, created in a temporary
tablespace file, use the ``innodb_temp_tablespace_encrypt`` variable.

    .. variable:: innodb_temp_tablespace_encrypt

        :cli: ``--innodb-temp-tablespace-encrypt``
        :dyn: Yes
        :scope: Global
        :vartype: Boolean
        :default: ``OFF``

Encrypts the global temporary tablespace (`ibtmp*` files) and session temporary
tablesapces (`#innodb_temp` or `*.ibt`). The variable does not enforce
encryption of currently open temporary files and does not rebuild the system
temporary tablespace to encrypt data which has already been written.

The ``CREATE TEMPORARY TABLE`` does not support the ``ENCRYPTION`` clause. The
``TABLESPACE`` clause cannot be set to innodb_temporary.

The global temporary tablespace  datafile ``ibtmp1`` contains temporary table
undo logs while intrinsic temporary tables and user-created temporary tables are
located in the encrypted session temporary tablespace.


