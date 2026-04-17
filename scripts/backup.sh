#!/usr/bin/env bash
set -euo pipefail

timestamp="$(date +%Y%m%d_%H%M%S)"
backup_dir="${1:-./backups}"
mkdir -p "$backup_dir"

docker compose exec -T db pg_dump -U "${DB_USER:-postgres}" "${DB_NAME:-queue_mgmt}" > "${backup_dir}/queue_backup_${timestamp}.sql"
echo "Backup saved to ${backup_dir}/queue_backup_${timestamp}.sql"
