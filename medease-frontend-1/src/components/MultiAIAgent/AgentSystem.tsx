import React, { useEffect, useState } from 'react';

const AgentSystem: React.FC = () => {
    const [agents, setAgents] = useState<any[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchAgents = async () => {
            try {
                const response = await fetch('/api/agents'); // Replace with your API endpoint
                if (!response.ok) {
                    throw new Error('Failed to fetch agents');
                }
                const data = await response.json();
                setAgents(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchAgents();
    }, []);

    if (loading) {
        return <div>Loading agents...</div>;
    }

    if (error) {
        return <div>Error: {error}</div>;
    }

    return (
        <div>
            <h2>Multi AI Agent System</h2>
            <ul>
                {agents.map((agent) => (
                    <li key={agent.id}>
                        <h3>{agent.name}</h3>
                        <p>{agent.description}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default AgentSystem;