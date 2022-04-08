# Does not work yet

#!/bin/sh
echo 'running'
if [ -z "hadoop fs -ls /data" ]; then
    echo '/data is hdfs was empty, filling up'
    ./load_data_to_hdfs.sh
else
    echo '/data is hdfs was NOT empty'

./drop_raw.sql
./set_up_hiveDB.sql
./data_to_table.sql

echo 'DONE'

fi