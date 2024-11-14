import React, { useContext, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../../context/AuthContext';
import {
  Box,
  TextField,
  Button,
  Typography,
  Divider,
  Link,
  IconButton,
} from '@mui/material';
import GoogleIcon from '@mui/icons-material/Google';
import AppleIcon from '@mui/icons-material/Apple';
// import WindowsIcon from '@mui/icons-material/Windows';
// import { Slack, SSO } from './CustomIcons'; // Assume you have custom icons for Slack and SSO

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
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        mt: 8,
        fontFamily: 'Karla, sans-serif',  // Default font for the component
      }}
    >
      <Typography
        variant="h3"
        gutterBottom
        sx={{
          fontFamily: '"Roboto Mono", monospace', // Override for Roboto Mono
          fontWeight: 'bold',
        }}
      >
        roadMasters
      </Typography>

      <Box component="form" onSubmit={handleLoginClick} sx={{ width: '100%', maxWidth: 400 }}>
        <TextField
          fullWidth
          margin="normal"
          label="Email"
          variant="outlined"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          slotProps={{ sx: { fontFamily: 'Karla, sans-serif' } }}
        />
        <TextField
          fullWidth
          margin="normal"
          label="Password"
          type="password"
          variant="outlined"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          slotProps={{ sx: { fontFamily: 'Karla, sans-serif' } }} // Karla for label
        />
        {error && <Typography color="error" sx={{ fontFamily: 'Karla, sans-serif' }}>{error}</Typography>}

        <Link href="#" variant="body2" sx={{ display: 'block', mt: 1, mb: 2, fontFamily: 'Karla, sans-serif' }}>
          Forgot password?
        </Link>

        <Button
          type="submit"
          variant="contained"
          color="primary"
          fullWidth
          sx={{ py: 1.5, mb: 2, fontFamily: 'Karla, sans-serif' }}
        >
          Log in
        </Button>

        <Divider sx={{ my: 2 }}>or</Divider>

        <Button
          variant="outlined"
          color="secondary"
          fullWidth
          startIcon={<GoogleIcon />}
          sx={{ mb: 1, fontFamily: 'Karla, sans-serif' }}
        >
          Continue with Google
        </Button>

        <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 1 }}>
          {/* <IconButton><WindowsIcon /></IconButton> */}
          <IconButton><AppleIcon /></IconButton>
          {/* <IconButton><Slack /></IconButton> */}
          <Button variant="outlined" sx={{ fontFamily: 'Karla, sans-serif' }}>SAML SSO</Button>
        </Box>

        <Typography variant="body2" sx={{ mt: 3, fontFamily: 'Karla, sans-serif' }}>
          Don't have an account yet? <Link href="#">Sign up here →</Link>
        </Typography>
      </Box>
    </Box>
  );
}

export default Login;
