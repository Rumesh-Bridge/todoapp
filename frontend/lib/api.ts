import { NewTodo, Todo } from "@/types";

export const API_URL = 'http://127.0.0.1:8000';

// --- CREATE ---
export const addTodo = async (newTodo: NewTodo) => {
  const response = await fetch(`${API_URL}/todos/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      ...newTodo,
      completed: false,
    }),
  });

  if (!response.ok) {
    throw new Error('Failed to create todo');
  }
  return response.json();
};

// --- READ ---
export const getTodos = async (): Promise<Todo[]> => {
  const response = await fetch(`${API_URL}/todos/`);
  if (!response.ok) {
    throw new Error('Failed to fetch todos');
  }
  return response.json();
};

// --- UPDATE ---
// We'll update the 'completed' status
export const updateTodo = async (todo: Todo) => {
  const response = await fetch(`${API_URL}/todos/${todo.id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      completed: todo.completed,
    }),
  });

  if (!response.ok) {
    throw new Error('Failed to update todo');
  }
  return response.json();
};

// --- DELETE ---
export const deleteTodo = async (id: string) => {
  const response = await fetch(`${API_URL}/todos/${id}`, {
    method: 'DELETE',
  });

  if (!response.ok) {
    throw new Error('Failed to delete todo');
  }
  // No content is returned on a successful delete
  return true;
};

