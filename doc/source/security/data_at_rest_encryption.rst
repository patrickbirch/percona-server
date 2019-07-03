.. _data_at_rest_encryption:

================================================================================
Data at Rest Encryption
================================================================================

.. contents::
   :local:

Data at rest encryption is an important aspect of any regulatory compliance strategy. The data is maintained physically in any format and in persistent storage and data is encrypted at the database level. Data at rest encryption protects the data through the full data lifecycle. The encryption provides a high level of assurance.

The benefits of data encryption are the following:

* Protects the data from physical theft of the device
* Denies unauthorized access to the data
* Satisfies regulatory requirements and information security standards
* Ensures the integrity of the data

Data at rest encryption is a key-based encryption system. The administrator must set a master encryption key. A key or phrase allows users to access the data transparently.

Creating a tablespace with encryption enabled automatically encrypts the objects stored in the tablespace and uses the encryption algorithm specified at the tablespace is defined.



Checking
================================================================================

If there is a general tablespace which doesn't include tables yet, sometimes
user needs to find out whether it is encrypted or not (this task is easier for
single tablespaces since you can check table info).

A ``flag`` field in the ``INFORMATION_SCHEMA.INNODB_TABLESPACES`` has bit
number 13 set if tablespace is encrypted. This bit can be ckecked with
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

.. variable:: innodb_temp_tablespace_encrypt

  :cli: ``--innodb-temp-tablespace-encrypt``
  :dyn: Yes
  :scope: Global
  :vartype: Boolean
  :default: ``Off``

When this option is set to ``ON``, the server encrypts the global temporary
tablespace (:file:`ibtmp*` files) and the session temporary tablespaces
(:file:`#innodb_temp/temp_*.ibt` files). This option does not enforce the
encryption of temporary tables which are currently open, and it does not rebuild
the system temporary tablespace to encrypt data which are already written.

The ``ENCRYPTION`` option is not allowed in the ``CREATE TEMPORARY TABLE``
statement. The ``TABLESPACE`` option cannot be set to `innodb_temporary`. The
global temporary tablespace datafile ``ibtmp1`` holds temporary table undo logs
while intrinsic temporary tables and user temporary tables go to the encrypted
session temporary tablespace.

Since the global temporary tablespaces are created fresh at each server startup,
it will not contain unencrypted data if this option is specified as a server
argument.

Setting :variable:`innodb_temp_tablespace_encrypt` to ``OFF`` with
:variable:`innodb_encrypt_tables` set to ``OFF`` at runtime makes the server
create new temporary tablespaces unencrypted. Intrinsic tables to go unencrypted
session temporary tablespaces. Existing encrypted user temporary and intrinsic
temporary tables remain in encrypted session temporary tablespaces and are only
destroyed when the session is disconnected.

When :variable:`innodb_temp_tablespace_encrypt` is ``OFF`` while
:variable:`innodb_encrypt_tables` is ``ON`` at startup, the temporary tablespace
datafile ``ibtmp1``, which only contains undo logs, is not encrypted. However,
user-created and intrinsic temporary tables go to the encrypted session
temporary tablespace.

This feature is considered **BETA** quality.

.. important::

   To use this option, a keyring plugin must be loaded, otherwise the server
   produces an error message and refuses to create new temporary tables.

.. seealso::

   |MySQL| Documentation
      https://dev.mysql.com/doc/refman/8.0/en/create-temporary-table.html

.. variable:: innodb_encrypt_tables

  :cli: ``--innodb-encrypt-tables``
  :dyn: Yes
  :scope: Global
  :vartype: Text
  :default: ``OFF``

The implementation of the behavior controlled by this variable is considered
**BETA** quality.

This variable was ported from MariaDB and then extended to support key rotation. This
variable has the following possible values:

.. rubric:: ON

New tables are created encrypted. You can create an unencrypted table by using
the ``ENCRYPTION=NO`` clause to the ``CREATE TABLE`` or ``ALTER TABLE``
statement.

.. rubric:: OFF

By default, newly created tables are not encrypted. Add the ``ENCRYPTION=NO``
clause in the ``CREATE TABLE`` or ``ALTER TABLE`` statement to create an
encrypted table.

.. rubric:: FORCE

New tables are created encrypted with the master key. Passing ``ENCRYPTION=NO``
to ``CREATE TABLE`` or ``ALTER TABLE`` will result in an error and the table
will not be created or altered.

If you alter a table which was created without encryption, note that it will not
be encrypted unless you use the ``ENCRYPTION`` clause explicitly.

.. rubric:: KEYRING_ON

:Availability: This value is **Experimental** quality

New tables are created encrypted with the keyring as the default encryption. You
may specify a numeric key identifier and use a specific ``percona-innodb-`` key
from the keyring instead of the default key:

.. code-block:: guess

   mysql> CREATE TABLE ... ENCRYPTION=’KEYRING’ ENCRYPTION_KEY_ID=NEW_ID

**NEW_ID** is an unsigned 32-bit integer that refers to the numerical part of
the ``percona_innodb-`` key.  When you assign a numerical identifer in the
``ENCRYPTION_KEY_ID`` clause, the server uses the latest version of the
corresponding key. For example, the clause ``ENCRYPTION_KEY_ID=2`` refers to the
latest version of the ``percona_innodb-2`` key from the keyring.

In case the ``percona-innodb-`` key with the requested ID does not exist in the
keyring, |Percona Server| will create it with version 1. If a new
``percona-innodb-`` key cannot be created with the requested ID, the whole
``CREATE TABLE`` statement fails

.. rubric:: FORCE_KEYRING

:Availability: This value is **Experimental** quality

New tables are created encrypted and keyring encryption is enforced.

.. rubric:: ONLINE_TO_KEYRING

:Availability: This value is **Experimental** quality

All tables created or altered without the ``ENCRYPTION=NO`` clause
are encrypted with the latest version of the default encryption key. If a table
being altered is already encrypted with the master key, the table is recreated
encrypted with the latest version of the default encryption key.

.. rubric:: ONLINE_TO_KEYRING_FORCE

:Availability: This value is **Experimental** quality

It is only possible to apply the keyring encryption when creating or altering
tables.

.. note::

   The ``ALTER TABLE`` statement changes the current encryption mode only if you
   use the ``ENCRYPTION`` clause.

.. seealso::

   |MariaDB| Documentation: ``innodb_encrypt_tables`` Option
      https://mariadb.com/kb/en/library/xtradbinnodb-server-system-variables/#innodb_encrypt_tables

.. variable:: innodb_online_encryption_threads

   :cli: ``--innodb-online-encryption-threads``
   :dyn: Yes
   :scope: Global
   :vartype: Numeric
   :default: 1

This variable works in combination with the :variable:`innodb_encrypt_tables`
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


Installation
------------

The safest way to load the plugin is to do it on the server startup by
using `--early-plugin-load variable
<https://dev.mysql.com/doc/refman/8.0/en/server-options.html#option_mysqld_early-plugin-load>`_
option:

.. code-block:: bash

  --early-plugin-load="keyring_vault=keyring_vault.so" \
  --loose-keyring_vault_config="/home/mysql/keyring_vault.conf"

It should be loaded this way to be able to facilitate recovery for encrypted
tables.

.. warning::

  If server should be started with several plugins loaded early,
  ``--early-plugin-load`` should contain their list separated by semicolons. Also it's a good practice to put this list in double quotes so that semicolons
  do not create problems when executed in a script.

Apart from installing the plugin you also need to set the
:variable:`keyring_vault_config` variable. This variable should point to the
keyring_vault configuration file, whose contents are discussed below.

This plugin supports the SQL interface for keyring key management described in
`General-Purpose Keyring Key-Management Functions
<https://dev.mysql.com/doc/refman/8.0/en/keyring-udfs-general-purpose.html>`_
manual.

To enable the functions you'll need to install the ``keyring_udf`` plugin:

.. code-block:: mysql

  mysql> INSTALL PLUGIN keyring_udf SONAME 'keyring_udf.so';

Usage
--------------------------------------------------------------------------------

On plugin initialization ``keyring_vault`` connects to the Vault server using
credentials stored in the credentials file. Location of this file is specified
in by :variable:`keyring_vault_config`. On successful initialization it
retrieves keys signatures and stores them inside an in-memory hash map.

Configuration file should contain the following information:

* ``vault_url`` - the address of the server where Vault is running. It can be a
  named address, like one in the following example, or just an IP address. The
  important part is that it should begin with ``https://``.

* ``secret_mount_point`` - the name of the mount point where ``keyring_vault``
  will store keys.

* ``token`` - a token generated by the Vault server, which ``keyring_vault``
  will further use when connecting to the Vault. At minimum, this token should
  be allowed to store new keys in a secret mount point (when ``keyring_vault``
  is used only for transparent data encryption, and not for ``keyring_udf``
  plugin). If ``keyring_udf`` plugin is combined with ``keyring_vault``, this
  token should be also allowed to remove keys from the Vault (for the
  ``keyring_key_remove`` operation supported by the ``keyring_udf`` plugin).

* ``vault_ca [optional]`` - this variable needs to be specified only when the
  Vault's CA certificate is not trusted by the machine that is going to connect
  to the Vault server. In this case this variable should point to CA
  certificate that was used to sign Vault's certificates.

.. warning::

   Each ``secret_mount_point`` should be used by only one server - otherwise
   mixing encryption keys from different servers may lead to undefined
   behavior.

An example of the configuration file looks like this: ::

  vault_url = https://vault.public.com:8202
  secret_mount_point = secret
  token = 58a20c08-8001-fd5f-5192-7498a48eaf20
  vault_ca = /data/keyring_vault_confs/vault_ca.crt

When a key is fetched from a ``keyring`` for the first time the
``keyring_vault`` communicates with the Vault server, and retrieves the key
type and data. Next it queries the Vault server for the key type and data and
caches it locally.

Key deletion will permanently delete key from the in-memory hash map and the
Vault server.

.. note::

  |Percona XtraBackup| currently doesn't support backup of tables encrypted
  with :ref:`keyring_vault_plugin`.

System Variables
----------------

.. variable:: keyring_vault_config

  :cli: ``--keyring-vault-config``
  :dyn: Yes
  :scope: Global
  :vartype: Text
  :default:

This variable is used to define the location of the :ref:`keyring_vault_plugin` configuration file.

.. variable:: keyring_vault_timeout

  :cli: ``--keyring-vault-timeout``
  :dyn: Yes
  :scope: Global
  :vartype: Numeric
  :default: ``15``

This variable allows to set the duration in seconds for the Vault server
connection timeout. Default value is ``15``. Allowed range is from ``1``
second to ``86400`` seconds (24 hours). The timeout can be also completely
disabled to wait infinite amount of time by setting this variable to ``0``.

.. seealso::

   Vault Documentation
      https://www.vaultproject.io/docs/index.html
   General-Purpose Keyring Key-Management Functions
      https://dev.mysql.com/doc/refman/8.0/en/keyring-udfs-general-purpose.html
