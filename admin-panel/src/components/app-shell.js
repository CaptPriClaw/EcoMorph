// src/components/app-shell.js
import { LitElement, html, css } from 'lit';

class AppShell extends LitElement {
  static styles = css`
    :host {
      display: flex;
      height: 100vh;
    }
    .sidebar {
      width: 220px;
      background: #f4f4f4;
      padding: 1rem;
      border-right: 1px solid #ddd;
    }
    .sidebar h2 {
      margin-top: 0;
    }
    .sidebar ul {
      list-style: none;
      padding: 0;
    }
    .sidebar li {
      padding: 0.5rem;
      cursor: pointer;
    }
    .sidebar li:hover {
      background: #e0e0e0;
    }
    .content {
      flex: 1;
      padding: 1rem;
      overflow-y: auto;
    }
  `;

  _handleNav(view) {
    this.dispatchEvent(new CustomEvent('navigate', { detail: view, bubbles: true, composed: true }));
  }

  render() {
    return html`
      <div class="sidebar">
        <h2>EcoMorph</h2>
        <ul>
          <li @click=${() => this._handleNav('dashboard')}>Dashboard</li>
          <li @click=${() => this._handleNav('waste-approval')}>Waste Approval</li>
          <li @click=${() => this._handleNav('users')}>User Management</li>
        </ul>
      </div>
      <div class="content">
        <slot></slot>
      </div>
    `;
  }
}

customElements.define('app-shell', AppShell);