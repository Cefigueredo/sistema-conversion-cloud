while !</dev/tcp/conversion_toolDB/5432;
do sleep 1;
done;
celery --app tasks.task.celery worker --loglevel=info -l  info & gunicorn -b 0.0.0.0:8000 app:app