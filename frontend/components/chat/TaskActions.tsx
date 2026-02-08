'use client';

import React from 'react';

interface TaskActionProps {
  action: string;
  taskTitle: string;
  onConfirm: () => void;
  onCancel: () => void;
  isPending?: boolean;
}

const TaskActions = ({ action, taskTitle, onConfirm, onCancel, isPending = false }: TaskActionProps) => {
  const actionMap: Record<string, string> = {
    add: 'Add',
    complete: 'Complete',
    delete: 'Delete',
    update: 'Update'
  };

  const actionText = actionMap[action] || action;

  return (
    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 my-2">
      <div className="text-sm text-blue-800 font-medium">
        {actionText} task: "{taskTitle}"?
      </div>
      <div className="flex gap-2 mt-2">
        <button
          onClick={onConfirm}
          disabled={isPending}
          className={`px-3 py-1.5 text-xs rounded-md ${
            isPending
              ? 'bg-blue-400 text-white cursor-not-allowed'
              : 'bg-blue-600 text-white hover:bg-blue-700 active:bg-blue-800'
          }`}
        >
          {isPending ? 'Confirming...' : 'Yes'}
        </button>
        <button
          onClick={onCancel}
          disabled={isPending}
          className="px-3 py-1.5 text-xs bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300 active:bg-gray-400"
        >
          No
        </button>
      </div>
    </div>
  );
};

interface TaskConfirmationProps {
  taskAction: {
    action: string;
    taskTitle: string;
    taskId?: number;
  };
  onConfirm: (taskId?: number) => void;
  onCancel: () => void;
  isPending?: boolean;
}

const TaskConfirmation = ({ taskAction, onConfirm, onCancel, isPending }: TaskConfirmationProps) => {
  const handleConfirm = () => {
    onConfirm(taskAction.taskId);
  };

  return (
    <TaskActions
      action={taskAction.action}
      taskTitle={taskAction.taskTitle}
      onConfirm={handleConfirm}
      onCancel={onCancel}
      isPending={isPending}
    />
  );
};

export { TaskActions, TaskConfirmation };