pipeline {
  agent any
    stages {
      stage('Check Data') {
        steps {
          sh 'script --vanilla table_check.R'
            }
          }
      stage('Stage 2') {
        steps {
              echo 'Hello World'
                }
          }    
        
    }

}