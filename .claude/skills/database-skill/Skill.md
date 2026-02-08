---
name: database-skill
description: Design and manage database schemas, create tables, and handle migrations. Use for backend development and data modeling.
---

# Database Skill – Tables, Migrations, and Schema Design

## Instructions

### 1. Schema Design
- Identify entities and relationships
- Define primary keys and foreign keys
- Normalize tables (1NF, 2NF, 3NF)
- Include indexes for frequently queried columns

### 2. Creating Tables
- Use `CREATE TABLE` statements
- Specify data types accurately (`INT`, `VARCHAR`, `DATE`, etc.)
- Add constraints: `NOT NULL`, `UNIQUE`, `CHECK`
- Include default values where applicable

### 3. Migrations
- Use a migration tool (e.g., Flyway, Sequelize, Alembic)
- Create versioned migration files
- Apply migrations consistently across environments
- Rollback migrations safely if needed

### 4. Relationships
- One-to-One, One-to-Many, Many-to-Many
- Define junction tables for Many-to-Many
- Set cascading rules (`ON DELETE CASCADE`, `ON UPDATE CASCADE`)

### 5. Data Integrity & Performance
- Use constraints and triggers to enforce rules
- Optimize queries with indexes
- Avoid redundant data
- Regularly review and refactor schema as needed

## Best Practices
- Name tables and columns clearly and consistently  
- Use singular nouns for table names (`user` instead of `users`)  
- Keep migrations atomic and reversible  
- Document schema changes  

## Example Structure

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Posts table
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Junction table for many-to-many
CREATE TABLE post_tags (
    post_id INT NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    tag_id INT NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY(post_id, tag_id)
);
