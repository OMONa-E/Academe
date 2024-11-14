import React, { useEffect, useState } from 'react';
import { getAudits } from '../../services/auditService'

function CEODashboard() {
  const [auditLogs, setAuditLogs] = useState([]);

  useEffect(() => {
    const fetchAuditLogs = async () => {
      try {
        const data = await getAudits();
        setAuditLogs(data);
      } catch (error) {
        console.error("Error fetching audit logs:", error);
      }
    };
    fetchAuditLogs();
  }, []);

  return (
    <div>
      <h1>CEO Dashboard</h1>
      <h3>Audit Logs</h3>
      <ul>
      {auditLogs.map((log) => (
          <li key={log.id}>
            <strong>Action:</strong> {log.action_type} by {log.actor?.username || "Unknown"}
            <br />
            <strong>Timestamp:</strong> {new Date(log.timestamp).toLocaleString()}
            <br />
            <strong>Device:</strong> {log.device_info || "N/A"}
            <br />
            <strong>IP Address:</strong> {log.ip_address || "N/A"}
            <br />
            <strong>Last Active:</strong> {log.last_active ? new Date(log.last_active).toLocaleString() : "N/A"}
            <br />
            <strong>Login Timestamp:</strong> {log.login_timestamp ? new Date(log.login_timestamp).toLocaleString() : "N/A"}
            <br />
            <strong>Changes:</strong> {log.changes && Object.keys(log.changes).length > 0 ? (
              <pre>{JSON.stringify(log.changes, null, 2)}</pre>
            ) : (
              "No changes recorded"
            )}
          </li>
        ))}
      </ul>

      {/* TODO */}
      <p>View all active sessions, manage Employers and Employees.</p>
      {/* Render data relevant to the CEO */}
    </div>
  );
}

export default CEODashboard;
