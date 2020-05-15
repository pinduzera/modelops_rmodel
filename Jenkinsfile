pipeline {
  agent any
  environment {
  PATH = "/opt/anaconda3/bin/:$PATH"
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
      stage('Model Training') {
        steps {
          sh "Rscript --vanilla model_validation.R"
                }
          }        
        
    }
      post { 
        always { 
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