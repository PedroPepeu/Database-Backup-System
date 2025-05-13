# Jenkins Scheduled Database Backup System

This project demonstrates a complete database backup system using Jenkins and Docker. It includes:

- Automated PostgreSQL database backups
- Scheduled nightly backups via Jenkins
- Backup rotation with configurable retention
- Email notifications for success/failure
- Visual dashboard for backup history

## Requirements

- Docker and Docker Compose
- Internet connection to download images

## Setup Instructions

1. Clone this repository:

>git clone https://github.com/yourusername/jenkins-db-backup.git
>cd jenkins-db-backup

2. Update email settings in `jenkins-config/casc.yaml` file

3. Start the environment:

>docker-compose up -d

4. Access Jenkins at http://localhost:8080

5. Login with username `admin` and password `admin123`

6. The backup job will be automatically created and scheduled to run daily at 2 AM

## Manual Backup

To trigger a manual backup:

1. Go to Jenkins dashboard
2. Click on "scheduled-db-backup" job
3. Click "Build Now"

## Viewing the Dashboard

1. After at least one successful backup run, click on "scheduled-db-backup" job
2. Click "Backup Dashboard" in the left menu

## Customization

- Edit retention period in `scripts/cleanup.sh`
- Modify backup frequency by changing the cron schedule in `jenkins-config/jobs/db-backup.groovy`
- Add more visualization to the dashboard by updating `scripts/monitor.py`