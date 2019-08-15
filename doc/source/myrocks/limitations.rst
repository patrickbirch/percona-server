<h1 id="myrocks_limitations">MyRocks Limitations</h1>
<p>The MyRocks storage engine lacks the following features compared to InnoDB:</p>
<ul>
<li><a href="https://dev.mysql.com/doc/refman/8.0/en/innodb-online-ddl.html">Online DDL</a></li>
<li><a href="https://dev.mysql.com/doc/refman/8.0/en/partitioning-management-exchange.html">ALTER TABLE ... EXCHANGE PARTITION</a></li>
<li><a href="https://dev.mysql.com/doc/refman/8.0/en/savepoint.html">SAVEPOINT</a></li>
<li><a href="https://dev.mysql.com/doc/refman/8.0/en/innodb-transportable-tablespace-examples.html">Transportable tablespace</a></li>
<li><a href="https://dev.mysql.com/doc/refman/8.0/en/create-table-foreign-keys.html">Foreign keys</a></li>
<li><a href="https://dev.mysql.com/doc/refman/8.0/en/using-spatial-indexes.html">Spatial indexes</a></li>
<li><a href="https://dev.mysql.com/doc/refman/8.0/en/innodb-fulltext-index.html">Fulltext indexes</a></li>
<li><a href="https://dev.mysql.com/doc/refman/8.0/en/innodb-locking.html#innodb-gap-locks">Gap locks</a></li>
<li><a href="https://dev.mysql.com/doc/refman/8.0/en/group-replication.html">Group Replication</a></li>
<li><a href="https://mysqlserverteam.com/mysql-8-0-optimizing-small-partial-update-of-lob-in-innodb/">Partial Update of LOB in InnoDB</a></li>
</ul>
<p>You should also consider the following:</p>
<ul>
<li><p><code class="interpreted-text" role="file">*_bin</code> (e.g. <code>latin1_bin</code>) or binary collation should be used on <code>CHAR</code> and <code>VARCHAR</code> indexed columns. By default, MyRocks prevents creating indexes with non-binary collations (including <code>latin1</code>). You can optionally use it by setting <code class="interpreted-text" role="variable">rocksdb_strict_collation_exceptions</code> to <code>t1</code> (table names with regex format), but non-binary covering indexes other than <code>latin1</code> (excluding <code>german1</code>) still require a primary key lookup to return the <code>CHAR</code> or <code>VARCHAR</code> column.</p></li>
<li><p>Either <code>ORDER BY DESC</code> or <code>ORDER BY ASC</code> is slow. This is because of "Prefix Key Encoding" feature in RocksDB. See <a href="http://www.slideshare.net/matsunobu/myrocks-deep-dive/58">http://www.slideshare.net/matsunobu/myrocks-deep-dive/58</a> for details. By default, ascending scan is faster and descending scan is slower. If the "reverse column family" is configured, then descending scan will be faster and ascending scan will be slower. Note that InnoDB also imposes a cost when the index is scanned in the opposite order.</p></li>
<li><p>MyRocks does not support operating as either a master or a slave in any replication topology that is not exclusively row-based. Statement-based and mixed-format binary logging is not supported. For more information, see <a href="https://dev.mysql.com/doc/refman/8.0/en/replication-formats.html">Replication Formats</a>.</p></li>
<li><p>When converting from large MyISAM/InnoDB tables, either by using the <code>ALTER</code> or <code>INSERT INTO SELECT</code> statements it's recommended that you check the <code class="interpreted-text" role="ref">Data loading &lt;myrocks_data_loading&gt;</code> documentation and create MyRocks tables as below (in case the table is sufficiently big it will cause the server to consume all the memory and then be terminated by the OOM killer):</p>
<pre class="mysql"><code>SET session sql_log_bin=0;
SET session rocksdb_bulk_load=1;
ALTER TABLE large_myisam_table ENGINE=RocksDB;
SET session rocksdb_bulk_load=0;</code></pre>
<blockquote>
<div class="warning">
<div class="admonition-title">
<p>Warning</p>
</div>
<p>If you are loading large data without enabling <code class="interpreted-text" role="variable">rocksdb_bulk_load</code> or <code class="interpreted-text" role="variable">rocksdb_commit_in_the_middle</code>, please make sure transaction size is small enough. All modifications of the ongoing transactions are kept in memory.</p>
</div>
</blockquote></li>
<li><p>The<a href="https://dev.mysql.com/doc/refman/8.0/en/xa.html">XA protocol</a> support, which allows distributed transactions combining multiple separate transactional resources, is an experimental feature in MyRocks: the implementation is less tested, it may lack some functionality and be not as stable as in case of InnoDB.</p></li>
<li><p>With partitioned tables that use the or storage engine, the upgrade only works with native partitioning.</p>
<div class="seealso">
<dl>
<dt>Documentation: Preparing Your Installation for Upgrade</dt>
<dd><p><a href="https://dev.mysql.com/doc/refman/8.0/en/upgrade-prerequisites.html">https://dev.mysql.com/doc/refman/8.0/en/upgrade-prerequisites.html</a></p>
</dd>
</dl>
</div></li>
<li><p>8.0 and Unicode 9.0.0 standards have defined a change in the handling of binary collations. These collations are handled as NO PAD, trailing spaces are included in key comparisons. A binary collation comparison may result in two unique rows inserted and does not generate a`DUP_ENTRY` error. MyRocks key encoding and comparison does not account for this character set attribute.</p></li>
<li><p>8.0.16 does not support encryption for the MyRocks storage engine. At this time, during an <code>ALTER TABLE</code> operation, MyRocks mistakenly detects all InnoDB tables as encrypted. Therefore, any attempt to <code>ALTER</code> an InnoDB table to MyRocks fails.</p>
<p>As a workaround, we recommend a manual move of the table. The following steps are the same as the <code>ALTER TABLE ... ENGINE=...</code> process:</p>
<blockquote>
<ul>
<li>Use <code>SHOW CREATE TABLE ...</code> to return the InnoDB table definition.</li>
<li>With the table definition as the source, perform a <code>CREATE TABLE ... ENGINE=RocksDB</code>.</li>
<li>In the new table, use <code>INSERT INTO &lt;new table&gt; SELECT * FROM &lt;old table&gt;</code>.</li>
</ul>
</blockquote>
<div class="note">
<div class="admonition-title">
<p>Note</p>
</div>
<p>With MyRocks and with large tables, it is recommended to set the session variable <code>rocksdb_bulk_load=1</code> during the load to prevent running out of memory. This recommendation is because of the MyRocks large transaction limitation.</p>
</div>
<div class="seealso">
<p>MyRocks Data Loading <a href="https://www.percona.com/doc/percona-server/8.0/myrocks/data_loading.html">https://www.percona.com/doc/percona-server/8.0/myrocks/data_loading.html</a></p>
</div></li>
</ul>