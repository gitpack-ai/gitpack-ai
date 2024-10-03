#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files
#python gitpack/manage.py collectstatic --no-input

# Apply any outstanding database migrations
python gitpack/manage.py migrate