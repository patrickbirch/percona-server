.. _keyring_vault_plugin:

============================================================
Keyring Vault Plugin
============================================================


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
