---
id: "001"
title: "Fix Frontend Redirect Issue After Login"
stage: "general"
date_iso: "2026-01-18"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "master"
user: "SS Computer"
command: "fix frontend redirect issue"
labels:
  - "authentication"
  - "routing"
  - "bug-fix"
  - "frontend"
links:
  SPEC: null
  TICKET: null
  ADR: null
  PR: null
files_yaml:
  - "frontend/src/services/ApiService.ts"
  - "frontend/src/hooks/useAuth.ts"
  - "frontend/src/pages/ChatPage.tsx"
tests_yaml: []
---

# Fix Frontend Redirect Issue After Login

## Problem Statement
The application was redirecting to `/login` after successful login, but `/login` doesn't exist as a route in the frontend router. The router is configured to handle `/` and `/chat/:userId` routes, but after login the app was incorrectly redirecting to a non-existent login route.

## Root Cause
The issue was in the API service's response interceptor that handled 401 unauthorized errors by redirecting to `/login`:

```javascript
if (!['/login'].includes(window.location.pathname)) {
  window.location.href = '/login';
}
```

This caused problems because:
1. There's no `/login` route defined in the frontend router
2. The ChatPage component handles authentication internally with its own login form
3. The redirect was happening regardless of the authentication state

## Solution Implemented

### 1. Fixed API Service Redirect Issue
**File**: `frontend/src/services/ApiService.ts`
- Replaced redirect to `/login` with a custom event dispatch
- Instead of `window.location.href = '/login';`, now uses `window.dispatchEvent(new CustomEvent('authExpired'));`

### 2. Updated Authentication Hook
**File**: `frontend/src/hooks/useAuth.ts`
- Added event listener for `authExpired` event
- When the event fires, it triggers the logout function to properly clean up authentication state

### 3. Enhanced Chat Page Navigation
**File**: `frontend/src/pages/ChatPage.tsx`
- Added `useNavigate` hook from react-router-dom
- Updated login function to navigate to user's chat route after successful authentication
- Added logout button with proper navigation to home route
- Updated forbidden access button to use navigate instead of direct href

## Technical Details

### Before Fix
```javascript
// API Service - Problematic redirect
if (error.response?.status === 401) {
  localStorage.removeItem('auth_token');
  if (!['/login'].includes(window.location.pathname)) {
    window.location.href = '/login';  // Redirects to non-existent route
  }
}
```

### After Fix
```javascript
// API Service - Custom event approach
if (error.response?.status === 401) {
  localStorage.removeItem('auth_token');
  window.dispatchEvent(new CustomEvent('authExpired'));  // Notify app about auth failure
}

// Auth Hook - Event listener
useEffect(() => {
  checkAuthStatus()

  const handleAuthExpired = () => {
    logout()  // Properly handle logout
  }

  window.addEventListener('authExpired', handleAuthExpired)

  return () => {
    window.removeEventListener('authExpired', handleAuthExpired)
  }
}, [])
```

## Outcome
- Authentication flow now works properly within the existing routing structure
- Successful login navigates to the appropriate chat interface (`/chat/:userId` or `/`)
- Authentication failures are handled gracefully without redirecting to non-existent routes
- Users have a logout button for better UX
- The application maintains its stateless authentication approach while fixing the redirect issue

## Files Modified
1. `frontend/src/services/ApiService.ts` - Fixed redirect logic
2. `frontend/src/hooks/useAuth.ts` - Added event listener for auth failures
3. `frontend/src/pages/ChatPage.tsx` - Enhanced navigation and added logout functionality

## Testing
The fix ensures that:
- After successful login, the user is navigated to their chat interface
- Authentication failures don't cause redirects to non-existent routes
- Logout functionality works properly with navigation
- The existing routing structure is maintained