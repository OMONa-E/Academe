import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { getClientDetails } from '../../services/clientService';

function ClientDetails() {
    const { id } = useParams();
    const [client, setClient] = useState(null);

    useEffect(() => {
        const fetchClientDetails = async () => {
          try {
            const data = await getClientDetails(id);
            setClient(data)
          } catch (error) {
            console.error("Erro fetching client details:", error);
          }  
        };

        fetchClientDetails();
    }, [id]);

    if (!client) return <p>Loading client details....</p>;

    return (
        <div>
            <h2>{client.first_name} {client.last_name}</h2>
            <p>NIN: {client.nin}</p>
            <p>Email: {client.email}</p>
            <p>Phone: {client.phone_number}</p>
            <p>Status: {client.status}</p>
            <p>Payment Status: {client.payment_status ? "Paid": "Unpaid"}</p>
            <p>Assigned To: {client.assigned_employee.first_name} {client.assigned_employee.last_name}</p>
        </div>
    );
}

export default ClientDetails;