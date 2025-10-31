'use client';

import React, { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { addTodo } from '@/lib/api'; // Correctly imports API logic

export default function AddTodoForm() {
  const [formData, setFormData] = useState({
    title: "",
    description: ""
  });
  
  // State for success and error messages
  const [successMessage, setSuccessMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  
  const queryClient = useQueryClient();

  const { mutate, isPending } = useMutation({
    mutationFn: addTodo, // Uses the imported function
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['todos'] });
      setFormData({ title: "", description: "" });
      
      // Set success message and clear any error
      setSuccessMessage("Todo added successfully!");
      setErrorMessage("");
      
      // Clear success message after 3 seconds
      setTimeout(() => setSuccessMessage(""), 3000);
    },
    onError: (error) => {
      console.error(error);
      
      // Set error message and clear any success
      setErrorMessage("Error adding todo. Please try again.");
      setSuccessMessage("");

      // Clear error message after 3 seconds
      setTimeout(() => setErrorMessage(""), 3000);
    },
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    // Clear messages as soon as the user starts typing again
    setSuccessMessage("");
    setErrorMessage("");
    
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    
    // Clear any existing messages on a new submission
    setSuccessMessage("");
    setErrorMessage("");
    
    if (!formData.title.trim()) {
      // Use the UI for validation errors, not alert
      setErrorMessage("Title is required.");
      return;
    }
    
    mutate({
      title: formData.title,
      description: formData.description,
    });
  };

  return (
    <form className="w-full max-w-lg mb-8" onSubmit={handleSubmit}>
      <div className="flex flex-col gap-4">
        <input
          type="text"
          name="title"
          placeholder="Enter todo title..."
          className="w-full p-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={formData.title}
          onChange={handleChange}
          disabled={isPending}
        />
        
        <textarea
          name="description"
          placeholder="Enter todo description (optional)..."
          rows={3}
          className="w-full p-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={formData.description}
          onChange={handleChange}
          disabled={isPending}
        />
        
        {/* Success Message Block */}
        {successMessage && (
          <div className="p-3 text-sm text-green-800 bg-green-100 border border-green-200 rounded-lg">
            {successMessage}
          </div>
        )}
        
        {/* Error Message Block */}
        {errorMessage && (
          <div className="p-3 text-sm text-red-800 bg-red-100 border border-red-200 rounded-lg">
            {errorMessage}
          </div>
        )}
        
        <button
          type="submit"
          className="w-full px-6 py-3 font-semibold text-white bg-blue-600 rounded-lg shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:bg-gray-400"
          disabled={isPending}
        >
          {isPending ? 'Adding...' : 'Add Todo'}
        </button>
      </div>
    </form>
  );
}
