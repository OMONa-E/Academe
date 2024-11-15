import React, { useState, useEffect } from 'react';
import {
    Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper,
    Button, Dialog, DialogActions, DialogContent, DialogTitle, TextField, MenuItem
  } from '@mui/material';
import { getEmployers, updateEmployer, deleteEmployer } from '../../services/employerService';
import { registerEmployer } from '../../services/authService';

const EmployerComponent = () => {
    const [employers, setEmployers] = useState([]);
    const [currentEmployer, setCurrentEmployer] = useState(null);
    const [openForm, setOpenForm] = useState(false);
    const [formType, setFormType] = useState(''); // Determine whether it's 'Create', 'Update', or 'View'
    // Form Fields
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [department, setDepartment] = useState('training');
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [nin, setNIN] = useState('');
    const [dateOfBirth, setDateOfBirth] = useState('');

    useEffect(() => {
        fetchEmployers();
    }, []);

    const fetchEmployers = async () => {
        try {
            const data = await getEmployers();
            setEmployers(data);
        } catch (error) {
            console.error("Error fetching employers:", error)
        }
    };

    const handleOpenForm = (type, employer=null) => {
        setFormType(type);
        setCurrentEmployer(employer);
        if (employer) { // Populate form with employer details for editing/viewing
            setUsername(employer.user.username);
            setEmail(employer.user.email);
            setFirstName(employer.user.first_name);
            setLastName(employer.user.last_name);
            setNIN(employer.user.nin);
            setDateOfBirth(employer.user.date_of_birth);
            setDepartment(employer.department);
        } else { // Clear form for new entry
            setUsername('');
            setEmail('');
            setPassword('');
            setFirstName('');
            setLastName('');
            setNIN('');
            setDateOfBirth('');
            setDepartment('training');
        }
        setOpenForm(true);
    };

    const handleCloseForm = () => setOpenForm(false);

    const handleDelete = async (employerId) => {
        try {
            await deleteEmployer(employerId);
            fetchEmployers();
        } catch (error) {
            console.error("Error deleting employer:", error);
        }
    };

    const handleFormSubmit = async (e) => {
        e.preventDefault();
        if (formType === 'create') {
            try {
                const data = {
                    user: {username, email, password, first_name: firstName, last_name: lastName,},
                    department,
                };
                await registerEmployer(data);
                fetchEmployers();
            } catch (error) {
                console.error("Error registering employer:", error);
            }
        } else if (formType === 'update' && currentEmployer) {
            try {
                const data = {
                  user: {first_name: firstName, last_name: lastName, email, date_of_birth: dateOfBirth, nin,},
                  department,
                };
                await updateEmployer(currentEmployer.id, data);
                fetchEmployers();
            } catch (error) {
                console.error("Error updating employer:", error);
            }
        }
        handleCloseForm();
    }

    return (
        <div>
            <Button variant="contained" color="primary" onClick={() => handleOpenForm('create')}>
                Add New Employer
            </Button>
            <TableContainer component={Paper}>
                <Table>
                <TableHead>
                    <TableRow>
                    <TableCell>Username</TableCell>
                    <TableCell>Email</TableCell>
                    <TableCell>Department</TableCell>
                    <TableCell>Actions</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {employers.map((employer) => (
                    <TableRow key={employer.id}>
                        <TableCell>{employer.user.username}</TableCell>
                        <TableCell>{employer.user.email}</TableCell>
                        <TableCell>{employer.department}</TableCell>
                        <TableCell>
                        <Button onClick={() => handleOpenForm('view', employer)} color="primary">View</Button>
                        <Button onClick={() => handleOpenForm('update', employer)} color="secondary">Edit</Button>
                        <Button onClick={() => handleDelete(employer.id)} color="error">Delete</Button>
                        </TableCell>
                    </TableRow>
                    ))}
                </TableBody>
                </Table>
            </TableContainer>

            {/* Form Dialog for Create, Update, and View */}
            <Dialog open={openForm} onClose={handleCloseForm}>
                <DialogTitle>{formType === 'create' ? 'Register Employer' : formType === 'update' ? 'Edit Employer' : 'Employer Details'}</DialogTitle>
                <DialogContent>
                    {formType !== 'view' ? (
                        <form onSubmit={handleFormSubmit}>
                        {formType === 'create' && (
                            <>
                            <TextField label="Username" fullWidth value={username} onChange={(e) => setUsername(e.target.value)} />
                            <TextField label="Password" type="password" fullWidth value={password} onChange={(e) => setPassword(e.target.value)} />
                            </>
                        )}
                        <TextField label="Email" fullWidth value={email} onChange={(e) => setEmail(e.target.value)} />
                        <TextField label="First Name" fullWidth value={firstName} onChange={(e) => setFirstName(e.target.value)} />
                        <TextField label="Last Name" fullWidth value={lastName} onChange={(e) => setLastName(e.target.value)} />
                        <TextField label="NIN" fullWidth value={nin} onChange={(e) => setNIN(e.target.value)} />
                        <TextField label="Date of Birth" type="date" fullWidth value={dateOfBirth} onChange={(e) => setDateOfBirth(e.target.value)} />
                        <TextField label="Department" select fullWidth native value={department} onChange={(e) => setDepartment(e.target.value)} >
                            <MenuItem value="training">Training</MenuItem>
                            <MenuItem value="finance">Finance</MenuItem>
                            <MenuItem value="farewell">Farewell</MenuItem>
                        </TextField>
                        <DialogActions>
                            <Button onClick={handleCloseForm} color="primary">Cancel</Button>
                            <Button type="submit" color="primary">Save</Button>
                        </DialogActions>
                        </form>
                    ) : (
                        <div>
                            <p><strong>Username:</strong> {username}</p>
                            <p><strong>Email:</strong> {email}</p>
                            <p><strong>First Name:</strong> {firstName}</p>
                            <p><strong>Last Name:</strong> {lastName}</p>
                            <p><strong>NIN:</strong> {nin}</p>
                            <p><strong>Date of Birth:</strong> {dateOfBirth}</p>
                            <p><strong>Department:</strong> {department}</p>
                            <Button onClick={handleCloseForm} color="primary">Close</Button>
                        </div>
                    )}
                </DialogContent>
            </Dialog>
        </div>
    );
};

export default EmployerComponent;