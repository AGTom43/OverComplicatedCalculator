import React, { useEffect } from "react";

// Custom Dialog Components
interface DialogProps {
    open: boolean;
    onOpenChange: (open: boolean) => void;
    children: React.ReactNode;
}

export const Dialog: React.FC<DialogProps> = ({ open, onOpenChange, children }) => {
    if (!open) return null;

    // Handle escape key
    useEffect(() => {
        const handleEscape = (event: KeyboardEvent) => {
            if (event.key === 'Escape') {
                onOpenChange(false);
            }
        };
        
        document.addEventListener('keydown', handleEscape);
        return () => document.removeEventListener('keydown', handleEscape);
    }, [onOpenChange]);

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
            {/* Backdrop */}
            <div 
                className="fixed inset-0 bg-black/50 cursor-pointer" 
                onClick={() => onOpenChange(false)}
                aria-hidden="true"
            />
            {/* Modal content */}
            <div 
                className="relative bg-white rounded-lg shadow-lg max-w-md w-full mx-4"
                onClick={e => e.stopPropagation()} // Prevent clicks inside modal from closing it
            >
                {children}
            </div>
        </div>
    );
};

export const DialogContent: React.FC<{ children: React.ReactNode }> = ({ children }) => (
    <div className="p-6">{children}</div>
);

export const DialogHeader: React.FC<{ children: React.ReactNode }> = ({ children }) => (
    <div className="mb-4">{children}</div>
);

export const DialogTitle: React.FC<{ children: React.ReactNode }> = ({ children }) => (
    <h2 className="text-xl font-semibold">{children}</h2>
);

// Custom Button Component
interface ButtonProps {
    children: React.ReactNode;
    onClick: () => void;
    className?: string;
    variant?: 'ghost';
    size?: 'sm';
}

export const Button: React.FC<ButtonProps> = ({ 
    children, 
    onClick, 
    className = '' 
}) => (
    <button
        onClick={onClick}
        className={`px-3 py-1 rounded hover:bg-gray-200 transition-colors ${className}`}
    >
        {children}
    </button>
);