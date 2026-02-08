---
id: 1
title: Fix-demo-user-id-issue
stage: general
date_iso: 2026-01-18
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: user
command: "fix demo user id issue"
labels: ["bug", "authentication", "security"]
spec: null
ticket: null
adr: null
pr: null
---

# Fix demo user id issue

## User Prompt

Please fix the issue where after login, the application tries to load conversation history for 'demo_user_1' instead of the actual logged-in user. The error shows:

`GET http://localhost:8000/api/demo_user_1/conversations 401 (Unauthorized)`
`Error loading conversation history: Error: Invalid or expired token`

The issue is that the conversation history is being loaded with a hardcoded user ID 'demo_user_1' instead of using the actual user ID from the authentication context. The useChat hook at line 23 is calling loadConversationHistory which is trying to access the conversations endpoint with the wrong user ID. Please fix the useChat hook and related API calls to use the correct authenticated user ID.

## Assistant Response

Fixed the issue where the application was attempting to load conversation history for 'demo_user_1' instead of the actual authenticated user. Implemented comprehensive validation at multiple levels:

1. Updated the useChat hook to validate userId before making API calls, preventing requests with demo/test user IDs
2. Enhanced ChatInterface to validate and sanitize userId prop before passing to useChat hook
3. Modified ChatPage to detect and handle demo/test user IDs appropriately with user feedback
4. Strengthened authService to validate user IDs during login and token parsing, automatically clearing invalid tokens
5. Added proper error handling and user notifications for invalid session states

The fix ensures that only legitimate authenticated user IDs are used for API calls, preventing unauthorized access attempts with demo user IDs while providing clear feedback to users when their session is invalid.

## Files Modified

 - C:\Users\SS Computer\Desktop\hackhathon_2\frontend\src\hooks\useChat.ts
 - C:\Users\SS Computer\Desktop\hackhathon_2\frontend\src\components\ChatInterface.tsx
 - C:\Users\SS Computer\Desktop\hackhathon_2\frontend\src\pages\ChatPage.tsx
 - C:\Users\SS Computer\Desktop\hackhathon_2\frontend\src\services\authService.ts

## Outcome

The application now properly validates user authentication state and prevents API calls with demo/test user IDs. Users receive appropriate feedback when their session is invalid, and the system maintains security by rejecting unauthorized access attempts.