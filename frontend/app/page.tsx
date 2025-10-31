// import Image from "next/image";

import AddTodoForm from "./Components/AddTodoForm";
import TodoList from "./Components/TodoList";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center p-24">
      <h1 className="text-4xl font-bold mb-8">Todo App</h1>
      
        <AddTodoForm />
      
        <TodoList />
    </main>
  );
}