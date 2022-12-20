echo "Waiting for postgres..."

while ! nc -z db "$POSTGRES_DEV_PORT"; do
  sleep 0.1
done

echo "PostgreSQL started"

echo "Rolling migrations..."

cd backend || exit
alembic upgrade head
cd ..

echo "Done"

exec "$@"