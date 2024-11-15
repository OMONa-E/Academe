import React from 'react';
import { Container, Grid2, Paper, Typography, List, ListItem, ListItemText, Divider} from '@mui/material';
import { styled } from '@mui/material/styles';

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

const EmployerDashboard = () => {
  return (
    <Container>
      <Root>
        <Grid2 container spacing={3}>
          {/* Sidebar */}
          <Sidebar item xs={2}>
            <List component="nav">
              <ListItem button>
                <ListItemText primary="Dashboard" />
              </ListItem>
              <ListItem button>
                <ListItemText primary="Employee" />
              </ListItem>
              <ListItem button>
                <ListItemText primary="Client" />
              </ListItem>
              <ListItem button>
                <ListItemText primary="Academy" />
              </ListItem>
              <ListItem button>
                <ListItemText primary="Profile" />
              </ListItem>
              <ListItem button>
                <ListItemText primary="Notifications" />
              </ListItem>
              <Divider />
              <ListItem button>
                <ListItemText primary="Sign Out" />
              </ListItem>
            </List>
          </Sidebar>

          {/* Main Content */}
          <Content item xs={10}>
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
          </Content>
        </Grid2>
      </Root>
    </Container>
  );
};

export default EmployerDashboard;
