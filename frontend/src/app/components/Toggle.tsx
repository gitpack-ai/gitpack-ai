import React, { useState } from 'react';
import fetchJson from '../lib/fetchJson';

interface ToggleProps {
  initialState: boolean;
  toggleUrl: string;
  onToggle?: (newState: boolean) => void;
}

const Toggle: React.FC<ToggleProps> = ({ initialState, toggleUrl, onToggle }) => {
  const [isEnabled, setIsEnabled] = useState(initialState);

  const handleToggle = async () => {
    try {
      const newState = !isEnabled;
      const response = await fetchJson<{ is_enabled: boolean }>(toggleUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ state: newState }),
      });
      setIsEnabled(response.is_enabled);
      if (onToggle) {
        onToggle(response.is_enabled);
      }
    } catch (error) {
      console.error('Error toggling state:', error);
      // Optionally, handle the error in the UI
    }
  };

  return (
    <button
      type="button"
      onClick={handleToggle}
      className={`${
        isEnabled ? 'bg-indigo-600' : 'bg-gray-200'
      } relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:ring-offset-2`}
    >
      <span className="sr-only">Toggle state</span>
      <span
        className={`${
          isEnabled ? 'translate-x-5' : 'translate-x-0'
        } pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out`}
      />
    </button>
  );
};

export default Toggle;
