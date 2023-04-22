# IA API

## Introduction

This is a simple API to wrap IA models.

## Installation

```bash
git clone https://github.com/ESIR2-PROJET-KEOLIS/IA_API.git
```

## Usage

```bash
python3 main.py
```

## Documentation

### API

#### GET /predict/Nombus='Nombus'&Sens='Sens'

Return the prediction of the bus Nombus in the direction Sens.

see [example](testRequette.py)

## Model creation
For the creation of the model we used the data collected for another project. You can see the model creation process on the following [github](https://github.com/lumi-git/ProjetDataEngineering).
```
https://github.com/lumi-git/ProjetDataEngineering
```
### Model
```
Input:
Number of buses on the line
Average delay of buses (s)
Length of the line (m)
Average distance between buses on a line (m)

Output:
Low level (%)
Medium level (%)
High level (%)

NB : Low level + Medium level + High level = 100%
```
