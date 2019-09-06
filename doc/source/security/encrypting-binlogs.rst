.. _encrypting-binlogs:

================================================================================
Encrypting Binary Logs
================================================================================

After you have enabled the ``binlog_encryption`` option and the keyring is available, you can encrypt new binary logs and relay logs on disk. Only the data content is encrypted.

Attempting binlog encryption without the keyring generates a MySQL error.

The Binary log encryption uses two tiers:

    * File password

    * Binary log encryption key

The file password encrypts the content of a single binary file or relay log file. The binary log encryption key is used to encrypt the file password and is stored in the keyring.

Enabling Binary Log Encryption
-------------------------------
To enable the ``binlog_encryption`` option you must set the option in a startup configuration file, such as the my.cnf file.

.. code-block:: MySQL

    binlog_encryption=ON

Verifying the Encryption Setting
----------------------------------

You can verify if the binary log encryption option is enabled, you can run the following statement:

.. code-block:: MySQL

  mysql>SHOW BINARY LOGS;

  +-------------------+----------------+---------------+
  | Log_name          | File_size      | Encrypted     |
  +-------------------+----------------+---------------+
  | binlog.00011      | 72367          | No            |
  | binlog:00012      | 71503          | No            |
  | binlog:00013      | 73762          | Yes           |
  +-------------------+----------------+---------------+

An encrypted file has a 512 bytes header.

.. seealso::

  |MySQL| Documentation:
  - `Encrypting Binary Log Files and Relay Log Files <https://dev.mysql.com/doc/refman/8.0/en/replication-binlog-encryption.html>`__
