#!/bin/bash
# backup.sh - Script to backup PostgreSQL database

set -e

# Configuration
DB_HOST="postgres"
DB_NAME="demo_db"
DB_USER="demo"
DB_PASSWORD="demo123"
BACKUP_DIR="/opt/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="${BACKUP_DIR}/${DB_NAME}_${TIMESTAMP}.sql"

# Create backup directory if it doesn't exist
mkdir -p "${BACKUP_DIR}"

echo "Starting backup of ${DB_NAME} at $(date)"

# Perform the backup
export PGPASSWORD="${DB_PASSWORD}"
pg_dump -h "${DB_HOST}" -U "${DB_USER}" -d "${DB_NAME}" -f "${BACKUP_FILE}"

# Compress the backup file
gzip "${BACKUP_FILE}"
COMPRESSED_FILE="${BACKUP_FILE}.gz"

# Calculate backup size
BACKUP_SIZE=$(du -h "${COMPRESSED_FILE}" | awk '{print $1}')

# Log backup details to a JSON log file for dashboard visualization
echo "{\"timestamp\": \"$(date +"%Y-%m-%d %H:%M:%S")\", \"file\": \"$(basename ${COMPRESSED_FILE})\", \"size\": \"${BACKUP_SIZE}\", \"status\": \"success\"}" >> "${BACKUP_DIR}/backup_history.json"

echo "Backup completed successfully: ${COMPRESSED_FILE} (${BACKUP_SIZE})"
exit 0