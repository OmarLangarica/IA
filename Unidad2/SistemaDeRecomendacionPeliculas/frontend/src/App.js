import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [titles, setTitles] = useState([]);
  const [loadingTitles, setLoadingTitles] = useState(true);
  const [titlesError, setTitlesError] = useState(null);
  const [selected, setSelected] = useState('');
  const [movieInfo, setMovieInfo] = useState(null);
  const [recs, setRecs] = useState([]);

  useEffect(() => {
    // Carga lista de títulos desde el backend
    setLoadingTitles(true);
    fetch('/movies')
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
    .then((data) => {
      // backend devuelve { movies: [ {title, genres, actors, director}] }
      setTitles(data.movies || []);
        setTitlesError(null);
      })
      .catch((err) => {
        console.error('Error fetching titles', err);
        setTitlesError(String(err));
        setTitles([]);
      })
      .finally(() => setLoadingTitles(false));
  }, []);

  const getRecommendations = () => {
    if (!selected) return;
    fetch(`/recommendations?title=${encodeURIComponent(selected)}&top_k=5`)
      .then((res) => res.json())
      .then((data) => {
        if (data.error) {
          setMovieInfo(null);
          setRecs([]);
          alert(data.error);
        } else {
          setMovieInfo(data.movie);
          setRecs(data.recommendations || []);
        }
      })
      .catch((err) => console.error('Error fetching recommendations', err));
  };

  return (
    <div className="App">
      <header className="App-header">
        <h2>Sistema de Recomendación de Películas</h2>
      </header>

      <main className="container">
        <div className="controls">
          <label htmlFor="movie-select">Elige una película:</label>
          {loadingTitles ? (
            <span> Cargando títulos...</span>
          ) : titlesError ? (
            <span className="error">Error cargando títulos: {titlesError}</span>
          ) : (
            <select
              id="movie-select"
              className="movie-select"
              value={selected}
              onChange={(e) => setSelected(e.target.value)}
            >
              <option value="">-- Seleccionar --</option>
              {titles.map((m, i) => (
                <option key={i} value={m.title} title={`${m.actors} — ${m.director}`}>
                  {m.title}
                </option>
              ))}
            </select>
          )}

          <button className="btn-primary" onClick={getRecommendations} disabled={!selected}>
            Obtener recomendacion
          </button>
        </div>

        {movieInfo && (
          <section className="movie-info">
            <h3>Película seleccionada</h3>
            <p><strong>Título:</strong> {movieInfo.title}</p>
            <p className="letra-chiquita"><strong>Géneros:</strong> {movieInfo.genres}</p>
            <p className="letra-chiquita"><strong>Actores:</strong> {movieInfo.actors}</p>
            <p className="letra-chiquita"><strong>Director:</strong> {movieInfo.director}</p>
          </section>
        )}

        {recs.length > 0 && (
          <section className="recomendaciones">
            <h3>Recomendaciones</h3>
            <div className="rec-grid">
              {recs.map((r, i) => (
                <div className="rec-card" key={i}>
                  <h4 className="rec-titulo">{r.title}</h4>
                  <div className="rec-meta">{r.genres}</div>
                  <div className="rec-meta">Actores: {r.actors}</div>
                  <div className="rec-meta">Director: {r.director}</div>
                  <div className="rec-score">Score: {r.score.toFixed(3)}</div>
                </div>
              ))}
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

export default App;
