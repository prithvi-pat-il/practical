#!/bin/bash

# Exit on any error
set -e

echo "🚀 Starting College Practical Helper..."

# Create instance directory if it doesn't exist
mkdir -p /app/instance

# Set proper permissions (if running as root, but we're using appuser)
# chown -R appuser:appuser /app/instance 2>/dev/null || true

# Initialize database
echo "📊 Initializing database..."
python -c "
from app import init_db
try:
    init_db()
    print('✅ Database initialized successfully!')
except Exception as e:
    print(f'❌ Database initialization failed: {e}')
    exit(1)
"

# Check if database was created
if [ -f "/app/instance/database.db" ]; then
    echo "✅ Database file exists at /app/instance/database.db"
else
    echo "❌ Database file not found!"
    exit 1
fi

echo "🌐 Starting Flask application..."

# Execute the main command
exec "$@"
