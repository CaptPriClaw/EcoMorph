// src/views/waste-approval-view.js
import { LitElement, html, css } from 'lit';
import { state } from 'lit/decorators.js';
import { adminApi, wasteApi } from '../api/apiClient';

class WasteApprovalView extends LitElement {
  static styles = css`
    table { width: 100%; border-collapse: collapse; }
    th, td { padding: 0.8rem; text-align: left; border-bottom: 1px solid #ddd; }
    img { width: 40px; height: 40px; object-fit: cover; border-radius: 4px; }
    button { margin-right: 0.5rem; }
  `;

  @state()
  _pendingWastes = [];

  async connectedCallback() {
    super.connectedCallback();
    this._fetchPendingWastes();
  }

  async _fetchPendingWastes() {
    try {
      this._pendingWastes = await adminApi.getPendingWastes();
    } catch (error) { console.error('Failed to fetch:', error); }
  }

  async _handleAction(wasteId, status) {
    try {
      await wasteApi.updateStatus(wasteId, status);
      this._fetchPendingWastes();
    } catch (e) { alert(`Action failed: ${e.message}`) }
  }

  render() {
    return html`
      <h1>Waste Approval</h1>
      <table>
        <thead>
          <tr><th>Image</th><th>Material</th><th>Uploader ID</th><th>Actions</th></tr>
        </thead>
        <tbody>
          ${this._pendingWastes.map(item => html`
            <tr>
              <td><img src=${item.image_url} alt=${item.material_type} /></td>
              <td>${item.material_type}</td>
              <td>${item.uploader_id}</td>
              <td>
                <button @click=${() => this._handleAction(item.id, 'approved')}>Approve</button>
                <button @click=${() => this._handleAction(item.id, 'rejected')}>Reject</button>
              </td>
            </tr>
          `)}
        </tbody>
      </table>
    `;
  }
}
customElements.define('waste-approval-view', WasteApprovalView);