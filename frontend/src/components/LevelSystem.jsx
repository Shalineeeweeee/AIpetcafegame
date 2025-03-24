import React, { useEffect } from 'react';

export const LevelSystem = ({ level, experience }) => {
  const EXPERIENCE_PER_LEVEL = 100;

  useEffect(() => {
    // Level up logic
    if (experience >= EXPERIENCE_PER_LEVEL * level) {
      // Level up mechanism would be implemented here
      console.log('Level up!');
    }
  }, [experience, level]);

  return (
    <div className="level-system">
      <h3>Level: {level}</h3>
      <progress value={experience % EXPERIENCE_PER_LEVEL} max={EXPERIENCE_PER_LEVEL}></progress>
    </div>
  );
};
