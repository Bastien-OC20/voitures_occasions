import { useEffect, useState } from "react";
import Plot from 'react-plotly.js';
import axios from "axios";
import { Typography, Box, FormGroup, FormControlLabel, Checkbox } from "@mui/material";

function AnnéeParMarqueChart() {
  const [chartData, setChartData] = useState([]);
  const [allBrands, setAllBrands] = useState([]);
  const [selectedBrands, setSelectedBrands] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchChartData = async () => {
      try {
        const response = await axios.get(
          `${import.meta.env.VITE_API_BASE_URL}/data/year-brand-distribution`
        );

        if (response.data && Array.isArray(response.data) && response.data.length > 0) {
          // Organiser les données pour une utilisation facile dans le graphique
          const dataByYearAndBrand = response.data.reduce((acc, item) => {
            const year = item["Annee"];
            const brand = item["Marque"];
            const count = item["Count"];

            if (!acc[brand]) {
              acc[brand] = {};
            }
            acc[brand][year] = count;

            return acc;
          }, {});

          setAllBrands(Object.keys(dataByYearAndBrand));
          setSelectedBrands(Object.keys(dataByYearAndBrand).slice(0, 5)); // Par défaut, sélectionner les 5 premières marques
          setChartData(dataByYearAndBrand);
        } else {
          setError("Aucune donnée disponible pour le graphique.");
        }
      } catch (err) {
        setError("Erreur lors du chargement des données.");
        console.error("Erreur lors du chargement des données:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchChartData();
  }, []);

  const handleBrandChange = (brand) => {
    setSelectedBrands((prevSelected) => {
      if (prevSelected.includes(brand)) {
        return prevSelected.filter((b) => b !== brand);
      } else {
        return [...prevSelected, brand];
      }
    });
  };

  if (loading) {
    return <div>Chargement des données...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  // Préparer les données pour Plotly (barres empilées)
  const years = [...new Set(Object.values(chartData).flatMap(brand => 
    Object.keys(brand)
  ))].sort();
  const plotData = selectedBrands.map((brand) => {
    const counts = years.map((year) => chartData[brand][year] || 0);
    return {
      x: years,
      y: counts,
      type: 'bar',
      name: brand,
    };
  });

  return (
    <Box>
      <FormGroup row>
        {allBrands.map((brand) => (
          <FormControlLabel
            key={brand}
            control={
              <Checkbox
                checked={selectedBrands.includes(brand)}
                onChange={() => handleBrandChange(brand)}
              />
            }
            label={brand}
          />
        ))}
      </FormGroup>
      <Plot
        data={plotData}
        layout={{
          title: "Distribution des Années par Marque",
          barmode: 'stack',
          xaxis: { title: "Année" },
          yaxis: { title: "Nombre de véhicules" },
        }}
        style={{ width: "100%", height: "500px" }}
      />
      <Box mt={2} p={2} style={{ backgroundColor: "#c6deef", borderRadius: "8px" }}>
        <Typography variant="body1" align="center">
          Ce graphique montre la distribution des véhicules vendus par année, avec une représentation de chaque marque sous forme de barres empilées. Sélectionnez les marques que vous souhaitez voir pour comparer leur présence sur le marché.
        </Typography>
      </Box>
    </Box>
  );
}

export default AnnéeParMarqueChart;