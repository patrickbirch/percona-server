.. _keyring_vault_plugin:

==============================================================================
Keyring Vault Plugin
==============================================================================


Requirements
================================================================================

Data at rest encryption requires that a keyring plugin, such as `keyring_file
<https://dev.mysql.com/doc/refman/8.0/en/keyring-file-plugin.html>`_ or
:ref:`keyring_vault_plugin` be installed and already loaded. To load the
``keyring`` plugin when starting the server, use the ``--early-plugin-load``
option:

.. code-block:: bash

   $ mysqld --early-plugin-load="keyring_file=keyring_file.so"

Alternatively, you can add this option to your configuration file:

.. code-block:: guess

   [mysqld]
   early-plugin-load=keyring_file.so

.. warning::

   Only one keyring plugin should be enabled at a time. Enabling multiple
   keyring plugins is not supported and may result in data loss.

.. seealso::

   |MySQL| Documentation:
      - `Installing a Keyring Plugin <https://dev.mysql.com/doc/refman/8.0/en/keyring-installation.html>`_
      - `The --early-plugin-load Option <https://dev.mysql.com/doc/refman/8.0/en/server-options.html#option_mysqld_early-plugin-load>`_


Changing the Default Keyring Encryption
================================================================================

When encryption is enabled and the server is configured to use the KEYRING
encryption, new tables use the default encryption key.

You many change this default encryption via the
:variable:`innodb_default_encryption_key_id` variable.

.. seealso::

   Configuring the way how tables are encrypted
      :variable:`innodb_encrypt_tables`

System Variables
--------------------------------------------------------------------------------

.. variable:: innodb_default_encryption_key_id

   :cli: ``--innodb-default-encryption-key-id``
   :dyn: Yes
   :scope: Session
   :vartype: Numeric
   :default: 0

The ID of the default encryption key. By default, this variable contains **0**
to encrypt new tables with the latest version of the key ``percona_innodb-0``.

To change the default value use the following syntax:

.. code-block:: guess

   mysql> SET innodb_default_encryption_key_id = NEW_ID

Here, **NEW_ID** is an unsigned 32-bit integer.


.. _data-at-rest-encryption.key-rotation:

Using Key Rotation
================================================================================

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

Using the Keyring Vault plugin
==============================

The ``keyring_vault`` plugin can be used to store the encryption keys inside the
`Hashicorp Vault server <https://www.vaultproject.io>`_.

.. important::

   ``keyring_vault`` plugin only works with kv secrets engine version 1 (**shouldn't this be 2?**)

   .. seealso::

      HashiCorp Documentation: More information about ``kv`` secrets engine
         https://www.vaultproject.io/docs/secrets/kv/kv-v1.html



Notes to keyrings

The plugin must be loaded to access the variables. The user must edit the keyring variables:
For the keyring_vault, the user must set up keyring_vault_config to the file with the configurations to connect to the vault servers

Edit the keyring_file_data for the location where the keyring file stores the encryption keys.

A keyring file loads all of the encryption and metadata into a text file that contains the following columns:

* Key Identifier
* Key Type
* Key Owner
* Key Length
* Key

The keyring vault only loads the key identifier and the key owner. If the user must select from an encrypted table and the key is not stored in the keyring vault file,

When the user writes to keyring_file, the complete file is rewritten. Before the fire is rewritten, the current file is saved to a backup file. This backup file is deleted on the next reboot of the server.

A write to the keyring_vault only one key is sent.

Each server should store its own keyring. There is a keyring UDF plugin the user can use to insert keys into the keyring. Attempting to insert the same key in to servers only one key would succeed.

This separation of keyrings is not important for master key separation because the master key contains the UUID of the server embedded into the key. This embedded information does not allow the master key to repeat between servers.

The keyring vault configuration file is as follows:

* vault_url
* secret_mount_point - the location of the encryption keys on the vault server
* token
* vault_ca (optional) - the user can add the certificate to the certificate trusted by the vault server or add a path to the certificate.

The Keyring_vault has two options. The user can create a mount point on each server. The user can automate the creation with the following `curl` statement.

.. code-block:: bash

  curl -L "X-=Vault_Token:TOKEN" ca-cert VAULT-CA --data '{"type":"generic"}'
  --request POST
  VAULT_URL/v1/sys/mounts/SECRET_MOUNT_POINT

The second option is, in the configuration file, create a separate *directory* for the mount point inside for each vault server. This tells the vault server to create the directory the first time a secret is sent and the vault server removes the directory when the last encryption key.

.. code-block:: guess

  config for server1: secret_mount_point=<mount_point>/server1
  config for server2: secret_mount_point=<mount_point>/server1

The keys stored inside the Vault server are base64 encoded. You can decode the key by using `base64 -d`.

A Keyring_UDF plugin provides a set of UDFs. The plugin allows you to generate keys inside of keyrings and storing other generated keys. The UDF-generated keys do not contain a server UUID, therefore there is no natural separation of keys. You must separate the keys by server.

used for storing user's secret inside keyrings

Set of UDFS include the following:

* keyring_key_generate
* keyring_key_fetch
* keyring_key_length_fetch
* keyring_key_type_fetch
* keyring_key_store
* keyring_key_remove

Keys do not contain the server's UUID

..rubric:: Master Key Rotation

The Master Key rotation improves security, in case the Master Key is lost, or an unauthorized user has received it. The rotation also improves the speed of the InnoDB startup, when you have restored tables from different backups.

The keyring generates a new master key. For each table, re-encrypts the tablespace key and IV with the new master key and then updates the encryption information in the tablespace header.

The changes in the tablespace header are as follows:

* New Key ID
* New server UUID
* Tablespace key re-Encrypted
* CRC32 re-calculated

Keyring is in cache memory. If you have a core dump, that dump could contain sensitve information, such as the tablespace encryption keys and the Master Key.

For this information to be generated for a core dump, you must have the scope option core-file enabled. If the core file option is not enabled, the keyring information is not avaiable. If you do need the core-file enabled, you should generate the core dump in an encrypted place and use core_pattern.

.. Note::

  There is no mitigation for leaked tablespace keys. If a third-party application accesses the tablespace key, the Master Key rotation will not change that.
