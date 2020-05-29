## testing data

system('Rscript --vanilla scoreCode.R ./data/hmeq_score.csv ./data/score_test.csv')

## loading tested data
test_data <- read.csv('./data/score_test.csv')

checks <- c()
### checking number of columns

if (ncol(test_data) < 15){
  checks[1] <- 'notok'
  print("Missing columns in the output")
} else {
  checks[1] <- 'ok'
}

### checking outputs

if (any(!is.numeric(test_data$P_BAD0)) | any(!is.numeric(test_data$P_BAD1))){
  checks[2] <- 'notok'
  print('Output error, not a numberin the columns prediction')
} else {
  checks[2] <- 'ok'
}

print(head(test_data))


print(tail(test_data))

file.remove('./data/score_test.csv')


if(any(checks != 'ok')){
  stop('Validation error, check logs')
} else {
  print('Everything is good to go')
}
