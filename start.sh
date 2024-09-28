MIGRATIONS_PATH="/alembic/versions"
DB_RUN_AUTO_MIGRATE=True

if [ "$DB_RUN_AUTO_MIGRATE" = "True" ]; then
  if [ -d "$MIGRATIONS_PATH" ] && [ "$(ls -A $MIGRATIONS_PATH)" ]; then
    echo "Running Alembic migrations..."
    alembic upgrade head
  else
    echo "No migration files found in $MIGRATIONS_PATH. Skipping migrations."
  fi
else
  echo "Skipping Alembic migrations due to DB_RUN_AUTO_MIGRATE flag."
fi

uvicorn app.main:app --host=0.0.0.0 --port $PORT --forwarded-allow-ips='*' --proxy-headers --log-level warning --use-colors