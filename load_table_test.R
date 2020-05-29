library('swat')

### Connections
conn <- CAS(#'pdcesx16144.exnet.sas.com', port=8777, protocol = 'http',
  'pdcesx05173.exnet.sas.com', port=8777, protocol = 'http',
  caslib = 'Public', username = 'sasdemo',
  password = 'Orion123')

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
