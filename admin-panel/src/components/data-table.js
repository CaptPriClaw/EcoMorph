// src/components/data-table.js
import { LitElement, html, css } from 'lit';
import { property } from 'lit/decorators.js';

class DataTable extends LitElement {
  static styles = css`
    :host {
      display: block;
      font-family: var(--font-family, sans-serif);
    }
    table {
      width: 100%;
      border-collapse: collapse;
      box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    th, td {
      padding: 12px 15px;
      text-align: left;
      border-bottom: 1px solid var(--border-color, #ddd);
    }
    thead th {
      background-color: var(--light-gray, #f4f4f4);
      font-weight: 600;
      color: var(--text-color, #333);
    }
    tbody tr:hover {
      background-color: var(--light-gray, #f4f4f4);
    }
    .actions-cell ::slotted(button) {
        margin-right: 8px;
    }
  `;

  /**
   * Defines the table columns.
   * @type {Array<{key: string, label: string}>}
   * Example: [{ key: 'name', label: 'Full Name' }, { key: 'email', label: 'Email' }]
   */
  @property({ type: Array })
  headers = [];

  /**
   * The array of data objects to display in the table.
   * @type {Array<Object>}
   */
  @property({ type: Array })
  items = [];

  render() {
    return html`
      <table>
        <thead>
          <tr>
            ${this.headers.map(header => html`<th>${header.label}</th>`)}
          </tr>
        </thead>
        <tbody>
          ${this.items.map(item => html`
            <tr>
              ${this.headers.map(header => html`
                <td>${item[header.key]}</td>
              `)}
              <td class="actions-cell">
                  <slot name="actions" .item=${item}></slot>
              </td>
            </tr>
          `)}
        </tbody>
      </table>
    `;
  }
}

customElements.define('data-table', DataTable);