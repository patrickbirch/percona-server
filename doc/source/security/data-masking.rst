.. _security/data-masking:

==================================================================
Data Masking
==================================================================

This feature is **Experimental** quality.

The Percona Data Masking plugin is a free and Open Source implmentation of the |MySQL|'s data masking plugin. Data Masking provides a set of functions to hide sensitive data with modified content.

The data masking functions are the following:

    * Mask_Inner - modifies the inner part of a string. The ends of the string are not masked.
    * Mask_Outer - modiers the ends of the string. The inner part is not masked.
    * Mask_PAN - modifies the Primary Account Number (PAN). The function replaces the string except the last four characters with 'X' characters.

.. seealso::

    |MySQL| Documentation
    https://dev.mysql.com/doc/refman/8.0/en/data-masking-reference.html
