import React, { useEffect, useState } from 'react';
import { fetchOrders } from '../api'; // Assuming you have a function to fetch orders
import OrderList from '../components/Orders/OrderList';

const Orders: React.FC = () => {
    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const getOrders = async () => {
            try {
                const data = await fetchOrders();
                setOrders(data);
            } catch (err) {
                setError('Failed to fetch orders');
            } finally {
                setLoading(false);
            }
        };

        getOrders();
    }, []);

    if (loading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>{error}</div>;
    }

    return (
        <div>
            <h1>Order Management</h1>
            <OrderList orders={orders} />
        </div>
    );
};

export default Orders;