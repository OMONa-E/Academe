import React, { useContext, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../../context/AuthContext';

function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();
    const { handleLogin, getUserRole, getDashboardPath } = useContext(AuthContext);

    const handleLoginClick = async (e) => {
        e.preventDefault();
        try {
            await handleLogin(username, password);
            const role = getUserRole();
            const dashboardPath = getDashboardPath(role);
            setError('');
            navigate(dashboardPath);
        } catch (err) {
            setError('Login failed. Please check your credentials and try again.');
        }
    };    

    return (
        <div>
            <h2>Login</h2>
            <form onSubmit={handleLoginClick}>
                <input type='text' value={username} onChange={(e) => setUsername(e.target.value)} placeholder='Username' />
                <input type='password' value={password} onChange={(e) => setPassword(e.target.value)} placeholder='Password' />
                <button type='submit'>Login</button>
            </form>
            {error && <p>{error}</p>}
        </div>
    );
}

export default Login;