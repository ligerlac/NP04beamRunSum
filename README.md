## Welcome to NP04beamRunSum
### Table of contents
* [Introduction](#introduction) 
* [Setup](#setup)
* [Usage](#usage)

### Introduction
NP04beamRunSum examines data from the Detector Control System
Database (DCS-DB, formerly known as Slow Controls Archive) in
search for periods of unstable high voltage. The time-indexed
values from a voltage and a current sensor are considered to
derive the time-dependent resistance. Hard cuts are applied
to this resistance to derive 'streamers' (periods of unstable
HV) as the final result. Everything is summarized in on large
plot.

### Setup
If not already existing, create a virtual environment
```
$ python -m venv venv/
```
Activate it
```
$ . venv/bin/activate
```
Install requirements
```
$ pip install requirements.txt
```

### Usage
Make plot of sensor output and averages
```
$ python src/make_heinz_plot.py
```
Make summary plot and derive periods of unstable HV
('streamers')
```
$ python src/make_summary_plot.py
```

### Further Documentation
