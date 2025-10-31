// types.ts
export type Todo = {
    id: string;
    title: string;
    description?: string;
    completed: boolean;
  };
  

  export type NewTodo = {
    title: string;
    description?: string;
  };