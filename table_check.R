library('swat')

conn <- CAS('pdcesx16144.exnet.sas.com', port=8777,
            # 'localhost',
            caslib = 'casuser', username = 'sasdemo01',
            password = 'Orion123', protocol = "http")

session_id <- cas.session.sessionId(conn)

tablenames <- c('hmeq', 
                'hmeqpr_1_1q', 'hmeqpr_2_2q',
                'hmeqpr_3_3q', 'hmeqpr_4_4q')

tables <- c()

for (i in tablenames){
tables[i] <-  cas.table.tableExists(conn, caslib= 'public',
                        name= i )$exists
}

exists <- tables %in% 2

if (all(exists)) {
  writeLines(session_id[[1]], 'session_id.txt')
  cas.close(conn)
  
  print(paste0('All tables exists in session with id:', session_id[[1]]))
  print(tables)

} else {
  writeLines(session_id[[1]], 'session_id.txt')
  cas.close(conn)
  
  print(tables)
  stop(paste0('Not all tables exists in session with id:', session_id[[1]]))
}




