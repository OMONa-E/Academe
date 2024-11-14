import React, { useState } from "react";
import { createClient, updateClient } from "../../services/clientService";

function ClientForm({ client, onSubmit }) {
    const [firstName, setFirstName] = useState(client ? client.first_name: '');
    const [lastName, setLastName] = useState(client ? client.last_name: '');
    const [nin, setNIN] = useState(client ? client.nin : '');
    const [email, setEmail] = useState(client ? client.email : '');
    const [phone, setPhone] = useState(client ? client.phone_number : '');
    const [status, setStatus] = useState(client ? client.status : 'partial');

    const handleSubmit = async (e) => {
        e.preventDefault();
        const clientData = { first_name: firstName, last_name: lastName, email, phone_number: phone, status, nin }
        try {
            if (client) {
                await updateClient(client.id, clientData)
            } else {
                await createClient(clientData);
            }
            onSubmit();
        } catch (error) {
            console.error("Error saving client:", error);            
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input type="text" value={firstName} onChange={(e) => setFirstName(e.target.value)} placeholder="First Name" />
            <input type="text" value={lastName} onChange={(e) => setLastName(e.target.value)} placeholder="Last Name" />
            <input type="text" value={status} onChange={(e) => setStatus(e.target.value)} placeholder="Payment Status" />
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
            <input type="text" value={phone} onChange={(e) => setPhone(e.target.value)} placeholder="Phone Number" />
            <input type="text" value={nin} onChange={(e) => setNIN(e.target.value)} placeholder="National Identification Number" />
            <select value={status}>
                <option value="partial">Partial</option>
                <option value="full">Full</option>
            </select>
            <button type="submit">{client ? 'Update' : 'Create'} Client</button>
        </form>
    );
}

export default ClientForm;