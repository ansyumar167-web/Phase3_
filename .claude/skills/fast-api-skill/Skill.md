---
name: backend-routes
description: Build backend routes, handle requests/responses, and connect to a database. Use for REST APIs or server applications.
---

# Backend Routes & DB Connection

## Instructions

1. **Project setup**
   - Initialize project with Node.js / Python / relevant backend framework
   - Install required packages (Express, FastAPI, Flask, or similar)
   - Configure environment variables for DB connection

2. **Route creation**
   - Define GET, POST, PUT, DELETE routes
   - Use route parameters and query strings
   - Implement request validation and error handling

3. **Request/Response handling**
   - Parse JSON payloads
   - Send appropriate HTTP status codes
   - Handle errors gracefully and return meaningful messages

4. **Database connection**
   - Connect to SQL/NoSQL database (PostgreSQL, MongoDB, MySQL, etc.)
   - Perform CRUD operations (Create, Read, Update, Delete)
   - Use ORM/ODM if applicable (Sequelize, Prisma, Mongoose, SQLAlchemy)

## Best Practices
- Use proper HTTP methods for each action
- Validate and sanitize user input
- Use environment variables for sensitive data
- Keep code modular: separate routes, controllers, and DB logic
- Log errors for debugging and monitoring

## Example Structure (Node.js + Express)
```javascript
const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const { connectDB } = require('./db');

app.use(bodyParser.json());

// Connect to DB
connectDB();

// Routes
app.get('/items', async (req, res) => {
  try {
    const items = await db.getItems();
    res.status(200).json(items);
  } catch (error) {
    res.status(500).json({ message: 'Server error' });
  }
});

app.post('/items', async (req, res) => {
  try {
    const newItem = await db.createItem(req.body);
    res.status(201).json(newItem);
  } catch (error) {
    res.status(500).json({ message: 'Server error' });
  }
});

app.listen(3000, () => console.log('Server running on port 3000'));
