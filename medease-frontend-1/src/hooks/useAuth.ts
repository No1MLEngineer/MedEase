import { useContext, useState } from 'react';
import { AuthContext } from '../contexts/AuthContext';

const useAuth = () => {
    const { login, register, logout } = useContext(AuthContext);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleLogin = async (email, password) => {
        setLoading(true);
        setError(null);
        try {
            await login(email, password);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleRegister = async (email, password) => {
        setLoading(true);
        setError(null);
        try {
            await register(email, password);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleLogout = async () => {
        setLoading(true);
        setError(null);
        try {
            await logout();
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return {
        handleLogin,
        handleRegister,
        handleLogout,
        error,
        loading,
    };
};

export default useAuth;