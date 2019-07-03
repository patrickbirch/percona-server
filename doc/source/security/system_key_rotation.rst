.. _system_key_rotation:

==============================================================
System Key Rotation
==============================================================

System encryption keys can be rotated. A new version of a key is generated.

The PS 5.7 and < 8.0.14 the following is encrypted:

* percona_binlog
* percona_innodb
* percona_redo

From PS 5.7 and >= 8.0.14

* percona_innodb

Key versioning

Appends the version to the key_id in keyring

Percona_binlog:1 (starts with version 1)

`Select rotate_system_key("percona_binlog");`
percona_binlog:2 (version 2)
