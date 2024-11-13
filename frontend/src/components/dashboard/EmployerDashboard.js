import React, { useEffect, useState } from 'react';
import { getEmployees, getFinancialData } from '../../services/employerService';

function EmployerDashboard() {
  const [employees, setEmployees] = useState([]);
  const [financialData, setFinancialData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const employeesData = await getEmployees();
        const financialInfo = await getFinancialData();
        setEmployees(employeesData);
        setFinancialData(financialInfo);
      } catch (error) {
        console.error("Error fetching employer data:", error);
      }
    };
    fetchData();
  }, []);

  return (
    <div>
      <h1>Employer Dashboard</h1>
      <h3>Employees</h3>
      <ul>
        {employees.map((employee) => (
          <li key={employee.id}>{employee.user.username}</li>
        ))}
      </ul>
      <h3>Financial Data</h3>
      {financialData ? (
        <div>
          <p>Total Revenue: ${financialData.total_revenue}</p>
          <p>Outstanding Payments: ${financialData.outstanding}</p>
        </div>
      ) : (
        <p>Loading financial data...</p>
      )}
    </div>
  );
}

export default EmployerDashboard;
