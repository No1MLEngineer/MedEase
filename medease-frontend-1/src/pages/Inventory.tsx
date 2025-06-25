import React, { useEffect, useState } from 'react';
import { fetchInventory } from '../api';
import InventoryList from '../components/Inventory/InventoryList';

const Inventory: React.FC = () => {
    const [inventory, setInventory] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const loadInventory = async () => {
            try {
                const data = await fetchInventory();
                setInventory(data);
            } catch (err) {
                setError('Failed to load inventory');
            } finally {
                setLoading(false);
            }
        };

        loadInventory();
    }, []);

    if (loading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>{error}</div>;
    }

    return (
        <div>
            <h1>Inventory Management</h1>
            <InventoryList inventory={inventory} />
        </div>
    );
};

export default Inventory;