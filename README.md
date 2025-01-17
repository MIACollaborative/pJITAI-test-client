# mDOT pJITAI (Just-In-Time Adaptive Intervention) Client

## Build and release
Run this under ```src/pJITAI```.
```bash

bumpver update -p

python3 -m build

twine check dist/*
twine upload dist/*

```

## Main Call
Use simulatory.py to write code and make API calls. There are three API calls: decision, upload and update. When you run the command below in the terminal, it will connect to the server based on the code under simulator.py.

```bash
python simulator.py --service_id '<your project uuid>' --server '<base_url>/api' --service_token '<your token>'
```

## Decision
The decision call from a client allows the RL algorithm to make a decision for the intervention.

### Request 
```python
def process_decision():
  state_data = {  # mock data, must match project's covariate(s)
    'Location_validation_status_code': ['SUCCESS'],  
    'Location': 1,
  }
  user_id = 1 # mock data
  timestamp = str(datetime.now())

  row = {}
  row['user_id'] = user_id
  row['timestamp'] = timestamp
  row['state_data'] = state_data

  allevents.append(('decision', row))
```
### Response
When the call was made successfully, the terminal will print DecisionResponse. 
```bash
DecisionResponse(status_code='SUCCESS', status_message='Decision made successfully', user_id=1, timestamp='2025-01-07 11:23:36.675201', id=39, proj_uuid='85c562be-ab36-43b3-b4be-9152162b1555', state_data='{"Location_validation_status_code": ["SUCCESS"], "Location": 1}', decision=0, pi=0.1, random_number=0.104327)
```

## Upload
The upload call from a client allows the RL algorithm to upload data after making a decision.

### Request
```python
def process_upload():
  upload_data = {
    "user_id": 1,  # mock data
    "timestamp": str(datetime.now()),
    "proximal_outcome": 0.5,  # mock data
    "proximal_outcome_timestamp": "2024-10-23T16:57:39Z",  # mock data
    "decision_id": 39,  # mock data
  }

  allevents.append(('upload', upload_data))
```
### Response
When the call was made successfully, the terminal will print UploadResponse. 
```bash
UploadResponse(status_code='SUCCESS', status_message='Data uploaded to model \'85c562be-ab36-43b3-b4be-9152162b1555', data={'decision_id': 39, 'id': 16, 'proj_uuid': '85c562be-ab36-43b3-b4be-9152162b1555', 'proximal_outcome': 0.5, 'proximal_outcome_timestamp': '2024-10-23T16:57:39Z', 'timestamp': '2025-01-07 11:23:36.675213', 'user_id': 1})
```

## Update
The update call from a client allows the RL algorithm to update its parameters.

### Request
```python
def process_update():
  user_id = 1  # mock data

  row = {}
  row['user_id'] = user_id

  allevents.append(('update', row))
```
### Response
When the call was made successfully, the terminal will print UpdateResponse. 
```bash
UpdateResponse(status_code='SUCCESS', status_message='Update has been made successfully.', update_result={'degree': 5.0, 'id': 5, 'proj_uuid': '85c562be-ab36-43b3-b4be-9152162b1555', 'scale': [[0.0]], 'theta_Sigma': [[0.15, 0.14999999999999997, 0.0, 0.0, 0.0, 0.0], [0.15, 0.7499999999999999, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.028607194359878133, 0.028607194359878133, 0.0, 0.0], [0.0, 0.0, 0.028607194359878133, 0.02890161833039568, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.028607194359878133, 0.028607194359878133], [0.0, 0.0, 0.0, 0.0, 0.028607194359878133, 0.02890161833039568]], 'theta_mu': [[-6.162975822039155e-33], [1.1102230246251563e-16], [-0.03797468354430311], [-0.021864211737628647], [-0.03797468354430304], [-0.021864211737628692]], 'timestamp': '2025-01-07 11:23:36.759070', 'user_id': 1})
```
