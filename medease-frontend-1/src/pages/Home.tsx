import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css'; // Assuming you have a CSS file for styling

const Home: React.FC = () => {
    return (
        <div className="home-container">
            <header className="home-header">
                <h1>Welcome to MedEase</h1>
                <p>Your one-stop solution for healthcare management.</p>
            </header>
            <main className="home-main">
                <section className="home-features">
                    <h2>Features</h2>
                    <ul>
                        <li>
                            <Link to="/appointments">Schedule Appointments</Link>
                        </li>
                        <li>
                            <Link to="/inventory">Manage Inventory</Link>
                        </li>
                        <li>
                            <Link to="/orders">View Orders</Link>
                        </li>
                        <li>
                            <Link to="/customers">Manage Customers</Link>
                        </li>
                        <li>
                            <Link to="/dashboard">Dashboard Overview</Link>
                        </li>
                    </ul>
                </section>
            </main>
            <footer className="home-footer">
                <p>&copy; {new Date().getFullYear()} MedEase. All rights reserved.</p>
            </footer>
        </div>
    );
};

export default Home;