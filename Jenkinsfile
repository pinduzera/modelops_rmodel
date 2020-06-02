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
        
    }
      post { 
        always {
            cleanWs deleteDirs: true, notFailBuild: true
            echo 'The job is done!'
        }
        success {
            echo 'Model is trained and deployed!'
        }
        failure {
            echo 'Something went badly wrong!'
        }
    }

}