.. _data_at_rest_encryption:

================================================================================
Data at Rest Encryption
================================================================================

.. contents::
   :local:

Data security is a concern for institutions and organizations. Data at rest is
any data which is not accessed or changed frequently, stored on different types
of storage devices. Encryption ensures that if an unauthorized user accesses the data files from
the file system, the user cannot read contents. 

The MySQL keyring plugin stores the master key, which is used to encrypt the
data in the tablespace. 

The InnoDB Tablespace encryption has the following components:

    * The database instance has one master key. This key encrypts all
      of the tablespace keys.

    * Each tablespace has a tablespace key. The key is used to encrypt the
      Tablespace data pages. Encrypted tablespace keys are written on tablespace header.

Two separate keys allow the master key to be rotated in a minimal operation. When the master key is
rotated, each tablespace key is decrypted and re-encrypted with the new
master key. Only the first page of every tablespace (.ibd) file is read and
written during the key rotation.

An InnoDB table file is comprised of multiple logical and physical pages. Page 0 is
the tablepace header page and keeps the metadata for the tablespace. Page 0 is
not encrypted. The encryption information is stored on page 0. 

A buffer pool page is not encrypted. An encrypted page is decrypted at the I/O
layer and added to the buffer pool and used to access the data. The page is encrypted by the I/O before the page is flushed to disk.


