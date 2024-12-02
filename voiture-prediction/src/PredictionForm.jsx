import { useState } from 'react';
import axios from 'axios';
import {
  Container,
  Typography,
  TextField,
  Button,
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Slider,
  LinearProgress,
  Paper,
} from '@mui/material';

function PredictionForm() {
  const [formData, setFormData] = useState({
    kilometrage: 15000,
    annee: 2020,
    marque: 'Peugeot',
    carburant: 'Essence',
    transmission: 'Manuelle',
    modele: '208',
    etat: 'Occasion',
  });
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);

  const marquesDisponibles = [
    'Audi', 'BMW', 'Citroën', 'Dacia', 'Fiat', 'Ford', 'Honda', 'Hyundai', 'Jeep',
    'Kia', 'Lexus', 'Mazda', 'Mercedes-Benz', 'Mini', 'Mitsubishi', 'Nissan', 'Opel',
    'Peugeot', 'Renault', 'Seat', 'Skoda', 'Smart', 'Subaru', 'Suzuki', 'Tesla',
    'Toyota', 'Volkswagen', 'Volvo'
  ];

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSliderChange = (field) => (event, value) => {
    setFormData({ ...formData, [field]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      // Simuler une attente de 3 secondes pour l'utilisateur
      setTimeout(async () => {
        const response = await axios.post(
          `${import.meta.env.VITE_API_BASE_URL}/predict_combined`,
          formData
        );
        setPrediction(response.data);
        setLoading(false);
      }, 3000);
    } catch (error) {
      console.error('Erreur lors de la prédiction', error);
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="sm" sx={{ marginTop: '50px' }}>
      <Typography variant="h4" gutterBottom>
        Prédiction des Voitures d&apos;Occasion
      </Typography>
      <Box component="form" onSubmit={handleSubmit} sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
        
        {/* Section Kilométrage et Année */}
        <Typography variant="h6">Caractéristiques du Véhicule</Typography>
        <FormControl fullWidth>
          <Typography gutterBottom>Kilométrage (en km)</Typography>
          <Slider
            value={formData.kilometrage}
            onChange={handleSliderChange('kilometrage')}
            min={0}
            max={300000}
            step={1000}
            valueLabelDisplay="auto"
            name="kilometrage"
          />
        </FormControl>
        <FormControl fullWidth>
          <Typography gutterBottom>Année de Mise en Circulation</Typography>
          <Slider
            value={formData.annee}
            onChange={handleSliderChange('annee')}
            min={1980}
            max={2024}
            step={1}
            valueLabelDisplay="auto"
            name="annee"
          />
        </FormControl>

        <FormControl fullWidth>
          <InputLabel>Marque</InputLabel>
          <Select
            name="marque"
            value={formData.marque}
            onChange={handleChange}
          >
            {marquesDisponibles.map((marque) => (
              <MenuItem key={marque} value={marque}>
                {marque}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <TextField
          label="Modèle"
          variant="outlined"
          name="modele"
          type="text"
          value={formData.modele}
          onChange={handleChange}
        />
        <FormControl fullWidth>
          <InputLabel>Transmission</InputLabel>
          <Select
            name="transmission"
            value={formData.transmission}
            onChange={handleChange}
          >
            <MenuItem value="Manuelle">Manuelle</MenuItem>
            <MenuItem value="Automatique">Automatique</MenuItem>
          </Select>
        </FormControl>
        <FormControl fullWidth>
          <InputLabel>Type de Carburant</InputLabel>
          <Select
            name="carburant"
            value={formData.carburant}
            onChange={handleChange}
          >
            <MenuItem value="Essence">Essence</MenuItem>
            <MenuItem value="Diesel">Diesel</MenuItem>
            <MenuItem value="Hybride">Hybride</MenuItem>
            <MenuItem value="Électrique">Électrique</MenuItem>
          </Select>
        </FormControl>
        <TextField
          label="État"
          variant="outlined"
          name="etat"
          type="text"
          value={formData.etat}
          onChange={handleChange}
        />
        <Button variant="contained" color="primary" type="submit" disabled={loading}>
          Prédire le Prix
        </Button>
      </Box>
      {loading && (
        <Box mt={2}>
          <LinearProgress />
          <Typography variant="body2" align="center" mt={2}>
            Prédiction en cours, veuillez patienter...
          </Typography>
        </Box>
      )}
      {prediction && (
        <Box mt={4} component={Paper} elevation={3} p={3} sx={{ backgroundColor: prediction.deal_classification === 'Bonne affaire' ? '#c8e6c9' : '#ffcdd2' }}>
          <Typography variant="h6" align="center">
            Prix estimé : {prediction.predicted_price} €
          </Typography>
          <Typography variant="h6" align="center">
            Classification : {prediction.deal_classification}
          </Typography>
        </Box>
      )}
    </Container>
  );
}

export default PredictionForm;