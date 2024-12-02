import { AppBar, Toolbar, Typography, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import logo from '../assets/logo.png';

function NavBar() {
  const navigate = useNavigate();

  return (
    <AppBar position="static">
      <Toolbar>
        <Button onClick={() => navigate('/')}>
          <img src={logo} alt="Prédict Car Logo" style={{ height: '50px', marginRight: '10px' }} />
        </Button>
        <Typography variant="h6" sx={{ flexGrow: 1 }}>
        </Typography>
        <Button color="inherit" onClick={() => navigate('/')}>
          Accueil
        </Button>
        <Button color="inherit" onClick={() => navigate('/predict')}>
          Prédiction Prix
        </Button>
        <Button color="inherit" onClick={() => navigate('/visualize')}>
          Visualisation des Données
        </Button>
      </Toolbar>
    </AppBar>
  );
}

export default NavBar;