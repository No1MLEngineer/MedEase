import React from 'react';
import { Link } from 'react-router-dom';
import InventoryList from '../components/Inventory/InventoryList';
import AppointmentScheduler from '../components/Appointments/AppointmentScheduler';
import OrderList from '../components/Orders/OrderList';
import CustomerList from '../components/Customers/CustomerList';
import AgentSystem from '../components/MultiAIAgent/AgentSystem';

const Dashboard: React.FC = () => {
    return (
        <div className="dashboard">
            <h1>Dashboard</h1>
            <div className="dashboard-overview">
                <h2>Overview</h2>
                <Link to="/inventory">Manage Inventory</Link>
                <Link to="/appointments">Schedule Appointments</Link>
                <Link to="/orders">View Orders</Link>
                <Link to="/customers">Manage Customers</Link>
            </div>
            <div className="dashboard-components">
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