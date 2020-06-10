library('swat')

### Connections
conn <- CAS(#'pdcesx06182.exnet.sas.com', port=8777, protocol = 'http',
            'localhost',
            caslib = 'casuser', username = 'sasdemo01',
            password = 'Orion123')


### Saving session
session_id <- cas.session.sessionId(conn)

### increasig session timeout to 1h
cas.sessionProp.setSessOpt(conn,
                           casLib="casuser", 
                           timeOut=3600)

### Table names for checking
tablenames <- c('hmeq', 
                'hmeqpr_1_1q', 'hmeqpr_2_2q',
                'hmeqpr_3_3q', 'hmeqpr_4_4q')

## check table existance
tables <- c()

for (i in tablenames){
tables[i] <-  cas.table.tableExists(conn, caslib= 'public',
                        name= i )$exists
}

exists <- tables %in% 2


## what to do if OK
if (all(exists)) {
  writeLines(session_id[[1]], 'session_id.txt')
  cas.close(conn)
  
  print(paste0('All tables exists in session with id:', session_id[[1]]))
  print(tables)

## what to do if fails
} else {
  writeLines(session_id[[1]], 'session_id.txt')
  cas.close(conn)
  
  print(tables)
  stop(paste0('Not all tables exists in session with id:', session_id[[1]]))
}




