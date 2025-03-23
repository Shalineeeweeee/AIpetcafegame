import React, { useEffect, useState } from "react";

function Orders({ onComplete }) {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    const interval = setInterval(() => {
      const newOrder = {
        id: Date.now(),
        item: ["Coffee", "Cake", "Sandwich"][Math.floor(Math.random() * 3)],
        timeLeft: 10, // 10s per order
      };
      setOrders((prev) => [...prev, newOrder]);
    }, 5000); // New order every 5s

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="orders-container">
      {orders.map((order) => (
        <div key={order.id} className="order">
          <p>{order.item}</p>
          <p>⏳ {order.timeLeft}s</p>
          <button onClick={() => onComplete(order.item)}>Serve</button>
        </div>
      ))}
    </div>
  );
}

export default Orders;
