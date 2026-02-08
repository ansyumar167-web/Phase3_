---
name: openai-chatkit-ui
description: Design and implement interactive UI and frontend components using OpenAI ChatKit for real-time AI chat applications.
---

# OpenAI ChatKit UI Design

## Instructions

1. **Layout structure**
   - Full viewport height for chat pages
   - Flex or grid-based layouts for chat & task components
   - Header, message list, and input box clearly separated
   - Modular sections for reuse across pages (chat windows, task cards, dashboards)

2. **Chat components**
   - Use `ChatProvider`, `Channel`, `ChatMessage`, and `ChatInput` from OpenAI ChatKit
   - Support real-time message updates
   - Include interactive elements: buttons, toggles, task creation inputs

3. **Styling & animations**
   - Utility-first CSS (Tailwind) or CSS-in-JS for consistent styling
   - Smooth hover, focus, and entry animations
   - Consistent color palette, typography, and spacing
   - Mobile-first and responsive design

4. **Best practices**
   - Components should be reusable and composable
   - Minimize DOM re-renders for performance
   - Accessibility: ARIA roles for interactive components
   - Clear separation of logic, layout, and style
   - Handle loading, error, and empty states gracefully

## Example Structure
```tsx
import { ChatProvider, Channel, ChatMessage, ChatInput } from '@openai/chatkit-react';

export function TodoChatPage() {
  return (
    <div className="flex flex-col h-screen border rounded-xl">
      <header className="p-4 border-b text-lg font-bold">AI Todo Chat</header>
      <ChatProvider apiKey={process.env.NEXT_PUBLIC_OPENAI_API_KEY} userId="user123">
        <Channel channelId="general" className="flex-1 flex flex-col">
          <div className="flex-1 overflow-y-auto p-4">
            <ChatMessage />
          </div>
          <ChatInput placeholder="Add a task or ask AI..." className="p-2 border-t" />
        </Channel>
      </ChatProvider>
    </div>
  );
}
