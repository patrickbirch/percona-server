.. _managing_keyrings

============================================================
Managing Keyrings
============================================================

Data at rest encryption requires a keyring plugin to be installed, configured, and loaded. A keyring stores known keys. The following are the keyring plugin options:

* `keyring_file <https://dev.mysql.com/doc/refman/8.0/en/keyring-file-plugin.html>`_
* :ref:`keyring_vault_plugin`

To load the ``keyring`` plugin when starting the server, use the ``--early-plugin-load`` option:

.. code-block:: bash

   $ mysqld --early-plugin-load="keyring_file=keyring_file.so"

Alternatively, you can add this option to your configuration file:

.. code-block:: guess

   [mysqld]
   early-plugin-load=keyring_file.so

.. warning::

   Enable only one keyring plugin at a time. Implementing multiple keyring plugins at the same time is not supported and may result in data loss.

.. seealso::

   |MySQL| Documentation:
      - `Installing a Keyring Plugin <https://dev.mysql.com/doc/refman/8.0/en/keyring-installation.html>`_
      - `The --early-plugin-load Option <https://dev.mysql.com/doc/refman/8.0/en/server-options.html#option_mysqld_early-plugin-load>`_

.. rubric:: Using the Keyring Vault Plugin

 <add text here>


.. rubric:: Changing the Default Keyring Encryption


When encryption is enabled and the server is configured to use the KEYRING encryption, new tables use the default encryption key.

You many change this default encryption via the

  :variable:`innodb_default_encryption_key_id` variable.

.. seealso::

    Configuring the way how tables are encrypted
    :variable:`innodb_encrypt_tables`

System Variables
------------------------------------------------------------------------------

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

.. rubric:: Keyring Vault

The ``keyring_vault`` plugin can be used to store the encryption keys inside the
`Hashicorp Vault server <https://www.vaultproject.io>`_.

.. important::

   ``keyring_vault`` plugin only works with kv secrets engine version 1 (**shouldn't this be 2?**)

.. seealso::

   HashiCorp Documentation: More information about ``kv`` secrets engine
           https://www.vaultproject.io/docs/secrets/kv/kv-v1.html

.. rubric:: Storing Keys in the Vault

The ``keyring_vault`` plugin can be used to store the encryption keys inside the
`Hashicorp Vault server <https://www.vaultproject.io>`_.

.. important::

   ``keyring_vault`` plugin only works with kv secrets engine version 1 (**shouldn't this be 2?**)

.. seealso::

   HashiCorp Documentation: More information about ``kv`` secrets engine
         https://www.vaultproject.io/docs/secrets/kv/kv-v1.html

.. rubric:: Rotating the Master Key

The Master Key rotation improves security, in case the Master Key is lost, or an unauthorized user has received it. The rotation also improves the speed of the InnoDB startup, when you have restored tables from different backups.

The keyring generates a new master key. For each table, re-encrypts the tablespace key and IV with the new master key and then updates the encryption information in the tablespace header.

The changes in the tablespace header are as follows:

* New Key ID
* New server UUID
* Tablespace key re-Encrypted
* CRC32 re-calculated

Keyring is in cache memory. If you have a core dump, that dump could contain sensitve information, such as the tablespace encryption keys and the Master Key.

For this information to be generated for a core dump, you must have the scope option core-file enabled. If the core file option is not enabled, the keyring information is not avaiable. If you do need the core-file enabled, you should generate the core dump in an encrypted place and use core_pattern.

.. note::

  There is no mitigation for leaked tablespace keys. If a third-party application accesses the tablespace key, the Master Key rotation will not change that.

.. rubric:: Rotating Keys

ADD TEXT

.. rubric:: Rotating System Keys

System encryption keys can be rotated. A new version of a key is generated.

The PS 5.7 and < 8.0.14 the following is encrypted:

* percona_binlog
* percona_innodb (experimental)
* percona_redo (experimental)

From Percona Server >= 8.0.14
* percona_innodb (experimental)

The system key encryption is a feature of the encryption threads, which are **experimental**.

Key versioning updates the key_id in keyring with a new version.

Run the following command to version the system encryption keys:

.. code-block:: mysql

   $ Select rotate_system_key("percona_binlog");
