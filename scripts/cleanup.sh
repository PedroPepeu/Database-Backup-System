#!/bin/bash
# cleanup.sh - Script to manage backup retention

set -e

# Configuration
BACKUP_DIR="/opt/backups"
RETENTION_DAYS=7  # Keep backups for 7 days

echo "Starting cleanup of old backups at $(date)"

# Find and delete backup files older than RETENTION_DAYS
find "${BACKUP_DIR}" -name "*.sql.gz" -type f -mtime +${RETENTION_DAYS} | while read -r old_backup; do
    echo "Removing old backup: ${old_backup}"
    rm "${old_backup}"
    
    # Log deletion to history file
    FILENAME=$(basename "${old_backup}")
    echo "{\"timestamp\": \"$(date +"%Y-%m-%d %H:%M:%S")\", \"file\": \"${FILENAME}\", \"action\": \"deleted\", \"reason\": \"retention policy\"}" >> "${BACKUP_DIR}/cleanup_history.json"
done

echo "Cleanup completed at $(date)"
exit 0