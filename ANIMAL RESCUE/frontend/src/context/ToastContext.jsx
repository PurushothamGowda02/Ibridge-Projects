import React, { createContext, useContext, useState, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle, AlertCircle, X } from 'lucide-react';

const ToastContext = createContext();

export const ToastProvider = ({ children }) => {
    const [toasts, setToasts] = useState([]);

    const addToast = useCallback((message, type = 'success') => {
        const id = Math.random().toString(36).substr(2, 9);
        setToasts((prev) => [...prev, { id, message, type }]);
        setTimeout(() => removeToast(id), 5000);
    }, []);

    const removeToast = useCallback((id) => {
        setToasts((prev) => prev.filter((toast) => toast.id !== id));
    }, []);

    return (
        <ToastContext.Provider value={{ addToast }}>
            {children}
            <div style={{ position: 'fixed', bottom: '24px', right: '24px', zIndex: 9999, display: 'flex', flexDirection: 'column', gap: '12px' }}>
                <AnimatePresence>
                    {toasts.map((toast) => (
                        <motion.div
                            key={toast.id}
                            initial={{ opacity: 0, x: 50 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, scale: 0.95 }}
                            className="glass-morphism"
                            style={{ 
                                padding: '16px 24px', 
                                minWidth: '300px',
                                display: 'flex',
                                alignItems: 'center',
                                gap: '12px',
                                borderLeft: `4px solid ${toast.type === 'success' ? '#10b981' : '#ef4444'}`
                            }}
                        >
                            {toast.type === 'success' ? <CheckCircle color="#10b981" /> : <AlertCircle color="#ef4444" />}
                            <span style={{ flex: 1 }}>{toast.message}</span>
                            <button onClick={() => removeToast(toast.id)} style={{ background: 'none', border: 'none', color: 'var(--muted-text)', cursor: 'pointer' }}>
                                <X size={16} />
                            </button>
                        </motion.div>
                    ))}
                </AnimatePresence>
            </div>
        </ToastContext.Provider>
    );
};

export const useToast = () => useContext(ToastContext);
