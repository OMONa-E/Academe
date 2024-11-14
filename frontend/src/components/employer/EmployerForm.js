import React, { useState, useEffect } from "react";
import { updateEmployer } from "../../services/employerService";

function EmployerForm({ employer, onSubmit }) {
    // State for each field with initial values based on `employer` prop
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [nin, setNIN] = useState('');
    const [email, setEmail] = useState('');
    const [dateOfBirth, setDateOfBirth] = useState('');
    const [department, setDepartment] = useState('training');
    const [error, setError] = useState(null);

    // Effect to update state if `employer` prop changes
    useEffect(() => {
        if (employer) {
            setFirstName(employer.user.first_name || '');
            setLastName(employer.user.last_name || '');
            setNIN(employer.user.nin || '');
            setEmail(employer.user.email || '');
            setDateOfBirth(employer.user.date_of_birth || '');
            setDepartment(employer.department || 'training');
        }
    }, [employer]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        // Structuring employerData with the nested `user` object
        const employerData = {
            user: {
                first_name: firstName,
                last_name: lastName,
                email,
                date_of_birth: dateOfBirth,
                nin,
            },
            department,
        };

        try {
            if (employer) {
                await updateEmployer(employer.id, employerData); // Call the API to update the employer data
            }
            onSubmit(); // Trigger callback after a successful update
        } catch (error) {
            console.error("Error saving employer:", error);
            setError("An error occurred while updating employer details.");
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            <input type="text" value={firstName} onChange={(e) => setFirstName(e.target.value)} placeholder="First Name" />
            <input type="text" value={lastName} onChange={(e) => setLastName(e.target.value)} placeholder="Last Name" />
            <input type="date" value={dateOfBirth} onChange={(e) => setDateOfBirth(e.target.value)} placeholder="Date of Birth" />
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
            <input type="text" value={nin} onChange={(e) => setNIN(e.target.value)} placeholder="National Identification Number" />
            <select value={department} onChange={(e) => setDepartment(e.target.value)}>
                <option value="" disabled>Select Department</option>
                <option value="training">Training</option>
                <option value="finance">Finance</option>
                <option value="farewell">Farewell</option>
            </select>
            <button type="submit">Update Employer</button>
        </form>
    );
}

export default EmployerForm;
