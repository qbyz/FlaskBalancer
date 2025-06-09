import React, { useState, useEffect } from 'react';
import './index.css';

export default function BalanceFrontend() {
    const [equation, setEquation] = useState('');
    const [result, setResult] = useState(null);
    const [matrix, setMatrix] = useState('');
    const [elementInfo, setElementInfo] = useState('');
    const [coefficients, setCoefficients] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [darkMode, setDarkMode] = useState(true);

    useEffect(() => {
        if (darkMode) {
            document.body.classList.add('dark');
        } else {
            document.body.classList.remove('dark');
        }
    }, [darkMode]);

    async function handleSubmit(e) {
        e.preventDefault();
        setLoading(true);
        setError('');
        setResult(null);

        try {
            const response = await fetch('https://flaskbalancer.onrender.com/balance', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ equation, isRace: false })
            });

            if (!response.ok) {
                const errorData = await response.json();
            }

            const data = await response.json();
            setResult(data.balanced);
            setMatrix(data.matrix);
            setElementInfo(data.element_info);
            setCoefficients(data.coefficients);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className={darkMode ? 'dark' : ''}>
            <button className='darkButton' onClick={() => setDarkMode(!darkMode)} /* styling */>
                {darkMode ? '☀️' : '🌙'}
            </button>


                <h1 className="title">Chemical Equation Balancer</h1>

                <form onSubmit={handleSubmit} className="box">
                    <input
                        type="text"
                        value={equation}
                        onChange={(e) => setEquation(e.target.value)}
                        placeholder="Enter chemical equation like: H^2 + O^2 = H^2O"
                        className="input"
                    />
                    <button
                        type="submit"
                        className="button"
                        disabled={loading}
                    >
                        {loading ? 'Balancing...' : 'Balance'}
                    </button>
                    {error && <div className="error">{error}</div>}
                </form>

                {result && (
                    <div className="results">
                        <div className="box">
                            <h2 className="subtitle">Balanced Equation</h2>
                            <p>{result}</p>
                        </div>
                        <div className="box">
                            <h2 className="subtitle">Matrix</h2>
                            <p>{matrix}</p>
                        </div>
                        <div className="box">
                            <h2 className="subtitle">Element Info</h2>
                            <p>{elementInfo}</p>
                        </div>
                        <div className="box">
                            <h2 className="subtitle">Coefficients</h2>
                            <p>{coefficients.join(', ')}</p>
                        </div>
                    </div>
                )}
            </div>
    );
}
