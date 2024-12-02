import { Box, Typography, Link } from '@mui/material';

export default function Footer() {
  return (
    <Box 
      sx={{
        backgroundColor: 'primary.main', 
        color: 'white', 
        textAlign: 'center', 
        padding: 2, 
        mt: 4
      }}
    >
      <Typography variant="body1">
        © 2024 Prédict Car - Tous droits réservés.
      </Typography>

      <Typography variant="body2" mt={2}>
        <Link href="https://rands.netlify.app/" color="inherit" underline="hover">
          Sébastien Rapuzzi
        </Link>
        {' | '}
        <Link href="https://www.linkedin.com/in/yamine-aissani-876514254/" color="inherit" underline="hover">
          Yamine Aissani
        </Link>
        {' | '}
        <Link href="https://www.mathieu-soussignan.com" color="inherit" underline="hover">
          Mathieu Soussignan
        </Link>
      </Typography>
    </Box>
  );
}