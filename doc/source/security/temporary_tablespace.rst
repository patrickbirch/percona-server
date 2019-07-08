.. _temporary_tablespace:

==============================================================================
Encrypting Temporary Tablespace Files
==============================================================================

:Availability: This feature is of **Experimental** quality.

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

To use this option the keyring plugin must be loaded. If the keyring is not available, the server returns an error message and refuses to create new temporary tables.

.. variable:: encrypt-tmp-files

  :cli: ``--encrypt-tmp-files``
  :dyn: No
  :scope: Global
  :vartype: Boolean
  :default: ``OFF``

The option turns on encryption of temporary files created by |Percona Server|.

.. variable:: innodb_temp_tablespace=ON/OFF

The option turns on server encrypts the temporary tablespace and temporary InnoDB file-per-table tablespaces. The option does not force encryption of currently open temporary tables. If the option is enabled at system startup, the temporary tablespace contains encrypted tables. Turning the option off at runtime allows the creation of every subsequent temporary file-per-table tablespace is unencrypted, but does not turn off the encryption of the system temporary tablespace.


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

  System Variables
  ----------------

  .. variable:: innodb_temp_tablespace_encrypt

    :cli: ``--innodb-temp-tablespace-encrypt``
    :dyn: Yes
    :scope: Global
    :vartype: Boolean
    :default: ``Off``

  When this option is set to ``ON``, the server encrypts the global temporary
  tablespace (:file:`ibtmp*` files) and the session temporary tablespaces
  (:file:`#innodb_temp/temp_*.ibt` files). This option does not enforce the
  encryption of temporary tables which are currently open, and it does not rebuild
  the system temporary tablespace to encrypt data which are already written.

  The ``ENCRYPTION`` option is not allowed in the ``CREATE TEMPORARY TABLE``
  statement. The ``TABLESPACE`` option cannot be set to `innodb_temporary`. The
  global temporary tablespace datafile ``ibtmp1`` holds temporary table undo logs
  while intrinsic temporary tables and user temporary tables go to the encrypted
  session temporary tablespace.

  Since the global temporary tablespaces are created fresh at each server startup,
  it will not contain unencrypted data if this option is specified as a server
  argument.

  Setting :variable:`innodb_temp_tablespace_encrypt` to ``OFF`` with
  :variable:`innodb_encrypt_tables` set to ``OFF`` at runtime makes the server
  create new temporary tablespaces unencrypted. Intrinsic tables to go unencrypted
  session temporary tablespaces. Existing encrypted user temporary and intrinsic
  temporary tables remain in encrypted session temporary tablespaces and are only
  destroyed when the session is disconnected.

  When :variable:`innodb_temp_tablespace_encrypt` is ``OFF`` while
  :variable:`innodb_encrypt_tables` is ``ON`` at startup, the temporary tablespace
  datafile ``ibtmp1``, which only contains undo logs, is not encrypted. However,
  user-created and intrinsic temporary tables go to the encrypted session
  temporary tablespace.

  This feature is considered **BETA** quality.

    .. important::

     To use this option, a keyring plugin must be loaded, otherwise the server
     produces an error message and refuses to create new temporary tables.

  .. seealso::

     |MySQL| Documentation
        https://dev.mysql.com/doc/refman/8.0/en/create-temporary-table.html

  .. variable:: innodb_encrypt_tables

    :cli: ``--innodb-encrypt-tables``
    :dyn: Yes
    :scope: Global
    :vartype: Text
    :default: ``OFF``

  The implementation of the behavior controlled by this variable is considered
  **BETA** quality.
