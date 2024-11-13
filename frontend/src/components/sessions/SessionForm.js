import React, { useState } from 'react';
import { createSession } from '../../services/sessionService';

function SessionForm({ onSubmit }) {
    const [cleintId, setClientId] = useState('');
    const [trainerId, setTrainerId] = useState('');
    const [moduleId, setModuleId] = useState('');
    const [sessionDateTime, setSessionDateTime] = useState('');
    const [status, setStatus] = useState('scheduled');

    const handleSubmit = async (e) => {
        e.preventDefault();
        const sessionData = { client: cleintId, trainer: trainerId, module: moduleId, session_date: sessionDateTime, status }
        try {
            await createSession(sessionData);
            onSubmit();
        } catch (error) {
            console.error("Error scheduling session:", error);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input type="text" value={cleintId} onChange={(e) => setClientId(e.target.value)} placeholder="Client ID" />
            <input type="text" value={trainerId} onChange={(e) => setTrainerId(e.target.value)} placeholder="Trainer ID" />
            <input type="text" value={moduleId} onChange={(e) => setModuleId(e.target.value)} placeholder="Module ID" />
            <input type="date" value={sessionDate} onChange={(e) => setSessionDateTime(e.target.value)} placeholder="Session Date" />
            <select value={status} onChange={(e) => setStatus(e.target.value)}>
                <option value="scheduled">Scheduled</option>
                <option value="completed">Completed</option>
                <option value="cancelled">Cancelled</option>
            </select>
            <button type="submit">Schedule Session</button>
        </form>
    );
}

export default SessionForm;