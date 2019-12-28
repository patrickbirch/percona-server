.. encryption-comparison:

===============================================================================
Comparing Encryption Methods
===============================================================================

You can use either of the encryption methods, but you cannot combine methods.

If you have enabled encryption with the Master key and
you then enable encryption with
background encryption threads, the tablespaces are re-encrypted with the keyring key.

.. note::

    While encryption threads are enabled, you cannot convert the tablespaces to
    Master key encryption. To convert the tablespaces, you must disable the
    encryption threads.

.. list-table::
    :widths: 15 10 10
    :header-rows: 1

    * - Task
      - Master key
      - Background Encryption Threads
    * - Encrypt existing tablespaces
      - Applied to all or some of the existing tablespaces
      - Applied by tablespace
    * - Key rotation for tablespaces
      - Each tablespace page is re-encrypted
      - Re-encrypts only the tablespace encryption header
