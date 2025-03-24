import React, { useState, useEffect } from 'react';
import { CoinSystem } from './CoinSystem';
import { LevelSystem } from './LevelSystem';
import { TasksSystem } from './TasksSystem';
import { TimerSystem } from './TimerSystem';
import { KitchenSystem } from './KitchenSystem';
import { OrdersSystem } from './OrdersSystem';

const GameUI = () => {
  const [gameState, setGameState] = useState({
    coins: 0,
    level: 1,
    experience: 0,
    tasks: [],
    activeOrders: [],
    kitchenInventory: [],
    gameTime: 0
  });

  const [isGameActive, setIsGameActive] = useState(false);

  useEffect(() => {
    let gameLoop;
    if (isGameActive) {
      gameLoop = setInterval(() => {
        // Game loop logic
        updateGameState();
      }, 1000); // Update every second
    }
    return () => clearInterval(gameLoop);
  }, [isGameActive]);

  const updateGameState = () => {
    setGameState(prevState => ({
      ...prevState,
      gameTime: prevState.gameTime + 1,
      // Additional game state updates
    }));
  };

  const startGame = () => {
    setIsGameActive(true);
    initializeGameState();
  };

  const initializeGameState = () => {
    setGameState({
      coins: 100,
      level: 1,
      experience: 0,
      tasks: generateInitialTasks(),
      activeOrders: [],
      kitchenInventory: [],
      gameTime: 0
    });
  };

  const generateInitialTasks = () => {
    return [
      { id: 1, description: 'Complete first kitchen order', completed: false },
      { id: 2, description: 'Earn 500 coins', completed: false }
    ];
  };

  const handleTaskCompletion = (taskId) => {
    setGameState(prevState => ({
      ...prevState,
      tasks: prevState.tasks.map(task => 
        task.id === taskId ? { ...task, completed: true } : task
      ),
      experience: prevState.experience + 10
    }));
  };

  return (
    <div className="game-container">
      {!isGameActive ? (
        <div className="start-screen">
          <h1>Alpet Game</h1>
          <button onClick={startGame}>Start Game</button>
        </div>
      ) : (
        <div className="game-interface">
          <div className="game-header">
            <CoinSystem 
              coins={gameState.coins} 
              onCoinsUpdate={(newCoins) => setGameState(prev => ({...prev, coins: newCoins}))}
            />
            <LevelSystem 
              level={gameState.level} 
              experience={gameState.experience}
            />
          </div>
          
          <div className="game-main">
            <KitchenSystem 
              inventory={gameState.kitchenInventory}
              onInventoryUpdate={(newInventory) => setGameState(prev => ({...prev, kitchenInventory: newInventory}))}
            />
            <OrdersSystem 
              activeOrders={gameState.activeOrders}
              onOrderUpdate={(newOrders) => setGameState(prev => ({...prev, activeOrders: newOrders}))}
            />
            <TasksSystem 
              tasks={gameState.tasks}
              onTaskComplete={handleTaskCompletion}
            />
            <TimerSystem 
              gameTime={gameState.gameTime}
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default GameUI;
