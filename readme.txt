CARA RUN:

python -m uvicorn main_cnn:app --reload --host 10.0.40.105 --port 8080

BIAR TETEP RUNNING WALAU UDAH EXIT TERMINAL (linux only):
 nohup python -m uvicorn main_cnn:app --reload --host 10.0.40.105 --port 8080 &