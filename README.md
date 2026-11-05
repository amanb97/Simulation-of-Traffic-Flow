# Simulation of Traffic Flow

A cellular automaton simulates cars on a circular, single-lane road. At each time step cars accelerate, check the gap ahead, respond to random slowdowns and move. The experiments vary speed limits, slowdown frequency, traffic density and driver behaviour. The [project report](docs/traffic-flow-report.pdf) describes the model and the original results.

## Run a simulation

From this folder, run:

```bash
python -m pip install -r requirements.txt
python run_simulation.py
```

The example runs 20 cars on a 200-cell road for 100 steps. It prints the flow, density and journey-time statistic, and saves a time–position plot as `MultipleSecondPlot.png`.  The original driving modes are the strings `'False'`, `'Skill'`, `'Aggression'` and `'Skill and Aggression'`.

## Run an experiment

```bash
python experiments.py velocity --trials 5 --seed 43
```

| Experiment | What varies |
|---|---|
| `velocity` | Speed limit versus journey time |
| `events` | Slowdown frequency versus journey time |
| `multiple` | Slowdown frequency at five different speed limits |
| `density` | Traffic flow across densities for three driving modes |
| `peak` | Traffic flow over a finer range of 30–45 cars |

Each command displays its plot. `--trials` sets the runs per setting. Error bars show the standard deviation across trials. If any spread is zero, the script announces an unweighted fit. If a fit fails to converge, the simulation points still plot.

## Files

| File | Contents |
|---|---|
| `road.py` | Road initialisation, one-step movement rules, flow counter and journey-time check |
| `plotting.py` | Road snapshot, time–position plot and GIF animation |
| `run_simulation.py` | The original `simulate(...)` function and editable example |
| `experiments.py` | The five parameter sweeps and their fitted plots |

`simulate(...)` returns `(flowcount/time, number_cars/length, journeytime/number_cars)`
