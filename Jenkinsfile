pipeline {
    agent any
    options { timeout(time: 25, unit: 'MINUTES') }
    triggers { cron('H 06 * * *') }
    stages {
        stage('Find Misspelled Words on Website') {
            agent { docker { image 'python:3.9-alpine3.13' } }
            steps {
                cleanWs()
                checkout(
                        [
                                $class                           : 'GitSCM', branches: [[name: '*/master']],
                                doGenerateSubmoduleConfigurations: false,
                                extensions                       : [[$class: 'CloneOption', noTags: false, reference: '', shallow: true]],
                                submoduleCfg                     : [],
                                userRemoteConfigs                : [[credentialsId: 'do-git', url: 'git@bitbucket.org:daily-objects/do-spelling-hornet.git']]]
                )
                sh 'python main.py'
                upload_to_folder('content', 'misspelled_words.csv')
            }
        }
    }
}

def upload_to_folder(String folder_name, String file_name) {
    withCredentials([
            [
                    $class           : 'AmazonWebServicesCredentialsBinding',
                    credentialsId    : 'bot-reporter',
                    accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
            ]
    ]) {
        s3Upload acl: 'PublicRead',
                bucket: 'do-reporting',
                includePathPattern: file_name,
                path: "$folder_name/"
    }
}