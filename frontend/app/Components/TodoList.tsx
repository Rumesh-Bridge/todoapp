'use client';

import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { getTodos } from '@/lib/api';
import TodoItem from './TodoItem'; // Import the new component

export default function TodoList() {
  // Use useQuery to fetch data
  const {
    data: todos,
    isLoading,
    isError,
  } = useQuery({
    queryKey: ['todos'], // This key is how TanStack Query caches the data
    queryFn: getTodos,  // This is the function it will call
  });

  // 1. Loading State
  if (isLoading) {
    return (
      <div className="w-full max-w-lg text-center">
        <p className="text-gray-500">Loading todos...</p>
      </div>
    );
  }

  // 2. Error State
  if (isError) {
    return (
      <div className="w-full max-w-lg p-4 text-red-800 bg-red-100 border border-red-200 rounded-lg">
        <p>Error fetching todos. Please try again later.</p>
      </div>
    );
  }

  // 3. Empty State
  if (!todos || todos.length === 0) {
    return (
      <div className="w-full max-w-lg text-center">
        <p className="text-gray-500">No todos yet. Add one above!</p>
      </div>
    );
  }

  // 4. Success State (Render the list)
  return (
    <div className="w-full max-w-lg space-y-4">
      {todos.map((todo) => (
        <TodoItem key={todo.id} todo={todo} />
      ))}
    </div>
  );
}
