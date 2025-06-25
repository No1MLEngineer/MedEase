import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import MainLayout from '../layouts/MainLayout';
import Home from '../pages/Home';
import Login from '../pages/Login';
import Dashboard from '../pages/Dashboard';
import Inventory from '../pages/Inventory';
import Appointments from '../pages/Appointments';
import Orders from '../pages/Orders';
import Customers from '../pages/Customers';

const AppRoutes: React.FC = () => {
    return (
        <Router>
            <MainLayout>
                <Switch>
                    <Route path="/" exact component={Home} />
                    <Route path="/login" component={Login} />
                    <Route path="/dashboard" component={Dashboard} />
                    <Route path="/inventory" component={Inventory} />
                    <Route path="/appointments" component={Appointments} />
                    <Route path="/orders" component={Orders} />
                    <Route path="/customers" component={Customers} />
                </Switch>
            </MainLayout>
        </Router>
    );
};

export default AppRoutes;