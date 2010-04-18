#! coding: utf-8

#----- database -----
redis_host = 'localhost'
cache_db = 1
api_db = 5

#----- end database config ------

#----- cassandra settings ------
cassandra_cluster_name = 'MELS Cluster'
cassandra_keyspace = 'MELS'
cassandra_hosts = ['localhost:9160', ]

cassandra_super_column_family = ['Users', 'Dictionary'] 

cassandra_log_file               = '/home/Workspace/MELS/database/log/cassandra.log'
cassandra_commit_log_directory   = '/home/Workspace/MELS/database/raw_data/commitlog'
cassandra_data_file_directory    = '/home/Workspace/MELS/database/raw_data/data'

#----- redis setting -----
redis_backup_filename = 'redis_dump'
redis_backup_dir = '/home/Workspace/MELS/database/raw_data'

#----- data directory -----
files_dir   = '/home/Workspace/MELS/database'
data_folder = '/home/Workspace/MELS/database/contents'
audio_url_prefix = '/database'
#----- end data directory config -----

#----- user settings -----
trial_time = 15 # days
#----- end user settings -----

#----- serve ports -----
api_ports = [9000, 9001, 9002, 9003, 9004, 9005]
#----- end serve config -----