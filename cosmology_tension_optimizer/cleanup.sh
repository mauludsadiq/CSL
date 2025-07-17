#!/bin/bash

echo "🔨 Starting cleanup..."

# Create main package dir if missing
mkdir -p cosmology_tension_optimizer

# Move all relevant files into the package folder
mv cobaya_fr.yaml cosmology_tension_optimizer/cobaya_fr.yaml 2>/dev/null
mv my_likelihood.py cosmology_tension_optimizer/my_likelihood.py 2>/dev/null
mv optimizer.py cosmology_tension_optimizer/optimizer.py 2>/dev/null
mv pk_DR12CMASS_North_z0.57.txt cosmology_tension_optimizer/pk_DR12CMASS_North_z0.57.txt 2>/dev/null

# Move CAMB and MGCAMB folders if they exist
[ -d CAMB ] && mv CAMB cosmology_tension_optimizer/CAMB
[ -d MGCAMB ] && mv MGCAMB cosmology_tension_optimizer/MGCAMB

# Remove any duplicate or stray chains folders outside the main one
rm -rf chains

# Re-create main chains directory for Cobaya outputs
mkdir -p chains

# Keep setup scripts & params.ini in project root
echo "✅ Project directory organized successfully!"
tree -L 3
