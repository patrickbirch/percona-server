.. _temporary_tablespace:

==============================================================================
Temporary Tablespace
==============================================================================

Temporary file encryption
================================================================================

:Availability: This feature is of **experimental** quality.

The encryption of temporary files is triggered by the
:variable:`encrypt-tmp-files` option.

Temporary files are currently used in |Percona Server| for the following
purposes:

* filesort (for example, ``SELECT`` statements with ``SQL_BIG_RESULT`` hints),
* binary log transactional caches,
* Group Replication caches.

For each temporary file, an encryption key is generated locally, only kept
in memory for the lifetime of the temporary file, and discarded afterwards.

System Variables
----------------

.. variable:: encrypt-tmp-files

  :cli: ``--encrypt-tmp-files``
  :dyn: No
  :scope: Global
  :vartype: Boolean
  :default: ``OFF``

The option turns on encryption of temporary files created by |Percona Server|.

FR01. innodb_temp_tablespace_encrypt=ON/OFF will have no impact during server bootstrap (data directory initialisation), as the temporary tablespace is created after server is started.

FR02. Server started with --innodb_temp_tablespace_encrypt=ON will encrypt the system temporary tablespace.

FR03. Server started with --innodb_temp_tablespace_encrypt=ON will encrypt file-per-table temporary tablespace.

FR04. Server started with --innodb_temp_tablespace_encrypt=OFF will NOT encrypt the system temporary tablespace.

FR05. Server started with --innodb_temp_tablespace_encrypt=ON will NOT encrypt file-per-table temporary tablespace.

FR06. If server started with --innodb_temp_tablespace_encrypt=ON, changing the value to OFF at runtime will create all subsequent temporary file-per-table tablespaces unencrypted

FR07. If server started with --innodb_temp_tablespace_encrypt=ON, changing the value to OFF at runtime will NOT turn off encryption for subsequently created tables in system temporary tablespace.

FR08. If server started with --innodb_temp_tablespace_encrypt=OFF, changing the value to ON at runtime will create all subsequent temporary file-per-table tablespaces encrypted

FR09. If server started with --innodb_temp_tablespace_encrypt=OFF, changing the value to ON at runtime will turn on encryption for subsequently created tables in system temporary tablespace.

FR10. Changing the --innodb_temp_tablespace_encrypt=ON/OFF, will have no changes on the already exisiting data in both file-per-table or system temporary tablespace

.. rubric:: Encrypting a file-per-table temporary table

Set the innodb-temp-tablespace-encrypt=ON option and then start the server.

Create a temporary table with the following command:

.. code-block:: mysql

CREATE TEMPORARY TABLE t1(a int) ROW_FORMAT=COMPRESSED ENCRYPTION='Y';

.. note::

  If the server is started with innodb-encrypt-tables=ON the temporary table is automatically created with the  ENCRYPTION='Y' option. The inclusion of the option in the example is for completeness.
