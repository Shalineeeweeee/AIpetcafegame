import React from 'react';

export const TasksSystem = ({ tasks, onTaskComplete }) => {
  return (
    <div className="tasks-system">
      <h3>Tasks</h3>
      {tasks.map(task => (
        <div key={task.id} className={`task ${task.completed ? 'completed' : ''}`}>
          {task.description}
          {!task.completed && (
            <button onClick={() => onTaskComplete(task.id)}>Complete</button>
          )}
        </div>
      ))}
    </div>
  );
};
