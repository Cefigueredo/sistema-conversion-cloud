while !</dev/tcp/conversion_tool_db/5432;
do sleep 1;
done;
celery --app tasks.task.celery worker --loglevel=info -l  info & gunicorn -b 0.0.0.0:5000 app:app