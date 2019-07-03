.. _binary_log_encryption

==============================================================================
Binary Log Encryption
==============================================================================

Binary log encryption
=====================

As described in the |MySQL| documentation, the encryption of binary and relay
logs is triggered by the `binlog_encryption
<https://dev.mysql.com/doc/refman/8.0/en/replication-options-binary-log.html#sysvar_binlog_encryption>`_
variable.

While replicating, master sends the stream of decrypted binary log events to a
slave (SSL connections can be set up to encrypt them in transport). That said,
masters and slaves use separate keyring storages and are free to use differing
keyring plugins.

Dumping of encrypted binary logs involves decryption, and can be done using
``mysqlbinlog`` with ``--read-from-remote-server`` option.

.. note:: Taking into account that ``--read-from-remote-server`` option  is only
   relevant to binary logs, encrypted relay logs can not be dumped/decrypted
   in this way.


.. rubric:: Upgrading from |Percona Server| |changed-version| to any higher version

.. include:: ../.res/text/encrypt_binlog.removing.txt

.. |changed-version| replace:: 5.7.20-19

System Variables
----------------

.. variable:: encrypt_binlog

   :version-info: removed in :rn:`8.0.15-5`
   :cli: ``--encrypt-binlog``
   :dyn: No
   :scope: Global
   :vartype: Boolean
   :default: ``OFF``

The variable turns on binary and relay logs encryption.
