
import React, { useEffect, useState } from 'react'
import { createPortal } from 'react-dom';

interface ToastNotificationProps {
    id: string;
    message: string;
    type: 'success' | 'error' | 'info' | 'warning';
    duration?: number; // in milliseconds, default is 3000ms
    onClose: (id: string) => void;
}

const ToastNotification: React.FC<ToastNotificationProps> = ({ id, message, type, duration = 3000, onClose}) => {
    const [isVisible, setIsVisible] = useState(true);

    useEffect(() => {
        const timer = setTimeout(() => {
            setIsVisible(false);
            onClose(id);
        }, duration);       
        return () => clearTimeout(timer);
    }, [duration, id, onClose]);
    const bgColor = {
        success: 'bg-green-100 text-green-800',
        error: 'bg-red-100 text-red-800',
        info: 'bg-blue-100 text-blue-800',
        warning: 'bg-yellow-100 text-yellow-800',
    }[type];


    return (
        <div className={`fixed bottom-4 right-4 max-w-xs p-4 rounded-lg shadow-lg transition-opacity duration-300 ${isVisible ? 'opacity-100' : 'opacity-0'} ${bgColor}`}>
                {message}
        </div>
    );
};


interface ToastContainerProps {}


export const ToastContainer: React.FC<ToastContainerProps> = () => {
    const [toasts, setToasts] = useState<{ id: string; message: string; type: ToastNotificationProps['type']}[]>([]);

    // Optionally, remove addToast if not used elsewhere
    // const addToast = (message: string, type: ToastNotificationProps['type'] = 'info') => {
    //     const id = new Date().getTime().toString();
    //     setToasts((prev) => [...prev, { id, message, type }]);
    // };

    const removeToast = (id: string) => {
        setToasts(prev => prev.filter((toast) => toast.id !== id));
    };
    return  createPortal(
        <div className="fixed top-4 right-0 p-4 space-y-2 z-50">
            {toasts.map((toast) => (
                <ToastNotification
                    key={toast.id}
                    id={toast.id}
                    message={toast.message}
                    type={toast.type}
                    onClose={removeToast}
                />
            ))}
        </div>,
        document.body
    );
}