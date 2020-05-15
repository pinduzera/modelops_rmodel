pipeline {
  agent any
    stages {
      stage('Check Data') {
        steps {
          sh 'Rscript --vanilla table_check.R'
            }
          }
      stage('Model Training') {
        steps {
          sh 'Rscript --vanilla model_training.R'
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