library('swat')
library('MASS')
library('pmml')

options(scipen=999)

session_id <- readLines('session_id.txt')

conn <- CAS(
  #'pdcesx06125.exnet.sas.com', port=8777, protocol = 'http',
  'localhost',
  caslib = 'casuser', username = 'sasdemo01',
  password = 'Orion123', session =Zsession_id)


ctbl <- defCasTable(conn, tablename = 'hmeq', 
                    caslib = 'public')
### download data
data <- to.data.frame(to.casDataFrame(ctbl))
data <- na.omit(data)
head(ctbl)
data <- as.data.frame(lapply(data,
                             FUN= function(x){
                               if (is.character(x)) as.factor(x) else {x}}
                             )
                       )
data$BAD <- as.factor(data$BAD)
data$BAD <- relevel(data$BAD , ref = "1")

model1 <- glm(formula = BAD ~ .,
          family = binomial(link = 'logit'),
          data = data,)
model1 <-  stepAIC(model1)

### model summary
summary(model1)

### odds ratio CI
round(exp(cbind(coef(model1), confint(model1))), 3)


### saving model as PMML
pmml_model <- pmml(model1, 
                   model_name = 'r_logistic'
                   )
saveXML(pmml_model, 'model.pmml')
pem <- readLines('model.pmml')

### editing PMML to 4.2 for SAS Model Manager Support
### Only works on models that were available on PMML 4.2
pem[2] <- gsub('4\\.4', '4.2', pem[2])
pem[2] <- gsub('4_4', '4_2', pem[2])
pem[2] <- gsub('4\\-4', '4\\-2', pem[2])

saveRDS(model1, 'rlogistic.rda', version =2)
writeLines(pem, 'model.pmml')
