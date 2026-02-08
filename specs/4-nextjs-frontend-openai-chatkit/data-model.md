# Data Model: Frontend — Next.js 16 + OpenAI ChatKit

## Frontend State Models

### User Authentication State
```typescript
interface User {
  id: string;
  email: string;
  username: string;
  created_at: Date;
  updated_at: Date;
}

interface AuthState {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  error: string | null;
}
```

### Chat Conversation State
```typescript
interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface ChatState {
  messages: Message[];
  conversationId: number | null;
  isLoading: boolean;
  error: string | null;
  user_id: string;
}
```

### Task Management State
```typescript
interface Task {
  id: number;
  user_id: string;
  title: string;
  description: string | null;
  completed: boolean;
  created_at: Date;
  updated_at: Date;
}

interface TaskAction {
  action: 'add' | 'update' | 'complete' | 'delete' | 'list';
  taskId?: number;
  title?: string;
  description?: string;
  completed?: boolean;
}
```

## API Request/Response Models

### Chat API Request
```typescript
interface ChatRequest {
  message: string;
  conversation_id?: number;
  user_id: string;
}
```

### Chat API Response
```typescript
interface ChatResponse {
  conversation_id: number;
  response: string;
  tool_calls: string[];
  status: 'success' | 'error';
}
```

### Error Response Model
```typescript
interface ErrorResponse {
  error: string;
  status: number;
  details?: string;
}
```

## Component State Models

### Chat Interface State
```typescript
interface ChatInterfaceState {
  inputValue: string;
  isProcessing: boolean;
  showError: boolean;
  errorMessage: string;
}
```

### Task Confirmation State
```typescript
interface TaskConfirmationState {
  showConfirmation: boolean;
  taskAction: TaskAction | null;
  confirmationMessage: string;
}
```

## Local Storage Models

### Conversation Persistence
```typescript
interface ConversationPersistence {
  conversationId: number | null;
  lastActive: Date;
  userId: string;
}
```

### User Session Persistence
```typescript
interface UserSession {
  userId: string;
  authToken: string;
  refreshToken: string;
  expiresAt: Date;
}
```

## Validation Rules

### Message Validation
- Content must be non-empty string
- Content length must be between 1 and 1000 characters
- Role must be either 'user' or 'assistant'
- Timestamp must be valid Date object

### Task Validation
- Title must be non-empty string (max 255 characters)
- Description is optional (max 1000 characters)
- Completed status defaults to false
- User ID must match authenticated user

### Chat Request Validation
- Message must be non-empty string
- Conversation ID must be positive integer if provided
- User ID must be present and valid