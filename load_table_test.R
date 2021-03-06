library('swat')

### Connections
conn <- CAS(#'hostname.com', port=8777, protocol = 'http',
  'hostname.com', port=8777, protocol = 'http',
  caslib = 'Public', username = 'username',
  password = 's3cr3t!')

tablenames <- c('hmeq', 
                'hmeqpr_1_1q', 'hmeqpr_2_2q',
                'hmeqpr_3_3q', 'hmeqpr_4_4q')

for (i in tablenames){
  cas.table.loadTable(conn, 
                      path=paste0("public/",i, ".sashdat"),
                      caslib = 'public',
                      casOut=list(name='public', replace=TRUE))
  cas.table.tableInfo(conn, table=i)
}
