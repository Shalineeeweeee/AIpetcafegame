import React from 'react';

export const TimerSystem = ({ gameTime }) => {
  const formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds < 10 ? '0' : ''}${remainingSeconds}`;
  };

  return (
    <div className="timer-system">
      <h3>Game Time: {formatTime(gameTime)}</h3>
    </div>
  );
};