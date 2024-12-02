import { BrowserRouter as Router, Route, Routes, useLocation } from 'react-router-dom';
import { AnimatePresence, motion } from 'framer-motion';
import HomePage from './pages/HomePage';
import NavBar from './pages/NavBar';
import PredictionForm from './PredictionForm';
import VisualizationPage from "./pages/VisualizationPage";

function App() {
  const location = useLocation();

  return (
    <>
      <NavBar />
      {/* AnimatePresence est utilisé pour animer la sortie de l'ancienne page */}
      <AnimatePresence mode="wait">
        {/* Les Routes sont enveloppées dans AnimatePresence et chaque route est un composant motion.div */}
        <Routes location={location} key={location.pathname}>
          <Route
            path="/"
            element={
              <motion.div
                initial={{ opacity: 0, x: -100 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 100 }}
                transition={{ duration: 0.5 }}
              >
                <HomePage />
              </motion.div>
            }
          />
          <Route
            path="/predict"
            element={
              <motion.div
                initial={{ opacity: 0, x: -100 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 100 }}
                transition={{ duration: 0.5 }}
              >
                <PredictionForm />
              </motion.div>
            }
          />
          <Route
            path="/visualize"
            element={
              <motion.div
                initial={{ opacity: 0, x: -100 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 100 }}
                transition={{ duration: 0.5 }}
              >
                <VisualizationPage />
              </motion.div>
            }
          />
        </Routes>
      </AnimatePresence>
    </>
  );
}

export default function WrappedApp() {
  return (
    <Router>
      <App />
    </Router>
  );
}