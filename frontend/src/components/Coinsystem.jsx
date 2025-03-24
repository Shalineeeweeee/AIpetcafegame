import React from 'react';

export const CoinSystem = ({ coins, onCoinsUpdate }) => {
  const earnCoins = (amount) => {
    onCoinsUpdate(coins + amount);
  };

  const spendCoins = (amount) => {
    if (coins >= amount) {
      onCoinsUpdate(coins - amount);
      return true;
    }
    return false;
  };

  return (
    <div className="coin-system">
      <h3>Coins: {coins}</h3>
    </div>
  );
};
