import React, { useEffect, useState } from 'react';
import { getAssignedClients, getUpcomingSessions } from '../../services/employeeService';

function EmployeeDashboard() {
  const [clients, setClients] = useState([]);
  const [sessions, setSessions] = useState([]);

  useEffect(() => {
    const fetchEmployeeData = async () => {
      try {
        const clientData = await getAssignedClients();
        const sessionData = await getUpcomingSessions();
        setClients(clientData);
        setSessions(sessionData);
      } catch (error) {
        console.error("Error fetching employee data:", error);
      }
    };
    fetchEmployeeData();
  }, []);

  return (
    <div>
      <h1>Employee Dashboard</h1>
      <h3>Assigned Clients</h3>
      <ul>
        {clients.map((client) => (
          <li key={client.id}>{client.first_name} {client.last_name}</li>
        ))}
      </ul>
      <h3>Upcoming Sessions</h3>
      <ul>
        {sessions.map((session) => (
          <li key={session.id}>{session.module.title} on {new Date(session.session_date).toLocaleDateString()}</li>
        ))}
      </ul>
    </div>
  );
}

export default EmployeeDashboard;
