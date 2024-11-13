import React, { useEffect, useState } from 'react';
import { getSessions } from '../../services/sessionService';

function SessionList() {
    const [sessions, setSessions] = useState([]);

    useEffect(() => {
        const fetchSessions = async () => {
            try {
                const data = await getSessions();
                setSessions(data);     
            } catch (error) {
                console.error("Error fetching sessions:", error);                
            }
        };
        fetchSessions();
    }, []);

    return (
        <div>
            <h2>Training Sessions</h2>
            <ul>
                {sessions.map((session) => (
                    <li key={session.id}>
                        Client: {session.client.first_name} {session.client.last_name} | Date: {session.session_date} | Status: {session.status}
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default SessionList;