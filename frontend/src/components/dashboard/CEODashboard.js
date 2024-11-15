import React, { useState } from 'react';
import { Container, Grid2, Paper, Typography, List, ListItem, ListItemText, Divider } from '@mui/material';
import { styled } from '@mui/material/styles';
import EmployerComponent from '../employer/EmployerComponent';
import LogoutButton from '../auth/LogoutButton';

// Styled components
const Root = styled('div')(({ theme }) => ({
  flexGrow: 1,
  fontFamily: 'Karla, sans-serif',
}));

const Sidebar = styled(Grid2)(({ theme }) => ({
  height: '100vh',
  backgroundColor: theme.palette.background.paper,
  padding: theme.spacing(2),
}));

const Content = styled(Grid2)(({ theme }) => ({
  padding: theme.spacing(3),
}));

const StyledPaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(2),
  textAlign: 'center',
  color: theme.palette.text.secondary,
}));

const CEODashboard = () => {
  const [selectedSection, setSelectedSection] = useState('Dashboard');
  const handleSidebarClick = (section) => setSelectedSection(section); // handler for sidebar item click

  const renderContent = () => { // render content based on selected section
    switch (selectedSection) {
      case 'Employer':
        return <EmployerComponent />;
      case 'Employee':
        // return <EmployeeComponent />;
        break;
        case 'Client':
          // return <ClientComponent />;
          break;
        case 'Academy':
          // return <AcademyComponent />;
          break;
        case 'Finance':
          // return <FinanceComponent />;
          break;
        case 'Profile':
          // return <ProfileComponent />;
          break;
        case 'Notification':
          // return <NotificationComponent />;
          break;
        case 'Sign Out':
            return <LogoutButton />;
        default:
          return (
            <Grid2 container spacing={3}>
              <Grid2 item xs={3}>
                <StyledPaper>
                  <Typography variant="h6">Bookings</Typography>
                  <Typography variant="h4">281</Typography>
                  <Typography variant="body2">+55% than last week</Typography>
                </StyledPaper>
              </Grid2>
              <Grid2 item xs={3}>
                <StyledPaper>
                  <Typography variant="h6">Today's Users</Typography>
                  <Typography variant="h4">2,300</Typography>
                  <Typography variant="body2">+3% than last month</Typography>
                </StyledPaper>
              </Grid2>
              <Grid2 item xs={3}>
                <StyledPaper>
                  <Typography variant="h6">Revenue</Typography>
                  <Typography variant="h4">34k</Typography>
                  <Typography variant="body2">+1% than yesterday</Typography>
                </StyledPaper>
              </Grid2>
              <Grid2 item xs={3}>
                <StyledPaper>
                  <Typography variant="h6">Followers</Typography>
                  <Typography variant="h4">+91</Typography>
                  <Typography variant="body2">Just updated</Typography>
                </StyledPaper>
              </Grid2>
            </Grid2>
          );
    }
  };
  return (
    <Container>
      <Root>
        <Grid2 container spacing={3}>
          {/* Sidebar */}
          <Sidebar item xs={2}>
            <List component="nav">
              {['Dashboard', 'Employer', 'Employee', 'Client', 'Academy', 'Finance', 'Profile', 'Notification'].map((section) => (
                <ListItem button key={section} onClick={() => handleSidebarClick(section)}>
                  <ListItemText primary={section} />
                </ListItem>
              ))}              
              <Divider />
              <ListItem button onClick={() => handleSidebarClick('Sign Out')}>
                <ListItemText primary="Sign out" />
              </ListItem>
            </List>
          </Sidebar>

          {/* Main Content */}
          <Content item xs={10}>
            {renderContent()}
          </Content>
        </Grid2>
      </Root>
    </Container>
  );
};

export default CEODashboard;
