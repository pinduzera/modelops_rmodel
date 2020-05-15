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
           sh  'Rscript --vanilla model_training.R'
                }
          }    
        
    }
      post { 
        always { 
            echo 'It's trained!'
        }
    }

}