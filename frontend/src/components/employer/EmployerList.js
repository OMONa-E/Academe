import React, { useEffect, useState } from 'react';
import { getEmployers } from '../../services/employerService';

function EmployerList() {
    const [employers, setEmployers] = useState([]);

    useEffect(() => {
        const fetchEmployers = async () => {
            try {
                const data = await getEmployers();
                setEmployers(data);
            } catch (error) {
                console.error("Error fatching employers:", error);                
            }        
        };

        fetchEmployers();
    }, []);

    return (
        <div>
            <h2>employers</h2>
            <ul>
                {employers.map((employer) => (
                    <li key={employer.id}>
                        {employer.user.first_name} {employer.user.last_name} - NIN: {employer.status}
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default EmployerList;