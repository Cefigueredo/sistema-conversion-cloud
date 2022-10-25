FROM python

RUN groupadd -r user && useradd -r -g user user
WORKDIR /app
ADD requirements.txt ./
RUN pip install -r requirements.txt
ADD . .
RUN chown -R user:user .
RUN ["chmod", "+x", "run_app.sh"]
USER user