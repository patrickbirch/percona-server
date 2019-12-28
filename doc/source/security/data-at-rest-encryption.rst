.. _data_at_rest_encryption:

================================================================================
Transparent Data Encryption
================================================================================

.. contents::
   :local:

The purpose of encrypting the data at rest ensures that if an unauthorized user
accesses the data files from the file system, the user cannot read contents.
``Transparent Data Encryption (TDE)`` or ``Data at Rest Encryption`` encrypts
data files and log files.

An encrypted page is decrypted at the I/O
layer and added to the buffer pool and used to access the data. A buffer pool
page is not encrypted. The the I/O layer encrypts the page is before the page is
flushed to disk.

.. note::

   |Percona XtraBackup| version 8 supports the backup of encrypted general
   tablespaces. Features which are not Generally Available (GA) in |Percona
   Server| are not supported in version 8.

.. seealso::

    :ref:`using-keyring-plugin`

    :ref:`encrypting-threads`
