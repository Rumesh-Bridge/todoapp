'use client';

import React from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { Todo } from '@/types';
import { updateTodo, deleteTodo } from '@/lib/api';

// This component receives a single todo as a prop
export default function TodoItem({ todo }: { todo: Todo }) {
  const queryClient = useQueryClient();

  // Mutation for updating the todo's 'completed' status
  const updateMutation = useMutation({
    mutationFn: () => updateTodo({ ...todo, completed: !todo.completed }),
    onSuccess: () => {
      // When successful, refetch the todo list
      queryClient.invalidateQueries({ queryKey: ['todos'] });
    },
  });

  // Mutation for deleting the todo
  const deleteMutation = useMutation({
    mutationFn: () => deleteTodo(todo.id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['todos'] });
    },
  });

  return (
    <div className="flex items-center justify-between p-4 bg-white border border-gray-200 rounded-lg shadow-sm">
      <div className="flex items-center gap-3">
        {/* Checkbox */}
        <input
          type="checkbox"
          className="w-5 h-5 text-blue-600 rounded"
          checked={todo.completed}
          onChange={() => updateMutation.mutate()}
        />
        <div>
          {/* Title - with strikethrough if completed */}
          <h2
            className={`text-lg font-medium ${
              todo.completed ? 'line-through text-gray-400' : 'text-gray-900'
            }`}
          >
            {todo.title}
          </h2>
          {/* Description - only show if it exists */}
          {todo.description && (
            <p
              className={`text-sm ${
                todo.completed ? 'line-through text-gray-400' : 'text-gray-600'
              }`}
            >
              {todo.description}
            </p>
          )}
        </div>
      </div>
      {/* Delete Button */}
      <button
        onClick={() => deleteMutation.mutate()}
        disabled={deleteMutation.isPending}
        className="px-3 py-1 text-sm font-medium text-red-600 bg-red-100 rounded-md hover:bg-red-200 disabled:opacity-50"
      >
        {deleteMutation.isPending ? '...' : 'Delete'}
      </button>
    </div>
  );
}
