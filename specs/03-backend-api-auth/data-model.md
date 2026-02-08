# Data Model: Backend API, Database, Stateless Chat, and Authentication

## Entity: User
- **Description**: Represents authenticated users in the system
- **Fields**:
  - id (str): Unique user identifier from Better Auth (Primary Key)
  - created_at (datetime): Timestamp of user creation
  - updated_at (datetime): Timestamp of last update

## Entity: Conversation
- **Description**: Represents a unique conversation thread between user and AI assistant
- **Fields**:
  - id (int): Auto-incrementing primary key
  - user_id (str): Foreign key linking to User.id
  - created_at (datetime): Timestamp of conversation creation
  - updated_at (datetime): Timestamp of last activity
- **Relationships**:
  - One-to-many with Message (one Conversation to many Messages)
  - Many-to-one with User (many Conversations to one User)

## Entity: Message
- **Description**: Represents individual messages within a conversation
- **Fields**:
  - id (int): Auto-incrementing primary key
  - user_id (str): Foreign key linking to User.id
  - conversation_id (int): Foreign key linking to Conversation.id
  - role (str): Enum of 'user' or 'assistant' indicating message sender
  - content (str): Message content (text)
  - created_at (datetime): Timestamp of message creation
- **Relationships**:
  - Many-to-one with Conversation (many Messages to one Conversation)
  - Many-to-one with User (many Messages to one User)

## Database Indexes
- Conversation.user_id: Index for efficient user-based queries
- Conversation.created_at: Index for chronological ordering
- Message.conversation_id: Index for conversation-based queries
- Message.role: Index for role-based filtering
- Message.created_at: Index for chronological ordering

## Validation Rules
- User.id: Required, must match Better Auth user ID format
- Conversation.user_id: Required, must reference valid User.id
- Message.user_id: Required, must match authenticated user
- Message.conversation_id: Required, must reference valid Conversation.id
- Message.role: Required, must be either 'user' or 'assistant'
- Message.content: Required, maximum length 10,000 characters