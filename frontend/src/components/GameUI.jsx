import { useState, useEffect } from "react";

function GameUI() {
    const [orders, setOrders] = useState([]);
    const [coins, setCoins] = useState(0);
    const [level, setLevel] = useState(1);
    const [tasksCompleted, setTasksCompleted] = useState(0);

    // Generate new customer orders
    useEffect(() => {
        const generateOrder = () => {
            const newOrder = {
                id: Date.now(),
                item: ["Coffee", "Cake", "Sandwich"][Math.floor(Math.random() * 3)],
                timeLeft: 10, // 10s timer per order
            };
            setOrders((prev) => [...prev, newOrder]);
        };

        const interval = setInterval(generateOrder, 5000); // New order every 5 seconds
        return () => clearInterval(interval);
    }, []);

    // Handle completing an order
    const completeOrder = (orderId) => {
        setOrders((prev) => prev.filter((order) => order.id !== orderId));
        setCoins((prev) => prev + 10); // Reward coins
        setTasksCompleted((prev) => prev + 1);

        if ((tasksCompleted + 1) % 3 === 0) {
            setLevel((prev) => prev + 1); // Level up every 3 tasks
        }
    };

    return (
        <div className="bg-gray-900 text-white h-screen p-6">
            <h1 className="text-3xl font-bold">Pet Café Game</h1>
            <p>Coins: {coins} | Level: {level}</p>

            <div className="mt-4 grid grid-cols-3 gap-4">
                {orders.map((order) => (
                    <div key={order.id} className="p-4 bg-gray-700 rounded-lg">
                        <p>{order.item}</p>
                        <button onClick={() => completeOrder(order.id)} className="bg-green-500 p-2 mt-2">
                            Serve
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default GameUI;
