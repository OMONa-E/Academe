import React, { useEffect, useState } from 'react';
import { getClients } from '../../services/clientService';

function ClientList() {
    const [clients, setClients] = useState([]);

    useEffect(() => {
        const fetchClients = async () => {
            try {
                const data = await getClients();
                setClients(data);
            } catch (error) {
                console.error("Error fatching clients:", error);                
            }        
        };

        fetchClients();
    }, []);

    return (
        <div>
            <h2>Clients</h2>
            <ul>
                {clients.map((client) => (
                    <li key={client.id}>
                        {client.first_name} {client.last_name} - Status: {client.status}
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default ClientList;