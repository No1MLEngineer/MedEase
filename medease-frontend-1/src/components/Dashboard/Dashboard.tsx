import React from 'react';
import { useAuth } from '../../hooks/useAuth';
import InventoryList from '../Inventory/InventoryList';
import AppointmentScheduler from '../Appointments/AppointmentScheduler';
import OrderList from '../Orders/OrderList';
import CustomerList from '../Customers/CustomerList';
import AgentSystem from '../MultiAIAgent/AgentSystem';

const Dashboard: React.FC = () => {
    const { user } = useAuth();

    return (
        <div className="dashboard">
            <h1>Welcome, {user?.name}</h1>
            <div className="dashboard-overview">
                <h2>Overview</h2>
                <InventoryList />
                <AppointmentScheduler />
                <OrderList />
                <CustomerList />
                <AgentSystem />
            </div>
        </div>
    );
};

export default Dashboard;