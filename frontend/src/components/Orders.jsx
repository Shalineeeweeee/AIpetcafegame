import React, { useState } from 'react';

export const OrdersSystem = ({ activeOrders, onOrderUpdate }) => {
  const generateNewOrder = () => {
    const newOrder = {
      id: Date.now(),
      items: ['Pizza', 'Salad'],
      reward: 50,
      timeLimit: 120 // seconds
    };

    onOrderUpdate([...activeOrders, newOrder]);
  };

  const completeOrder = (orderId) => {
    const completedOrder = activeOrders.find(order => order.id === orderId);
    
    // Remove order and potentially add rewards
    onOrderUpdate(activeOrders.filter(order => order.id !== orderId));
  };

  return (
    <div className="orders-system">
      <h3>Active Orders</h3>
      {activeOrders.map(order => (
        <div key={order.id} className="order">
          <p>Order: {order.items.join(', ')}</p>
          <p>Reward: {order.reward} coins</p>
          <button onClick={() => completeOrder(order.id)}>Complete Order</button>
        </div>
      ))}
      <button onClick={generateNewOrder}>Generate New Order</button>
    </div>
  );
};