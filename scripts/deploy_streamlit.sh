#!/bin/bash
set -e

cd streamlit_app
if [ "$GH_CI" = "true" ]; then
    LOCAL=false streamlit run app.py
else
    LOCAL=true streamlit run app.py
fi
