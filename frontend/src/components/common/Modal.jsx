// src/components/common/Modal.jsx
import React from 'react';
import ReactDOM from 'react-dom';
import './Modal.css';

/**
 * A reusable Modal component that renders its content in a portal.
 * @param {object} props
 * @param {boolean} props.isOpen - Controls if the modal is visible.
 * @param {function} props.onClose - Function to call when the modal should be closed.
 * @param {string} [props.title] - The title displayed at the top of the modal.
 * @param {React.ReactNode} props.children - The content to display inside the modal.
 */
function Modal({ isOpen, onClose, title, children }) {
  if (!isOpen) {
    return null; // Don't render anything if the modal is not open
  }

  // We use ReactDOM.createPortal to render the modal's JSX
  // into a specific DOM node outside of the main React component tree.
  return ReactDOM.createPortal(
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          {title && <h2 className="modal-title">{title}</h2>}
          <button className="modal-close-btn" onClick={onClose}>
            &times;
          </button>
        </div>
        <div className="modal-body">
          {children}
        </div>
      </div>
    </div>,
    document.getElementById('modal-root') // The target DOM node in index.html
  );
}

export default Modal;