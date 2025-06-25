export const validateEmail = (email: string): boolean => {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
};

export const validatePassword = (password: string): boolean => {
    return password.length >= 6;
};

export const formatDate = (date: Date): string => {
    return date.toLocaleDateString('en-US');
};

export const calculateInventoryValue = (inventory: { price: number; quantity: number }[]): number => {
    return inventory.reduce((total, item) => total + item.price * item.quantity, 0);
};

export const debounce = (func: Function, delay: number) => {
    let timeoutId: NodeJS.Timeout;
    return (...args: any[]) => {
        if (timeoutId) {
            clearTimeout(timeoutId);
        }
        timeoutId = setTimeout(() => {
            func(...args);
        }, delay);
    };
};