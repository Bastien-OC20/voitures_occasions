import PropTypes from 'prop-types';
import { AppBar, Toolbar, Typography, Switch, Box } from '@mui/material';
import { Link } from 'react-router-dom';
import logo from '../assets/logo.png';
import { createTheme, ThemeProvider } from '@mui/material/styles';

export default function NavBar({ darkMode, setDarkMode }) {
  return (
    <ThemeProvider
      theme={createTheme({
        palette: {
          mode: darkMode ? 'dark' : 'light',
        },
      })}
    >
      <AppBar position="static">
        <Toolbar>
          {/* Logo avec navigation vers l'accueil */}
          <Link to="/" style={{ display: 'flex', alignItems: 'center' }}>
            <img src={logo} alt="Prédict Car Logo" style={{ height: '50px', marginRight: '60px' }} />
          </Link>

          <Box sx={{ display: 'flex', gap: 2, flexGrow: 1 }}>
            <Link to="/" style={{ color: 'inherit', textDecoration: 'none' }}>
              <Typography variant="h6">Accueil</Typography>
            </Link>
            <Link to="/predict" style={{ color: 'inherit', textDecoration: 'none' }}>
              <Typography variant="h6">Prédiction</Typography>
            </Link>
            <Link to="/visualize" style={{ color: 'inherit', textDecoration: 'none' }}>
              <Typography variant="h6">Visualisation</Typography>
            </Link>
          </Box>

          {/* Toggle Dark/Light Mode */}
          <Switch
            checked={darkMode}
            onChange={() => setDarkMode(!darkMode)}
            color="default"
          />
        </Toolbar>
      </AppBar>
    </ThemeProvider>
  );
}

NavBar.propTypes = {
  darkMode: PropTypes.bool.isRequired,
  setDarkMode: PropTypes.func.isRequired,
};