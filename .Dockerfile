FROM python:3.12.6-bookworm

WORKDIR /root/code

RUN pip3 install flask
RUN pip3 install pandas
RUN pip3 install seaborn
RUN pip3 install numpy
RUN pip3 install scikit-learn
RUN pip3 install matplotlib
RUN pip3 install xgboost 
RUN pip3 install joblib
RUN pip3 install imbalanced-learn


COPY ./code /root/code

CMD ["python", "app.py"]