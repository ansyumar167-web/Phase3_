---
name: auth-skill
description: Implement secure authentication with signup, signin, password hashing, JWT tokens, and improved auth integration. Use for backend systems requiring user management.
---

# Auth Skill – Signup, Signin, Password Hashing, JWT Tokens

## Instructions

1. **User Signup**
   - Collect essential user data: email, password, name
   - Hash passwords before storing in database (e.g., using bcrypt)
   - Validate email format and password strength
   - Return meaningful success/error messages

2. **User Signin**
   - Verify email exists in database
   - Compare hashed password with submitted password
   - Generate JWT token on successful login
   - Return token securely (e.g., httpOnly cookie or Authorization header)

3. **Password Hashing**
   - Use bcrypt or argon2 for secure hashing
   - Salt passwords to prevent rainbow table attacks
   - Avoid storing plain text passwords
   - Allow password reset via secure token link

4. **JWT Token Management**
   - Generate JWT with user ID and optional roles/permissions
   - Set token expiration (e.g., 1h for access, 7d for refresh)
   - Securely verify token on protected routes
   - Optionally implement refresh tokens for extended sessions

5. **Integration Tips**
   - Centralize auth logic in a service or middleware
   - Protect sensitive routes with token verification
   - Use environment variables for JWT secret keys
   - Log auth events for security monitoring

## Best Practices
- Never return passwords in API responses
- Use HTTPS to protect token transmission
- Implement rate limiting to prevent brute-force attacks
- Use standardized HTTP status codes (401, 403, 400)
- Keep auth logic DRY (Don't Repeat Yourself)

## Example Structure (Node.js + Express)
```javascript
import express from 'express';
import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';

const router = express.Router();
const users = []; // Example in-memory user store

// Signup route
router.post('/signup', async (req, res) => {
  const { email, password } = req.body;
  const hashedPassword = await bcrypt.hash(password, 10);
  users.push({ email, password: hashedPassword });
  res.status(201).json({ message: 'User created' });
});

// Signin route
router.post('/signin', async (req, res) => {
  const { email, password } = req.body;
  const user = users.find(u => u.email === email);
  if (!user) return res.status(401).json({ message: 'Invalid credentials' });

  const match = await bcrypt.compare(password, user.password);
  if (!match) return res.status(401).json({ message: 'Invalid credentials' });

  const token = jwt.sign({ email }, process.env.JWT_SECRET, { expiresIn: '1h' });
  res.json({ token });
});

// Protected route example
router.get('/profile', (req, res) => {
  const authHeader = req.headers.authorization;
  if (!authHeader) return res.status(401).json({ message: 'Unauthorized' });

  const token = authHeader.split(' ')[1];
  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET);
    res.json({ email: payload.email });
  } catch {
    res.status(401).json({ message: 'Invalid token' });
  }
});

export default router;
