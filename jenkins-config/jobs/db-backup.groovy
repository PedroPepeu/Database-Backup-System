// db-backup.groovy - Jenkins Job DSL for Database Backup Job
pipelineJob('scheduled-db-backup') {
    description('Scheduled PostgreSQL database backup job')
    
    // Define the job triggers
    triggers {
        // Run every day at 2 AM
        cron('0 2 * * *')
    }
    
    parameters {
        booleanParam('FORCE_CLEANUP', false, 'Force cleanup of old backups')
    }
    
    definition {
        cps {
            script('''
pipeline {
    agent any
    
    stages {
        stage('Prepare') {
            steps {
                echo "Starting database backup job at ${new Date()}"
                sh 'mkdir -p /opt/backups'
            }
        }
        
        stage('Backup Database') {
            steps {
                script {
                    try {
                        sh 'chmod +x /opt/scripts/backup.sh'
                        sh '/opt/scripts/backup.sh > backup_details.txt'
                        archiveArtifacts artifacts: 'backup_details.txt', fingerprint: true
                    } catch (Exception e) {
                        currentBuild.result = 'FAILURE'
                        error "Backup failed: ${e.message}"
                    }
                }
            }
        }
        
        stage('Cleanup Old Backups') {
            steps {
                script {
                    try {
                        sh 'chmod +x /opt/scripts/cleanup.sh'
                        sh '/opt/scripts/cleanup.sh >> backup_details.txt'
                    } catch (Exception e) {
                        echo "Warning: Cleanup failed: ${e.message}"
                        // Don't fail the build if just cleanup fails
                    }
                }
            }
        }
        
        stage('Generate Dashboard') {
            steps {
                script {
                    try {
                        sh 'chmod +x /opt/scripts/monitor.py'
                        sh 'python3 /opt/scripts/monitor.py >> backup_details.txt'
                        archiveArtifacts artifacts: '/opt/backups/reports/dashboard.html', fingerprint: true
                        publishHTML([
                            allowMissing: false,
                            alwaysLinkToLastBuild: true,
                            keepAll: true,
                            reportDir: '/opt/backups/reports',
                            reportFiles: 'dashboard.html',
                            reportName: 'Backup Dashboard'
                        ])
                    } catch (Exception e) {
                        echo "Warning: Dashboard generation failed: ${e.message}"
                        // Don't fail the build if just dashboard generation fails
                    }
                }
            }
        }
    }
    
    post {
        success {
            echo 'Backup completed successfully!'
            emailext(
                subject: 'Database Backup Success',
                body: '''
                    <h1>Database Backup Successful</h1>
                    <p>The scheduled database backup completed successfully.</p>
                    <p>See the attached details for more information.</p>
                    <p>Dashboard: ${BUILD_URL}Backup_Dashboard/</p>
                ''',
                attachmentsPattern: 'backup_details.txt',
                to: 'admin@example.com'
            )
        }
        failure {
            echo 'Backup failed!'
            emailext(
                subject: 'Database Backup Failure',
                body: '''
                    <h1>Database Backup Failed</h1>
                    <p>The scheduled database backup failed. Please check the logs.</p>
                    <p><a href="${BUILD_URL}console">Console Output</a></p>
                ''',
                to: 'admin@example.com'
            )
        }
        always {
            echo "Backup job completed at ${new Date()}"
        }
    }
}
            ''')
            sandbox()
        }
    }
}