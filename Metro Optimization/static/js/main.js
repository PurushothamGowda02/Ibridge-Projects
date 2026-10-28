document.addEventListener('DOMContentLoaded', () => {
    // Initialize Clock
    const updateClock = () => {
        const clockEl = document.getElementById('clock');
        if (clockEl) {
            const now = new Date();
            clockEl.textContent = now.toLocaleTimeString();
        }
    };
    setInterval(updateClock, 1000);
    updateClock();

    let demandChart = null;

    // Fetch and update Real-time stats
    const fetchRealtimeStats = async () => {
        try {
            const response = await fetch('/api/stats/realtime');
            const data = await response.json();
            
            // Update System Status
            const statusBadge = document.getElementById('system-status-badge');
            if (statusBadge) {
                if (data.system_status === 'Normal') {
                    statusBadge.className = 'system-status normal';
                    statusBadge.innerHTML = '<i class="fa-solid fa-circle-check"></i> System Normal';
                } else {
                    statusBadge.className = 'system-status warning';
                    statusBadge.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i> System Delayed';
                }
            }

            // Update KPI Cards — API returns data.lines with passengers per line
            let totalPassengers = 0;
            if (data.lines) {
                data.lines.forEach(line => {
                    totalPassengers += line.passengers || 0;
                });
            }

            const kpiPassengers = document.getElementById('kpi-passengers');
            const kpiTrains = document.getElementById('kpi-trains');
            const kpiEnergy = document.getElementById('kpi-energy');
            const kpiEnergySavings = document.getElementById('kpi-energy-savings');
            const kpiFare = document.getElementById('kpi-fare');
            const kpiHealth = document.getElementById('kpi-health');
            const kpiSeats = document.getElementById('kpi-seats');
            
            if (kpiPassengers) kpiPassengers.textContent = totalPassengers;
            if (kpiTrains) {
                // If the app returned active_trains, use it, otherwise mock 42
                kpiTrains.textContent = data.active_trains !== undefined ? data.active_trains : 42;
            }
            if (kpiEnergy) {
                kpiEnergy.textContent = (data.energy_mwh !== undefined ? data.energy_mwh : '--') + ' MWh';
            }
            if (kpiEnergySavings) {
                kpiEnergySavings.textContent = (data.energy_saved_pct !== undefined ? data.energy_saved_pct : '--') + '% saved';
            }
            if (kpiFare && data.current_fare) kpiFare.textContent = '$' + data.current_fare.toFixed(2);
            if (kpiHealth && data.fleet_health) kpiHealth.textContent = data.fleet_health.toFixed(1) + '%';
            if (kpiSeats && data.available_seats !== undefined) kpiSeats.textContent = data.available_seats;
            
        } catch (error) {
            console.error("Error fetching real-time stats:", error);
        }
    };

    // Fetch predictions and update UI
    const fetchPredictions = async () => {
        try {
            const response = await fetch('/api/forecast/demand');
            const data = await response.json();

            if (data.error) {
                console.error("Prediction API Error:", data.error);
                return;
            }

            const predictions = data.predictions;
            try {
                updateChart(predictions);
            } catch (err) {
                console.error("Failed to update chart:", err);
            }
            try {
                updateScheduleTable(predictions);
            } catch (err) {
                console.error("Failed to update table:", err);
            }

        } catch (error) {
            console.error("Error fetching predictions:", error);
        }
    };

    const fetchSettings = async () => {
        try {
            const response = await fetch('/api/settings');
            const data = await response.json();
            
            const baseTrainsEl = document.getElementById('setting-base-trains');
            const maxCapacityEl = document.getElementById('setting-max-capacity');
            
            if (baseTrainsEl) baseTrainsEl.value = data.base_trains;
            if (maxCapacityEl) maxCapacityEl.value = data.max_capacity;
            
        } catch (error) {
            console.error("Error fetching settings:", error);
        }
    };

    const saveSettingsTrigger = document.getElementById('save-settings-btn');
    if (saveSettingsTrigger) {
        saveSettingsTrigger.addEventListener('click', async () => {
            const baseTrains = document.getElementById('setting-base-trains').value;
            const maxCapacity = document.getElementById('setting-max-capacity').value;
            
            try {
                const response = await fetch('/api/settings', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        base_trains: baseTrains,
                        max_capacity: maxCapacity
                    })
                });
                
                if (response.ok) {
                    const msgEl = document.getElementById('settings-message');
                    msgEl.style.display = 'block';
                    setTimeout(() => {
                        msgEl.style.display = 'none';
                    }, 3000);
                    
                    // Re-fetch predictions to update tables globally
                    fetchPredictions();
                }
            } catch (error) {
                console.error("Error saving settings:", error);
            }
        });
    }

    const updateChart = (data) => {
        const chartEl = document.getElementById('demandChart');
        if (!chartEl) return;
        
        const ctx = chartEl.getContext('2d');
        const labels = data.map(d => d.time);
        const values = data.map(d => d.predicted_demand);

        if (demandChart) {
            demandChart.data.labels = labels;
            demandChart.data.datasets[0].data = values;
            demandChart.update();
            return;
        }

        // Create fluid gradient for line chart
        const gradient = ctx.createLinearGradient(0, 0, 0, 400);
        gradient.addColorStop(0, 'rgba(59, 130, 246, 0.5)');   
        gradient.addColorStop(1, 'rgba(59, 130, 246, 0.0)');

        demandChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Predicted Demand',
                    data: values,
                    borderColor: '#3b82f6',
                    backgroundColor: gradient,
                    borderWidth: 3,
                    tension: 0.4,
                    fill: true,
                    pointBackgroundColor: '#8b5cf6',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 4,
                    pointHoverRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: '#1e293b',
                        titleColor: '#f8fafc',
                        bodyColor: '#cbd5e1',
                        borderColor: '#334155',
                        borderWidth: 1,
                        padding: 10,
                        displayColors: false,
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: '#334155',
                            drawBorder: false
                        },
                        ticks: {
                            color: '#94a3b8'
                        }
                    },
                    x: {
                        grid: {
                            display: false,
                            drawBorder: false
                        },
                        ticks: {
                            color: '#94a3b8'
                        }
                    }
                },
                animation: {
                    duration: 1000,
                    easing: 'easeOutQuart'
                }
            }
        });
    };

    const updateScheduleTable = (data) => {
        const tbody = document.getElementById('schedule-body');
        if (!tbody) return;
        
        tbody.innerHTML = ''; // Clear existing

        data.forEach(item => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><strong>${item.time}</strong></td>
                <td>${item.predicted_demand}</td>
                <td><span class="badge" style="background:var(--accent-primary);color:white">${item.trains_scheduled}</span></td>
                <td>${item.frequency_minutes}</td>
            `;
            tbody.appendChild(tr);
        });
    };

    const fetchTrainPositions = async () => {
        const layer = document.getElementById('trains-layer');
        if (!layer) return; // Not on map page

        try {
            const response = await fetch('/api/trains/positions');
            const data = await response.json();
            
            layer.innerHTML = ''; // clear trains
            data.trains.forEach(train => {
                const el = document.createElement('div');
                let cssColor = train.namma_line ? train.namma_line.toLowerCase() : '';
                el.className = `train-marker ${cssColor} ` + (train.health_status === 'Warning' ? 'warning' : '');
                
                // Add tooltip for driverless specifically
                if (train.is_driverless) {
                    el.innerHTML = '<span class="driverless-label" style="position: absolute; top: -20px; left: -10px; font-size: 10px; background: #fff; color: #000; padding: 2px 4px; border-radius: 4px; font-weight: bold; white-space: nowrap;">🤖 Auto</span>';
                }

                // position from 0 to 4 maps to 10% to 90% (80% total span, 20% per unit)
                const leftPct = 10 + (train.position * 20);
                el.style.left = leftPct + '%';
                
                layer.appendChild(el);
            });
        } catch(e) {
            console.error("Error fetching map:", e);
        }
    };

    let toastQueue = false;
    const showToast = (message) => {
        const container = document.getElementById('toast-container');
        if (!container || toastQueue) return;
        
        toastQueue = true;
        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.innerHTML = `<span>${message}</span>`;
        container.appendChild(toast);
        
        setTimeout(() => {
            toast.remove();
            toastQueue = false;
        }, 5000);
    };

    // Initial fetch
    fetchRealtimeStats();
    fetchPredictions();
    fetchSettings();
    fetchTrainPositions();

    // Setup polling every 30 seconds for real-time stats
    setInterval(fetchRealtimeStats, 30000);
    setInterval(fetchTrainPositions, 1000); // 1 second for live map 
});
