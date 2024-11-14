import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { getEmployerDetails } from '../../services/employerService';

function EmployerDetails() {
    const { id } = useParams();
    const [employer, setEmployer] = useState(null);

    useEffect(() => {
        const fetchEmployerDetails = async () => {
          try {
            const data = await getEmployerDetails(id);
            setEmployer(data)
          } catch (error) {
            console.error("Erro fetching employer details:", error);
          }  
        };

        fetchEmployerDetails();
    }, [id]);

    if (!employer) return <p>Loading employer details....</p>;

    return (
        <div>
            <h2>{employer.user.first_name} {employer.user.last_name}</h2>
            <p>NIN: {employer.user.nin}</p>
            <p>Email: {employer.user.email}</p>
            <p>Date of Birth: {employer.user.date_of_birth}</p>
            <p>Department: {employer.department}</p>
        </div>
    );
}

export default EmployerDetails;