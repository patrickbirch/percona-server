.. rn:: 8.0.16-7
================================================================================
|Percona Server| |release|
================================================================================
|Percona| announces the release of |Percona Server| |release| on |date|
(downloads are available `here
<https://www.percona.com/downloads/Percona-Server-8.0/>`__ and from the `Percona
Software Repositories
<https://www.percona.com/doc/percona-server/8.0/installation.html#installing-from-binaries>`__).
This release includes fixes to bugs found in previous releases of |Percona
Server| 8.0.
|Percona Server| |release| is now the current GA release in the 8.0
series. All of |Percona|’s software is open-source and free.

Percona Server for MySQL 8.0 includes all the `features available in MySQL 8.0.16
Community Edition
<https://dev.mysql.com/doc/relnotes/mysql/8.0/en/news-8-0-16.html>`__ in addition to
enterprise-grade features developed by Percona.  For a list of highlighted
@@ -35,7 +35,7 @@ features from both MySQL 8.0 and Percona Server for MySQL 8.0, please see the
New Features
================================================================================

- `Key rotation for the redo log <https://www.percona.com/doc/percona-server/LATEST/management/data_at_rest_encryption.html>`__ has been redesigned to rotate the key with `SELECT rotate_system_key("percona_redo")`. 

Bugs Fixed
================================================================================
- The :variable: `buf_dblwr_flush_buffered_writes` must crash the server when an I/O error occurs to the parallel doublewrite buffer. The doublewrite buffer error returns to the caller. Bug fixed :psbug:`5678`.
- After resetting the :variable:`innodb-temp-tablespace-encrypt` to `OFF` during runtime the subsequent file-per-table temporary tables continue to be encrypted. Bug fixed :psbug:`5734`.
- The `key rotation process <https://www.percona.com/doc/percona-server/LATEST/management/data_at_rest_encryption.html>`__ was redesigned. The updated process allows the key rotation with `SELECT rotate_system_key("percona_redo")` and the currently used key version is displayed in the `innodb_redo_key_version` variable.  Bug fixed :psbug:`5565`.
- Setting the encryption `ON` for the system tablespace generates an encryption key and encrypts system temporary tablespace pages. Resetting the encryption to `OFF`, all subsequent pages are written to the temporary tablespace without encryption. To allow any encrypted tables to be decrypted, the generated keys are not erased. Modifying the :variable:`innodb_temp_tablespace_encrypt` does not affect file-per-table temporary tables. This type of table is encrypted if `ENCRYPTION='y'` at table creation.  Bug fixed :psbug:`5736`.
- An instance started with the default values but setting the redo log to encrypt without specifying the keyring plugin parameters does not fail or throw an error.  Bug fixed :psbug:`5476`.
- The :variable:`rocksdb_large_prefix` allows index key prefixes up to 3072 bytes. The default value is changed to `TRUE` to match the behavior of the :variable:`innodb_large_prefix`. :psbug:`5655 `.
- On a server with two million or more tables, a user experiences a shutdown in less than ten minutes.  Bug fixed :psbug:`5639`.
- The changed page tracking may read pages which have the encryption bit set.  The redo log does not have the encryption key and decryption fails and generates an error message. A `flag <https://www.percona.com/doc/percona-server/LATEST/management/data_at_rest_encryption.html>`__ lets the read process safely ignore encryption errors in this case.  Bug fixed :psbug:`5541`.
- Large page allocations with the :variable:`innodb_buffer_pool_chunk_size` set to a shared memory segment larger than 4GB or more generates an incorrect size. Bug fixed :psbug:`5517`.
- The TokuDB hot backup library continually dumps TRACE information to stdout.  The user cannot enable or disable the dump of this information. Bug fixed :psbug:`4850`.
@@ -81,24 +81,24 @@
:psbug:`5688`,
:psbug:`5695`,
:psbug:`5752`,
:psbug:`5753`,
:psbug:`5129`,
:psbug:`5681`,
:psbug:`5310`,
:psbug:`5713`,
:psbug:`5681`,
:psbug:`5696`,
:psbug:`3845`,
:psbug:`5149`,
:psbug:`5581`,
:psbug:`5697`,
:psbug:`5733`,
:psbug:`5724`,
:psbug:`5767`,
:psbug:`5782`,
:psbug:`5746`, and
:psbug:`5748`.


.. |release| replace:: 8.0.16-7
.. |date| replace:: August 07, 2019