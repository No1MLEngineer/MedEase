import axios from 'axios';

const API_BASE_URL = 'https://api.medease.com'; // Replace with your actual API base URL

// User Authentication
export const login = async (email, password) => {
    const response = await axios.post(`${API_BASE_URL}/auth/login`, { email, password });
    return response.data;
};

export const register = async (userData) => {
    const response = await axios.post(`${API_BASE_URL}/auth/register`, userData);
    return response.data;
};

// Inventory Management
export const fetchInventory = async () => {
    const response = await axios.get(`${API_BASE_URL}/inventory`);
    return response.data;
};

export const addInventoryItem = async (item) => {
    const response = await axios.post(`${API_BASE_URL}/inventory`, item);
    return response.data;
};

export const updateInventoryItem = async (itemId, item) => {
    const response = await axios.put(`${API_BASE_URL}/inventory/${itemId}`, item);
    return response.data;
};

export const deleteInventoryItem = async (itemId) => {
    const response = await axios.delete(`${API_BASE_URL}/inventory/${itemId}`);
    return response.data;
};

// Appointment Scheduling
export const fetchAppointments = async () => {
    const response = await axios.get(`${API_BASE_URL}/appointments`);
    return response.data;
};

export const scheduleAppointment = async (appointmentData) => {
    const response = await axios.post(`${API_BASE_URL}/appointments`, appointmentData);
    return response.data;
};

// Orders Management
export const fetchOrders = async () => {
    const response = await axios.get(`${API_BASE_URL}/orders`);
    return response.data;
};

export const createOrder = async (orderData) => {
    const response = await axios.post(`${API_BASE_URL}/orders`, orderData);
    return response.data;
};

// Customer Management
export const fetchCustomers = async () => {
    const response = await axios.get(`${API_BASE_URL}/customers`);
    return response.data;
};

export const addCustomer = async (customerData) => {
    const response = await axios.post(`${API_BASE_URL}/customers`, customerData);
    return response.data;
};