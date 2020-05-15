library('swat')
library('ROCR')

session_id <- readLines('session_id.txt')

conn <- CAS(
  #'pdcesx16144.exnet.sas.com', port=8777, protocol = 'http',
  'localhost',
  caslib = 'casuser', username = 'sasdemo01',
  password = 'Orion123', session = session_id)


### new DATA
ctbl <- defCasTable(conn, tablename = 'hmeqpr_1_1q', 
                    caslib = 'public')

data <- to.data.frame(to.casDataFrame(ctbl))

data<-na.omit(data)

### Original predictions

ctbl2 <- defCasTable(conn, tablename = 'hmeq', 
                    caslib = 'public')

ctbl2 <- to.data.frame(to.casDataFrame(ctbl2))
data$BAD <- na.omit(ctbl2)$BAD

### read the Model, R can't read PMML easily
model <- readRDS('rlogistic.rda')


data$prediction <- predict(model, data2, type = 'response')

### performance

png('roc.png')

pred <- prediction(data$prediction, data$BAD)
perf <- performance(pred,"tpr","fpr")
plot(perf, main="ROC curve", colorize=T)

dev.off()

# lift chart
png('lift.png')

perf <- performance(pred,"lift","rpp")
plot(perf, main="lift curve", colorize=T)
dev.off()
