// src/views/login-view.js
import { LitElement, html, css } from 'lit';
import { authApi } from '../api/apiClient';

class LoginView extends LitElement {
  static styles = css`
    :host {
      display: flex; flex-direction: column; align-items: center;
      justify-content: center; height: 100vh; background-color: #f7f7f7;
    }
    form {
      display: flex; flex-direction: column; gap: 1rem;
      padding: 2.5rem; border: 1px solid #ccc; border-radius: 8px;
      background-color: white; box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    input { padding: 0.8rem; border: 1px solid #ccc; border-radius: 4px; }
    button { padding: 0.8rem; background-color: #4CAF50; color: white; border: none; cursor: pointer; border-radius: 4px;}
  `;

  async _handleLogin(e) {
    e.preventDefault();
    const email = e.target.email.value;
    const password = e.target.password.value;
    try {
      const data = await authApi.login(email, password);
      localStorage.setItem('authToken', data.access_token);
      this.dispatchEvent(new CustomEvent('login-success', { bubbles: true, composed: true }));
    } catch (error) {
      alert(`Login Failed: ${error.message}`);
    }
  }

  render() {
    return html`
      <form @submit=${this._handleLogin}>
        <h2>Admin Login</h2>
        <input type="email" name="email" placeholder="Email" required />
        <input type="password" name="password" placeholder="Password" required />
        <button type="submit">Login</button>
      </form>
    `;
  }
}

customElements.define('login-view', LoginView);