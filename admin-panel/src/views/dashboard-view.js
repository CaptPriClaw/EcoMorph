// src/views/dashboard-view.js
import { LitElement, html, css } from 'lit';
import { state } from 'lit/decorators.js';
import { adminApi } from '../api/apiClient';

class DashboardView extends LitElement {
  static styles = css`
    .stats-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }
    .stat-card { border: 1px solid #ddd; padding: 1.5rem; text-align: center; border-radius: 8px; }
    .stat-card h3 { margin: 0; font-size: 2.5rem; color: #4CAF50; }
  `;

  @state()
  _stats = { pendingWastes: 0, activeUsers: 0, productsSold: 0 };

  async connectedCallback() {
    super.connectedCallback();
    try {
      // this._stats = await adminApi.getDashboardStats();
    } catch (e) { console.error(e) }
  }

  render() {
    return html`
      <h1>Dashboard</h1>
      <div class="stats-grid">
        <div class="stat-card">
          <h3>${this._stats.pendingWastes}</h3>
          <p>Pending Approvals</p>
        </div>
        <div class="stat-card">
          <h3>${this._stats.activeUsers}</h3>
          <p>Active Users</p>
        </div>
        <div class="stat-card">
          <h3>${this._stats.productsSold}</h3>
          <p>Products Sold</p>
        </div>
      </div>
    `;
  }
}

customElements.define('dashboard-view', DashboardView);