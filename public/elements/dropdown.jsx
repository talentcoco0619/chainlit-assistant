import { useState } from 'react';

export default function SimpleToggleContent() {
  const [isContentVisible, setIsContentVisible] = useState(false);

  const toggleContent = () => {
    setIsContentVisible(!isContentVisible);
  };

  return (
    <div>
      <button onClick={toggleContent}>
        Toggle Content
      </button>
      {isContentVisible && (
        <div style={{ marginTop: '10px' }}>
          <p>This is the content displayed below the button.</p>
        </div>
      )}
    </div>
  );
}