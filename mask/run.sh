#!/bin/bash
#SBATCH -J mask-recognition # nombre del job
#SBATCH -p investigacion # nombre de la particion 
#SBATCH -c 4  # numero de cpu cores a usar

module load python/3.7.7
python3.7 training.py
module unload python/3.7.7
