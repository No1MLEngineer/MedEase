export interface User {
  id: string;
  username: string;
  email: string;
  role: 'admin' | 'user';
}

export interface Appointment {
  id: string;
  userId: string;
  date: string;
  time: string;
  reason: string;
}

export interface InventoryItem {
  id: string;
  name: string;
  quantity: number;
  price: number;
}

export interface Order {
  id: string;
  customerId: string;
  items: InventoryItem[];
  totalAmount: number;
  orderDate: string;
}

export interface Customer {
  id: string;
  name: string;
  email: string;
  phone: string;
  address: string;
}