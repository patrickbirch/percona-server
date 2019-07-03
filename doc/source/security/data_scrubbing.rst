.. _data-scrubbing:

=============================================================
Data Scrubbing
=============================================================



:Availability: This feature is **experimental** quality

When a user deletes database data, only the data structure metadata is overwritten. The data is still available on the hard drive and may be found by compliance software audits.  Data scrubbing removes the *deleted* rows. The space claimed by this deleted data
is overwritten with new data at a later time.

Data scrubbing is designed to delete the data so the data cannot be recovered. Once enabled, data scrubbing works automatically on each tablespace
separately. To enable data scrubbing, you need to set the following variables:

- :variable:`innodb-background-scrub-data-uncompressed`
- :variable:`innodb-background-scrub-data-compressed`

Uncompressed tables can also be scrubbed immediately, independently of key
rotation or background threads. This setting can be enabled by setting the variable
:variable:`innodb-immediate-scrub-data-uncompressed`. This option is not supported for
compressed tables.

Note that data scrubbing is made effective by setting the
:variable:`innodb_online_encryption_threads` variable to a value greater than
**zero**.

System Variables
--------------------------------------------------------------------------------

.. variable:: innodb_background_scrub_data_compressed

   :cli: ``--innodb-background-scrub-data-compressed``
   :dyn: Yes
   :scope: Global
   :vartype: Boolean
   :default: ``OFF``

.. variable:: innodb_background_scrub_data_uncompressed

   :cli: ``--innodb-background-scrub-data-uncompressed``
   :dyn: Yes
   :scope: Global
   :vartype: Boolean
   :default: ``OFF``
