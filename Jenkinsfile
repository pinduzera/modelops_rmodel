pipeline {
  agent any
  environment {
  PATH = "/opt/anaconda3/bin/:$PATH"
  }
  
    options {
        timeout(time: 15, unit: 'MINUTES')   // timeout on whole pipeline job
    }

    stages {
      stage('Check Data') {
        steps {
          sh "Rscript --vanilla table_check.R"
            }
          }
      stage('Model Training') {
        steps {
          sh "Rscript --vanilla model_training.R"
                }
          }
      stage('Model Validation') {
        steps {
          sh "Rscript --vanilla model_validation.R"
                }
          }
      stage('Testing Score Code') {
        steps {
          sh "Rscript --vanilla scoreTesting.R"
                }
          }
      stage('Model Upload & publish') {
        steps {
          sh "python model_upload.py"

                }
          }
      stage('Testing Publication') {
        steps {
          sh "python test_pub.py"

                }
          }  
        
    }
      post {
        always {
            cleanWs deleteDirs: true, notFailBuild: true
            echo 'The job is done!'

            withCredentials([string(credentialsId: 'telegramToken', variable: 'TOKEN'),
                string(credentialsId: 'telegramChatId', variable: 'CHAT_ID')]){
            sh  '''curl -s -X POST https://api.telegram.org/bot"$TOKEN"/sendMessage -d chat_id="$CHAT_ID" -d text="Your build $JOB_NAME-$BUILD_NUMBER is finished" '''
                }
        }
        
        success {
            echo 'Model is trained and deployed!'
            
            withCredentials([string(credentialsId: 'telegramToken', variable: 'TOKEN'),
                string(credentialsId: 'telegramChatId', variable: 'CHAT_ID')]){
            sh  '''curl -s -X POST https://api.telegram.org/bot"$TOKEN"/sendMessage -d chat_id="$CHAT_ID" -d text="And It worked! :D" '''
                }
            }
        failure {
            echo 'Something went badly wrong!'
            
            withCredentials([string(credentialsId: 'telegramToken', variable: 'TOKEN'),
                string(credentialsId: 'telegramChatId', variable: 'CHAT_ID')]){
            sh  '''curl -s -X POST https://api.telegram.org/bot"$TOKEN"/sendMessage -d chat_id="$CHAT_ID" -d text="But it failed :(" '''
                }
                          }
            }

}