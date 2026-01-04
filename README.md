# Tomoro Coffee Queue Simulation

This project simulates customer queues at Tomoro Coffee using the SimPy discrete-event simulation library. It compares two queue management scenarios: First-In-First-Out (FIFO) and priority-based queuing.

## Features

- Discrete-event simulation of coffee shop operations
- Two queue management scenarios
- Console-based simulation with summary reports
- Interactive web dashboard using Streamlit
- Data visualization with charts and metrics

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/jumat-berkah-is-me/Projek-Simulasi-Warung-Kopi.git
   cd Projek-Simulasi-Warung-Kopi
   ```

2. Install dependencies:
   ```
   pip install -e .
   ```

## Usage

### Web Dashboard

Launch the interactive dashboard:

```
streamlit run dashboard.py
```

Or, visit the hosted web dashboard:
```
https://simulasi-antrian-tomoro.streamlit.app/
```

The dashboard allows you to:
- Adjust simulation parameters (duration, arrival intervals, service times)
- Run simulations for both scenarios
- View comparative metrics and time-series charts
- Examine detailed customer data

## Simulation Scenarios

### Scenario A: FIFO (First-In-First-Out)
All customers are served in the order they arrive, regardless of order size or type.

### Scenario B: Priority-Based Queuing
- Walk-in customers (1-2 cups) receive high priority
- Online orders (3-8 cups) receive lower priority
- This prioritizes quick, small orders over larger online orders

## Configuration

Simulation parameters can be modified in `config.py`:
- `WAKTU_SIMULASI`: Total simulation time in minutes
- `INTERVAL_PELANGGAN`: Average time between customer arrivals
- `WAKTU_BUAT_PER_CUP`: Time to prepare one cup of coffee
- `JUMLAH_BARISTA`: Number of baristas available
- `RANDOM_SEED`: Random seed for reproducible results

## Project Structure

- `dashboard.py`: Streamlit web application
- `entities.py`: Simulation entities (TomoroCoffee class)
- `processes.py`: Customer arrival and service processes
- `config.py`: Configuration constants
- `pyproject.toml`: Project dependencies and metadata

## Dependencies

- simpy: Discrete-event simulation framework
- streamlit: Web app framework
- pandas: Data manipulation and analysis
- altair: Data visualization (used in dashboard)