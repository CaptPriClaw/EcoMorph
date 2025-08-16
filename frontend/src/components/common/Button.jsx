// src/components/common/Button.jsx
import React from 'react';
import './Button.css';

/**
 * A reusable button component with consistent styling.
 * @param {object} props
 * @param {React.ReactNode} props.children - The content inside the button (text, icon, etc.).
 * @param {function} props.onClick - The function to call when the button is clicked.
 * @param {string} [props.variant='primary'] - The button style ('primary' or 'secondary').
 * @param {string} [props.type='button'] - The button type ('button', 'submit', 'reset').
 * @param {boolean} [props.disabled=false] - Whether the button is disabled.
 */
function Button({ children, onClick, variant = 'primary', type = 'button', disabled = false, ...props }) {
  // We construct the className string based on the variant prop
  const className = `btn btn-${variant}`;

  return (
    <button
      className={className}
      onClick={onClick}
      type={type}
      disabled={disabled}
      {...props} // Pass through any other props
    >
      {children}
    </button>
  );
}

export default Button;