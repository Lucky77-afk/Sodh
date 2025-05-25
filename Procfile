web: streamlit run streamlit_app.py \
  --server.port=$PORT \
  --server.address=0.0.0.0 \
  --server.enableCORS=true \
  --server.enableXsrfProtection=true \
  --server.maxUploadSize=200 \
  --server.enableWebsocketCompression=true

health: python -c "import os; print('Health check passed')"
