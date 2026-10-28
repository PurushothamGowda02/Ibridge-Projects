import React, { useEffect, useState } from 'react';
import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ReferenceArea,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from 'recharts';
import { Activity, Database, GitCompareArrows, TrendingUp } from 'lucide-react';
import { format, parseISO } from 'date-fns';
import './index.css';

const API_URL = "http://localhost:8000/api";
const DISPLAY_HISTORY_DAYS = 14;
const TRAINING_HISTORY_DAYS = 60;
const FORECAST_STEPS = 12;
const RESAMPLE_HOURS = 6;
const VAR_LAG_ORDER = 4;

const formatForecastValue = (value, digits = 1) => (
  typeof value === "number" ? value.toFixed(digits) : "N/A"
);

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className="custom-tooltip">
        <p className="label">{format(parseISO(label), 'MMM dd, HH:mm')}</p>
        {payload.map((entry, index) => (
          <p key={index} style={{ color: entry.color }}>
            {entry.name}: {formatForecastValue(entry.value, 2)}
          </p>
        ))}
      </div>
    );
  }
  return null;
};

function App() {
  const [historicalData, setHistoricalData] = useState([]);
  const [forecastData, setForecastData] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  const metrics = {
    temperature: { name: "Temperature", unit: "deg C", color: "#ef4444" },
    humidity: { name: "Humidity", unit: "%", color: "#3b82f6" },
    pressure: { name: "Pressure", unit: "hPa", color: "#10b981" },
    wind: { name: "Wind Speed", unit: "km/h", color: "#f59e0b" }
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError("");

        const histRes = await fetch(`${API_URL}/weather/historical?days=${DISPLAY_HISTORY_DAYS}`);
        if (!histRes.ok) {
          throw new Error(`Historical request failed: ${histRes.status}`);
        }
        const histJson = await histRes.json();

        const foreRes = await fetch(`${API_URL}/weather/forecast?steps=${FORECAST_STEPS}`);
        if (!foreRes.ok) {
          throw new Error(`Forecast request failed: ${foreRes.status}`);
        }
        const foreJson = await foreRes.json();

        setHistoricalData(histJson.data || []);
        setForecastData(foreJson.forecast || []);
      } catch (error) {
        console.error("Failed to fetch data:", error);
        setError(error.message || "Failed to fetch weather data.");
        setHistoricalData([]);
        setForecastData([]);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const data = [
    ...historicalData.map((point) => ({
      time: point.time,
      type: "Historical",
      temperature_historical: point.temperature_2m,
      humidity_historical: point.relative_humidity_2m,
      pressure_historical: point.surface_pressure,
      wind_historical: point.wind_speed_10m
    })),
    ...forecastData.map((point) => ({
      time: point.time,
      type: "Predicted",
      temperature_forecast: point.temperature_2m,
      humidity_forecast: point.relative_humidity_2m,
      pressure_forecast: point.surface_pressure,
      wind_forecast: point.wind_speed_10m
    }))
  ];

  const currentValues = historicalData.length > 0
    ? historicalData[historicalData.length - 1]
    : null;
  const firstForecast = forecastData.length > 0 ? forecastData[0] : null;
  const finalForecast = forecastData.length > 0 ? forecastData[forecastData.length - 1] : null;
  const forecastStartTime = firstForecast ? firstForecast.time : null;
  const forecastEndTime = finalForecast ? finalForecast.time : null;
  const forecastHorizonDays = (FORECAST_STEPS * RESAMPLE_HOURS) / 24;
  const lastObservedTime = currentValues ? format(parseISO(currentValues.time), 'MMM dd, HH:mm') : 'N/A';
  const firstForecastTime = firstForecast ? format(parseISO(firstForecast.time), 'MMM dd, HH:mm') : 'N/A';
  const finalForecastTime = finalForecast ? format(parseISO(finalForecast.time), 'MMM dd, HH:mm') : 'N/A';

  const chartSeries = {
    temperature: {
      historicalKey: "temperature_historical",
      forecastKey: "temperature_forecast",
      historicalName: "Historical Temperature",
      forecastName: "Predicted Temperature"
    },
    humidity: {
      historicalKey: "humidity_historical",
      forecastKey: "humidity_forecast",
      historicalName: "Historical Humidity",
      forecastName: "Predicted Humidity"
    },
    pressure: {
      historicalKey: "pressure_historical",
      forecastKey: "pressure_forecast",
      historicalName: "Historical Pressure",
      forecastName: "Predicted Pressure"
    },
    wind: {
      historicalKey: "wind_historical",
      forecastKey: "wind_forecast",
      historicalName: "Historical Wind",
      forecastName: "Predicted Wind"
    }
  };

  const predictionSteps = [
    {
      icon: Database,
      title: "Collect",
      text: `Fetches ${TRAINING_HISTORY_DAYS} days of hourly Mumbai weather: temperature, humidity, pressure, and wind.`
    },
    {
      icon: Activity,
      title: "Resample",
      text: `Groups hourly readings into ${RESAMPLE_HOURS}-hour averages to smooth noise and align the model interval.`
    },
    {
      icon: GitCompareArrows,
      title: "Difference",
      text: "Uses change-from-previous-step values so the VAR model learns movement instead of only absolute levels."
    },
    {
      icon: TrendingUp,
      title: "Forecast",
      text: `Fits VAR(${VAR_LAG_ORDER}), predicts ${FORECAST_STEPS} future steps, then adds predicted changes back to the latest observed values.`
    }
  ];

  const renderVariableChart = (key) => {
    const metric = metrics[key];
    const series = chartSeries[key];

    return (
      <section className="glass-panel variable-chart-card" key={key}>
        <div className="chart-heading compact">
          <div>
            <h2>{metric.name}</h2>
            <p>Historical observations and VAR predictions in {metric.unit}.</p>
          </div>
          <div className="chart-legend-key">
            <span><i className="solid-sample" /> Historical</span>
            <span><i className="dash-sample" /> Predicted</span>
          </div>
        </div>

        <div className="chart-container variable-chart-container">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data} margin={{ top: 20, right: 24, left: 8, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--glass-border)" vertical={false} />
              <XAxis
                dataKey="time"
                stroke="var(--text-secondary)"
                tickFormatter={(time) => format(parseISO(time), 'dd MMM')}
                minTickGap={26}
              />
              <YAxis
                yAxisId="value"
                stroke="var(--text-secondary)"
                tickFormatter={(value) => formatForecastValue(value, 0)}
              />
              <Tooltip content={<CustomTooltip />} />
              <Legend wrapperStyle={{ paddingTop: '14px' }} />

              {forecastStartTime && forecastEndTime && (
                <ReferenceArea
                  x1={forecastStartTime}
                  x2={forecastEndTime}
                  yAxisId="value"
                  fill="rgba(99, 102, 241, 0.08)"
                  strokeOpacity={0}
                />
              )}

              {forecastStartTime && (
                <ReferenceLine
                  x={forecastStartTime}
                  yAxisId="value"
                  stroke="var(--accent-color)"
                  strokeDasharray="3 3"
                  label={{ position: 'top', value: 'Forecast Start', fill: 'var(--accent-color)', fontSize: 12 }}
                />
              )}

              <Line
                yAxisId="value"
                type="monotone"
                dataKey={series.historicalKey}
                name={series.historicalName}
                stroke={metric.color}
                strokeWidth={2}
                dot={false}
                connectNulls={false}
                activeDot={{ r: 7 }}
              />
              <Line
                yAxisId="value"
                type="monotone"
                dataKey={series.forecastKey}
                name={series.forecastName}
                stroke={metric.color}
                strokeWidth={2.5}
                strokeDasharray="8 5"
                dot={{ r: 3 }}
                connectNulls={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </section>
    );
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1>Multivariate Forecast</h1>
        <p>AI-Powered Weather Predictions (VAR Model)</p>
      </header>

      {loading ? (
        <div style={{ textAlign: 'center', marginTop: '4rem', color: 'var(--accent-color)' }}>
          <Activity size={48} className="animate-pulse" style={{ margin: '0 auto', animation: 'pulse 2s infinite' }} />
          <p style={{ marginTop: '1rem', fontSize: '1.2rem' }}>Training VAR Model & Fetching Forecast...</p>
        </div>
      ) : (
        <>
          {error && (
            <div className="glass-panel" style={{ color: '#fca5a5', marginBottom: '1.5rem' }}>
              {error}
            </div>
          )}

          <section className="glass-panel prediction-panel">
            <div className="panel-heading">
              <div>
                <h2>How The Prediction Is Made</h2>
                <p>
                  The backend trains a Vector Autoregression model on recent multivariate weather changes, then extends the series forward in 6-hour steps.
                </p>
              </div>
              <div className="model-badge">VAR({VAR_LAG_ORDER})</div>
            </div>

            <div className="prediction-summary">
              <div>
                <span>Training window</span>
                <strong>{TRAINING_HISTORY_DAYS} days</strong>
              </div>
              <div>
                <span>Display history</span>
                <strong>{historicalData.length} points</strong>
              </div>
              <div>
                <span>Forecast horizon</span>
                <strong>{forecastHorizonDays} days</strong>
              </div>
              <div>
                <span>Last observed</span>
                <strong>{lastObservedTime}</strong>
              </div>
              <div>
                <span>First prediction</span>
                <strong>{firstForecastTime}</strong>
              </div>
            </div>

            <div className="prediction-steps">
              {predictionSteps.map(({ icon: Icon, title, text }) => (
                <div className="prediction-step" key={title}>
                  <div className="step-icon">
                    <Icon size={20} />
                  </div>
                  <h3>{title}</h3>
                  <p>{text}</p>
                </div>
              ))}
            </div>
          </section>

          <section className="charts-section">
            <div className="section-heading">
              <h2>Historical vs Predicted Graphs</h2>
              <p>Each variable is shown separately. Solid lines are historical observations, and dashed lines are future VAR predictions.</p>
            </div>
            <div className="variable-charts-grid">
              {Object.keys(metrics).map(renderVariableChart)}
            </div>
          </section>

          <p style={{ textAlign: 'center', margin: '1.5rem 0 2rem', color: 'var(--text-secondary)', fontSize: '0.85rem' }}>
            Showing {historicalData.length} historical points and {forecastData.length} predicted steps using Vector Autoregression (VAR).
          </p>

          <section className="glass-panel forecast-panel">
            <div className="panel-heading">
              <div>
                <h2>Future Predictions</h2>
                <p>
                  These are the actual VAR outputs returned by the backend for each future 6-hour interval.
                </p>
              </div>
              <div className="model-badge">{firstForecastTime} to {finalForecastTime}</div>
            </div>

            {firstForecast && (
              <div className="next-forecast-grid">
                <div>
                  <span>Next predicted time</span>
                  <strong>{firstForecastTime}</strong>
                </div>
                <div>
                  <span>Temperature</span>
                  <strong>{formatForecastValue(firstForecast.temperature_2m)} deg C</strong>
                </div>
                <div>
                  <span>Humidity</span>
                  <strong>{formatForecastValue(firstForecast.relative_humidity_2m, 0)}%</strong>
                </div>
                <div>
                  <span>Pressure</span>
                  <strong>{formatForecastValue(firstForecast.surface_pressure, 0)} hPa</strong>
                </div>
                <div>
                  <span>Wind</span>
                  <strong>{formatForecastValue(firstForecast.wind_speed_10m)} km/h</strong>
                </div>
              </div>
            )}

            <div className="forecast-table-wrap">
              <table className="forecast-table">
                <thead>
                  <tr>
                    <th>Step</th>
                    <th>Time</th>
                    <th>Temp</th>
                    <th>Humidity</th>
                    <th>Pressure</th>
                    <th>Wind</th>
                  </tr>
                </thead>
                <tbody>
                  {forecastData.map((point, index) => (
                    <tr key={point.time}>
                      <td>{index + 1}</td>
                      <td>{format(parseISO(point.time), 'MMM dd, HH:mm')}</td>
                      <td>{formatForecastValue(point.temperature_2m)} deg C</td>
                      <td>{formatForecastValue(point.relative_humidity_2m, 0)}%</td>
                      <td>{formatForecastValue(point.surface_pressure, 0)} hPa</td>
                      <td>{formatForecastValue(point.wind_speed_10m)} km/h</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        </>
      )}
    </div>
  );
}

export default App;
