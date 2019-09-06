.. _keyring:

========================================================
Keyring
========================================================

.. _data-at-rest-encryption.prerequisite:


Prerequisites
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


.. _data-at-rest-encryption.keyring.changing-default:

Installation
==============================================================================

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
  ``--early-plugin-load`` should contain their list separated by semicolons. Also
  it's a good practice to put this list in double quotes so that semicolons
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

Changing the Default Keyring Encryption
================================================================================

When encryption is enabled and the server is configured to use the KEYRING
encryption, new tables use the default encryption key.

You many change this default encryption via the
:variable:`innodb_default_encryption_key_id` variable.

.. seealso::

   Configuring the way how tables are encrypted
      :variable:`default_table_encryption`

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


Keyring Encryption
================================================================================

:Availabiliity: This feature is **Experimental** quality

The keyring management is enabled for each table (per file table) separately when you set the encryption in the ``ENCRYPTION`` clause to ``KEYRING`` in the supported SQL statement.

- CREATE TABLE ... ENCRYPTION='KEYRING'
- ALTER TABLE .. ENCRYPTION='KEYRING'

.. note::

  Running ``ALTER TABLE ... ENCRYPTION='KEYRING'`` on the table created with ``ENCRYPTION='KEYRING'`` converts the table back to the existing MySQL scheme, tablespace, or table encryption state.


.. _keyring_vault_plugin:

Keyring Vault plugin
====================

The ``keyring_vault`` plugin can be used to store the encryption keys inside the
`Hashicorp Vault server <https://www.vaultproject.io>`_.

.. important::

   ``keyring_vault`` plugin only works with kv secrets engine version 1.

   .. seealso::

      HashiCorp Documentation: More information about ``kv`` secrets engine
         https://www.vaultproject.io/docs/secrets/kv/kv-v1.html


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

This variable is used to define the location of the
:ref:`keyring_vault_plugin` configuration file.

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


