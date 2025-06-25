import React, { useEffect, useState } from 'react';
import { fetchInventory, deleteItem } from '../../api';
import { InventoryItem } from '../../types';
import './InventoryList.css';

const InventoryList: React.FC = () => {
    const [inventory, setInventory] = useState<InventoryItem[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
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

    const handleDelete = async (id: string) => {
        try {
            await deleteItem(id);
            setInventory(inventory.filter(item => item.id !== id));
        } catch (err) {
            setError('Failed to delete item');
        }
    };

    if (loading) return <div>Loading...</div>;
    if (error) return <div>{error}</div>;

    return (
        <div className="inventory-list">
            <h2>Inventory List</h2>
            <table>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Quantity</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {inventory.map(item => (
                        <tr key={item.id}>
                            <td>{item.name}</td>
                            <td>{item.quantity}</td>
                            <td>
                                <button onClick={() => handleDelete(item.id)}>Delete</button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default InventoryList;