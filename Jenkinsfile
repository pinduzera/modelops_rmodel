pipeline {
  agent any
    stages {
      stage('Check Data') {
        steps {
          sh 'Rscript --vanilla table_check.R'
            }
          }
      stage('Stage 2') {
        steps {
              echo 'Hello World'
              echo 'Can you hear us?'
                }
          }    
        
    }

}