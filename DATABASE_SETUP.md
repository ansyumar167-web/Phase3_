# Neon PostgreSQL Database Setup

This document explains how to set up and configure the Neon PostgreSQL database for the Todo AI Agent application.

## Prerequisites

- Neon PostgreSQL account (sign up at [neon.tech](https://neon.tech))
- Created a project in Neon dashboard
- Have your connection details ready:
  - Host URL
  - Database name
  - Username
  - Password

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```bash
# Neon PostgreSQL Configuration
NEON_DB_HOST=ep-aged-snowflake-123456.us-east-1.aws.neon.tech
NEON_DB_NAME=todo_app
NEON_DB_USER=neondb_owner
NEON_DB_PASSWORD=your_password_here
NEON_DB_SSL_MODE=require

# Alternative: Direct connection string (if preferred)
DATABASE_URL=postgresql://neondb_owner:your_password@ep-aged-snowflake-123456.us-east-1.aws.neon.tech/todo_app?sslmode=require

# Application Settings
DEBUG=true
SECRET_KEY=your-super-secret-key-change-in-production
ENVIRONMENT=development
```

## Database Schema

The application creates the following tables:

### Tasks Table
- `id`: Primary key (auto-incrementing integer)
- `user_id`: String identifier for the user (indexed)
- `title`: Task title (varchar, max 255 chars)
- `description`: Optional task description (varchar, max 1000 chars)
- `completed`: Boolean indicating completion status (default: false)
- `created_at`: Timestamp when task was created
- `updated_at`: Timestamp when task was last updated

### Conversation Table
- `id`: Primary key (auto-incrementing integer)
- `user_id`: String identifier for the user (indexed)
- `created_at`: Timestamp when conversation was created
- `updated_at`: Timestamp when conversation was last updated

### Message Table
- `id`: Primary key (auto-incrementing integer)
- `user_id`: String identifier for the user (indexed)
- `conversation_id`: Foreign key referencing conversation (indexed)
- `role`: Message role (user or assistant)
- `content`: Message content (varchar, max 10000 chars)
- `created_at`: Timestamp when message was created

## Database Initialization

Run the following command to initialize the database:

```bash
python init_db.py
```

This will:
1. Create all required tables
2. Set up optimized indexes for Neon PostgreSQL
3. Initialize sample data for testing
4. Verify the database connection

## Connection Pooling for Neon Serverless

The application is configured with optimal connection settings for Neon's serverless architecture:

- **pool_size**: 5 (smaller pool for serverless efficiency)
- **max_overflow**: 10 (allow additional connections when needed)
- **pool_pre_ping**: True (verify connections before use)
- **pool_recycle**: 3600 seconds (recycle connections every hour)
- **pool_timeout**: 30 seconds (timeout for getting connections)
- **Statement timeout**: 30 seconds

These settings are optimized for Neon's serverless scaling behavior and connection management.

## Indexes

The following indexes are created automatically:

- `idx_tasks_user_id`: For efficient user-based task queries
- `idx_tasks_completed`: For filtering completed tasks
- `idx_tasks_user_completed`: Composite index for user and completion status
- `idx_conversation_user_id`: For user-based conversation queries
- `idx_message_user_id`: For user-based message queries
- `idx_message_conversation_id`: For conversation-based message queries
- `idx_*_created_at`: For chronological queries on all tables

## Migration Management

To run migrations manually:

```bash
cd backend
python -m src.database.migrate
```

## Testing the Connection

To verify your database connection is working:

```bash
python -c "from backend.src.database.neon_migration import verify_connection; verify_connection()"
```

## Production Considerations

- Use strong, unique secret keys
- Enable SSL mode in production
- Monitor connection usage
- Consider connection pool sizing based on your traffic
- Regular backups are handled by Neon automatically

## Troubleshooting

### Common Issues:

1. **Connection refused**: Verify your NEON_DB_HOST and network connectivity
2. **Authentication failed**: Check your NEON_DB_USER and NEON_DB_PASSWORD
3. **SSL Error**: Ensure NEON_DB_SSL_MODE is set to 'require'
4. **Permission denied**: Verify your database user has CREATE TABLE privileges

### Debug Mode:
Set `DEBUG=true` in your environment to enable SQL query logging.