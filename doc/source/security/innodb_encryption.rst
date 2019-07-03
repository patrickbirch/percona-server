.. _innodb_encryption

==============================================================================
Innodb Encryption
============================================================

InnoDB System Tablespace Encryption
============================================================

:Availabiliity: This feature is **Experimental** quality

The InnoDB system tablespace is encrypted by using master key encryption. The
server must be started with the ``--bootstrap`` option.

If the variable :variable:`innodb_sys_tablespace_encrypt` is set to ON and the
server has been started in the bootstrap mode, you may create an encrypted table
as follows:

.. code-block:: guess

   mysql> CREATE TABLE ... TABLESPACE=innodb_system ENCRYPTION='Y'

.. note::

   You cannot encrypt existing tables in the System tablespace.

It is not possible to convert the system tablespace from encrypted to
unencrypted or vice versa. A new instance should be created and user tables must
be transferred to the desired instance.

You can encrypt the already encrypted InnoDB system tablespace (key rotation)
with a new master key by running the following ``ALTER INSTANCE`` statement:

.. code-block:: guess

   mysql> ALTER INSTANCE ROTATE INNODB MASTER KEY

.. rubric:: Doublewrite Buffers

The two types of doublewrite buffers used in |Percona Server| are encrypted
differently.

When the InnoDB system tablespace is encrypted, the ``doublewrite buffer`` pages
are encrypted as well. The key which was used to encrypt the InnoDB system
tablespace is also used to encrypt the doublewrite buffer.

|Percona Server| encrypts the ``parallel doublewrite buffer`` with the respective
tablespace keys. Only encrypted tablespace pages are written as encrypted in the
parallel doublewrite buffer. Unencrypted tablespace pages will be written as
unencrypted.

.. important::

   A server instance bootstrapped with the encrypted InnoDB system tablespace
   cannot be downgraded. It is not possible to parse encrypted InnoDB system
   tablespace pages in a version of |Percona Server| lower than the version
   where the InnoDB system tablespace has been encrypted.


System variables
--------------------------------------------------------------------------------

.. variable:: innodb_sys_tablespace_encrypt

   :cli: ``--innodb-sys-tablespace-encrypt``
   :dyn: No
   :scope: Global
   :vartype: Boolean
   :default: ``OFF``

Enables the encryption of the InnoDB System tablespace. It is essential that the
server is started with the ``--bootstrap`` option.

.. seealso::

   |MySQL| Documentation: ``--bootstrap`` option
      https://dev.mysql.com/doc/refman/8.0/en/server-options.html#option_mysqld_bootstrap

.. variable:: innodb_parallel_dblwr_encrypt

   :cli: ``--innodb-parallel-dblwr-encrypt``
   :dyn: Yes
   :scope: Global
   :vartype: Boolean
   :default: ``OFF``

Enables the encryption of the parallel doublewrite buffer. For encryption, uses
the key of the tablespace where the parallel doublewrite buffer is used.


.. _innodb_general_tablespace_encryption:

InnoDB General Tablespace Encryption
================================================================================

In |Percona Server| :rn:`5.7.20-18` existing tablespace encryption support has
been extended to handle general tablespaces. A general tablespace is either
fully encrypted, covering all the tables inside, or not encrypted at all.
It is not possible to encrypt some of the tables in a general
tablespace.

This feature extends the  `CREATE TABLESPACE
<https://dev.mysql.com/doc/refman/8.0/en/create-tablespace.html>`_
statement to accept the ``ENCRYPTION='Y/N'`` option.

.. note::

   Prior to |Percona Server| 8.0.13, the ``ENCRYPTION`` option was specific to
   the ``CREATE TABLE`` or ``SHOW CREATE TABLE`` statement.  In |Percona Server|
   8.0.13, this option becomes a tablespace attribute and is not allowed with
   the ``CREATE TABLE`` or ``SHOW CREATE TABLE`` statement except for
   file-per-table tablespaces.


Usage
================================================================================

General tablespace encryption is enabled by the following syntax extension:

.. code-block:: mysql

   mysql> CREATE TABLESPACE tablespace_name ... ENCRYPTION='Y'

Attempts to create or to move tables, including partitioned ones, to a general
tablespace with an incompatible encryption setting are diagnosed and aborted.

As you cannot move tables between encrypted and unencrypted tablespaces,
you will need to create another table, add it to a specific tablespace and run
``INSERT INTO SELECT`` from the table you want to move from, and then you will
get encrypted or decrypted table with your desired content.

Example
================================================================================

To create an encrypted tablespace run: :mysql:`CREATE TABLESPACE foo ADD DATAFILE 'foo.ibd' ENCRYPTION='Y';`

To add an encrypted table to that table space run: :mysql:`CREATE TABLE t1 (a INT, b TEXT) TABLESPACE foo ENCRYPTION="Y";`

Trying to add unencrypted table to this table space will result in an error:

.. code-block:: mysql

   mysql> CREATE TABLE t3 (a INT, b TEXT) TABLESPACE foo ENCRYPTION="N";
   ERROR 1478 (HY000): InnoDB: Tablespace `foo` can contain only an ENCRYPTED tables.

.. note::

   |Percona XtraBackup| currently doesn't support backup of encrypted general
   tablespaces.

   Master Key encryption


   A tablespace consists of pages.

   There is always one Master Key and a set of keys. The set of keys is encrypted with the Master Key. In the Innnodb world master key resides in the keyring and the keys reside in the tablespace headers. When you create a tablespace and encrypt the tablespace, the server generates a random key, encrypts the key with the master key, and stores the key in the tablespace header.

   Tablespace's encryption header resides in page 0. Page 0 is never encrypted. The following are stored in the header:

   * Key ID - restores the master key key name
   * UUID - server
   * Tablespace key and Initialization Vector (IV) - combined and encrypted with the master key
   * CRC32 checksum of the plaintext tablespace key and IV

   .. note::
      The Key ID always starts with one. If you create a key in the first table, the key id will be `1`.

   The Master Key uses the CRC32 checksum to verify the key for each server. The process uses the Master Key to decrypt the tablespace key and IV and check if the CRC32 matches.

   `INNDODBKey-srv_uuid-master_key_id`

   Encrypted tables validation verifies that you can decrypt the tables. At startup, InnoDB reads the page 0, reads the encryption information from page 0, retrieves the Master Key, decrypts the tablespace key and IV and checks the CRC32. If any of these tasks fail, the tablespace is marked as `missing`. The user will not be able to access a missing table.

   In cryptology, the encryption algorithm may act on the plaintext in several ways:

   * Stream ciphers - the sequence is encrypted bit-by-bit
   * Block ciphers - the sequence is divided into blocks of a predetermined size and then encrypted

   Block ciphers allow you to encrypt the same information in different ways, depending on the block size, with a key. To encrypt a data stream, which can have an indeterminate length, you use block modes. The purpose of a block mode is to make the data secure by encrypting multiple blocks with the same key.

   Advanced Encryption Standard (AES) is used to secure the data. Basically, InnoDB uses the following block modes:

   * AES 256 ECB for tablespace key and initialization vector encryption (hardcoded)
   * AES 256 CBC for page encryption (hardcoded)

   .. Note::

     The modes are hardcoded and cannot be changed.

   Electronic Codebook (ECB) is the basic form of block cipher encryption. This version of encryption could leak information about the plaintext. Repetitive patterns in the plaintext always result in repetitive patterns in the ciphertext. This information can lead an unauthorized user to detect the following by reviewing ECB-encrypted ciphertexts:

   * If the two ciphertexts are identical
   * If the two ciphertexts share common prefix
   * If the two ciphertexts share common substrings
   * If the ciphertext contains repetitive data, repeated headers, or repeated phrases

   Using the ECB mode to encrypt tablespace keys are secure because the tablespace key is a random number, which should lessen the probability of repitition.

    Cipher Blocking Chaining (CBC) introduces the ability to use the previous block and the current block when encrypting the current block, which creates a cascading effect. The initialization vector (IV) allows you to encrypt the first block. You pick the unique IV, then no two ciphertexts are the same.

    The 256-bit encryption refers to the size of the key. The larger key size provides more possible keys. The 256-bit key length gives the maximum difficulty and the longest time before the code could possibly be broken.

   Do no confuse with block_encryption_mode variable


  Core dumps - could contain sensitive information like tablespace encryption keys and Master Key:

    * Option core-file
    * Should be generated in encrypted place (core_pattern)

No mitigation for leaked tablespace keys.

Tablespace keys comes directly from the keyring. Set `innodb_default_ENCRYPTION_KEY_ID=0`

Encryption threads

Background threads

Nubmer of threads is set by variable_innodb_encryption_threads can:

* encrypt and decrypt tables (`innodb_encrypt_tables`)
* re-encrypt tables - with new version of encryption key (key rotation)

innodb_encrypt_tables:= ONLINE_TO_KEYRING | ONLINE_TO_KEYRING_FORCE | ONLINE_FROM_KEYRING_TO_UNENCRYPTED

SET GLOBAL innodb_encrypt_tables = ONLINE_TO_KEYRING;
SET GLOBAL innodb_encryption_threads = 4;
SET GLOBAL innodb_default_encryption_key_id = 0;

`CREATE TABLE t1 (a VARCHAR(255));`

Re-encryption of a table with key rotation.
innodb_encryption_rotate_key_age
  = 1 - re-encrypt all the tables every key is rotated
  = 2 - re-encrypt all the tables every second time the key is rotated
  = 3 - re-encrypt all the tables every third time the key is rotated
  (and so on)
  = 0 - disable re-ENCRYPTION

  `SET GLOBAL rotate_system_key("percona_innodb-0");`

  Examples:

  CREATE TABLE t1 ENCRYPTION='N'; - t1 stays unencrypted "forever"
  CREATE TABLE t1 ENCRYPTION_KEY_ID=X; - table is encrypted with key X when the encryption threads
  The same commands work with ALTER
  innodb_default_encryption_key_id:

    - SESSION scope used by ENCRYPTION='KEYRING'
    - GLOBAL scope used by encryption threads

  If the tables are already encrypted with the Master Key. The tables are re-encrypted with keyring encryption by encryption threads. If the tables are already encrypted with keyring encryption, nothing changes. The tables are already in INNODB_TABLESPACE_ENCRYPTION.

  Decryption with encryption threads
  innodb_encrypt_tables=ONLINE_FROM_KEYRING_TO_UNENCRYPTED

  will only decrypt tables that were encrypted by encryption threads
