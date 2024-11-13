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
            {log.action_type} by {log.actor} on {new Date(log.timestamp).toLocaleString()} using
            {log.device_info} located at {log.ip_address}, last active at {log.last_active}
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
