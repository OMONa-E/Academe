import React, { useContext } from 'react';
import { AuthContext } from '../../context/AuthContext';
import { useNavigate } from 'react-router-dom';

function LogoutButton() {
    const { handleLogout } = useContext(AuthContext);
    const navigate = useNavigate();

    const onLogout = async () => {
        await handleLogout();
        navigate("/login");
    };

    return (
        <button onClick={onLogout}>Logout</button>
    );
}

export default LogoutButton;