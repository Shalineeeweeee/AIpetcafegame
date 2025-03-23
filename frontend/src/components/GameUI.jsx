import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Coins, Clock, ChefHat } from "lucide-react";
import "./styles.css"; // Ensure to have a pixel-art style CSS file

export default function GameScreen() {
  const [coins, setCoins] = useState(100);
  const [level, setLevel] = useState(1);
  const [progress, setProgress] = useState(33);
  const [orders, setOrders] = useState([
    { id: 1, item: "Latte", time: 30 },
    { id: 2, item: "Croissant", time: 45 },
  ]);

  useEffect(() => {
    if (progress >= 100) {
      setLevel(level + 1);
      setProgress(0);
    }
  }, [progress, level]);

  return (
    <div className="game-container pixel-art bg-cafe-night">
      {/* Top Bar */}
      <div className="top-bar">
        <div className="info-box">
          <Coins className="icon" />
          <span>{coins}</span>
        </div>
        <div className="info-box">
          <ChefHat className="icon" />
          <span>Level {level}</span>
        </div>
        <div className="info-box">
          <Clock className="icon" />
          <span>Time Left: 60s</span>
        </div>
      </div>

      {/* Orders Section */}
      <div className="orders-panel">
        {orders.map((order) => (
          <div key={order.id} className="order-box">
            <span>{order.item}</span>
            <span className="order-time">{order.time}s</span>
          </div>
        ))}
      </div>

      {/* Cooking & Serving Station */}
      <div className="cooking-station">
        <div className="ingredients">
          <motion.div whileHover={{ scale: 1.1 }} className="ingredient">☕</motion.div>
          <motion.div whileHover={{ scale: 1.1 }} className="ingredient">🥐</motion.div>
          <motion.div whileHover={{ scale: 1.1 }} className="ingredient">🍰</motion.div>
        </div>
        <div className="cooking-area">
          <motion.div whileTap={{ scale: 0.9 }} className="cooking-slot">🔥</motion.div>
          <motion.div whileTap={{ scale: 0.9 }} className="cooking-slot">🔥</motion.div>
        </div>
        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          className="serve-btn"
        >
          Serve Order
        </motion.button>
      </div>
    </div>
  );
}
