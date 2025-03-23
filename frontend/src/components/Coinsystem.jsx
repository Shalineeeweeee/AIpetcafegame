import React from "react";

function CoinSystem({ coins }) {
  return (
    <div className="coin-container">
      <p> Coins: {coins}</p>
    </div>
  );
}

export default CoinSystem;
