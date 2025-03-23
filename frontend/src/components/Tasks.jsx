import React, { useEffect } from "react";

function Tasks({ tasksCompleted, setTasksCompleted, setLevel }) {
  useEffect(() => {
    if (tasksCompleted >= 3) {
      setLevel((prev) => prev + 1);
      setTasksCompleted(0); // Reset after level up
    }
  }, [tasksCompleted]);

  return (
    <div className="tasks-container">
      <p> Tasks Completed: {tasksCompleted}/3</p>
    </div>
  );
}

export default Tasks;
