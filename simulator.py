#  Copyright (c) 2022. University of Memphis, mDOT Center
#
#  Redistribution and use in source and binary forms, with or without modification, are permitted
#  provided that the following conditions are met:
#
#  1. Redistributions of source code must retain the above copyright notice, this list of conditions
#  and the following disclaimer.
#
#  2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions
#  and the following disclaimer in the documentation and/or other materials provided with the distribution.
#
#  3. Neither the name of the copyright holder nor the names of its contributors may be used to
#  endorse or promote products derived from this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
#  IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
#  INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
#  NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
#  WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY
#  OF SUCH DAMAGE.

import argparse
import traceback
import pJITAI
from datetime import datetime
import json

from pJITAI.datatypes import DataVector

parser = argparse.ArgumentParser(description='Generate RL test data')
parser.add_argument('--server', default='http://localhost:5005/api')
parser.add_argument('--service_id', help='UUID')

# TODO: Remove the default once implemented on the server
parser.add_argument('--service_token', help='UUID',
                    default='e6e74d36-a3e4-4631-b077-4fdd703636f2')
args = parser.parse_args()

decision_responses = {}

# UPLOAD
def upload(row: dict):
    try:
        # temp = row.as_dict()
        # # print('row: ', row)
        # # temp['decision_id'] = decision_responses[row.user_id]
        # temp['decision_id'] = 1
        # temp['status_message'] = row.status_message
        # temp['status_code'] = row.status_code
        # # upload_result = session.upload(DataVector.from_dict(temp), session.model['configuration']['eligibility']) # TODO: Eligibility need to be retrieved and/or modified by the user.
        upload_result = session.upload(row) # TODO: Eligibility need to be retrieved and/or modified by the user.
        print(upload_result)
    except Exception as e:
        print(f'Upload Exception: {e}')
        traceback.print_exc()
        pass


# UPDATE
def update(row: dict):
    try:
        update_result = session.update(row)
        print(update_result)
    except Exception as e:
        print(f'Update Exception: {e}')
        traceback.print_exc()
        pass


# DECISION
def decision(row: dict):
    try:
        # decision_result = session.decision(row, session.model['configuration']['eligibility']) # TODO: Eligibility need to be retrieved and/or modified by the user.
        decision_result = session.decision(row) # TODO: Eligibility need to be retrieved and/or modified by the user.
        decision_responses[decision_result.decision_result['user_id']] = decision_result.decision_result['id']
        print(decision_result)
    except Exception as e:
        print(f'Decision Exception: {e}')
        traceback.print_exc()
        pass

def list_call(list_of_calls):
    try:
        for idx, c in enumerate(list_of_calls):
            type = c['type']
            content = c['content']
            if type == 'decision':
                result = session.decision(content)
            elif type == 'upload':
                result = session.upload(content)
            elif type == 'update':
                result = session.update(content)
            print(result)
    except Exception as e:
        print(f'Exception: {e}')
        traceback.print_exc()
        pass


allevents = []

def read_json_process_call():
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    list_call(data)
    # print(data)
    # print(type(data))
    return

def process_list_call():
    # Define JSON list of calls
    list_of_calls = [
        {'type': 'decision',
         'content': {
             'user_id': 1,
             'timestamp': str(datetime.now()),
             'state_data': {
                'Location_validation_status_code': ['SUCCESS'],
                'Location': 1, 
            }
         }},
        {'type': 'upload',
         'content': {
             "user_id": 1,
             "timestamp": str(datetime.now()),
             "proximal_outcome": 0.5,
             "proximal_outcome_timestamp": "2024-10-23T16:57:39Z",
             "decision_id": 3,
         }},
        {'type': 'update',
         'content': {
             'user_id': 1,
         }}
    ]

    # Call list_call()
    list_call(list_of_calls)
    return

def process_upload():
    # f = open('upload.csv')
    # i = 0
    # columns = None
    # for l in f:
    #     if i == 0:
    #         columns = l.strip().split(',')
    #     else:
    #         data = l.strip().split(',')
    #         row = {}
    #         row[columns[0]] = data[0]  # user id
    #         row[columns[1]] = data[1]  # timestamp
    #         timestamp = datetime.fromisoformat(data[1])
    #         row[columns[2]] = data[2]  # decision_timestamp
    #         row[columns[3]] = int(data[3])  # decision
    #         row[columns[4]] = data[4]  # proximal_outcome_timestamp
    #         row[columns[5]] = int(data[5])  # proximal_outcome
    #         values = []
    #         for idx in range(6, len(data)):
    #             val = {}
    #             val['name'] = columns[idx]
    #             val['value'] = float(data[idx])  # TODO FIXME - hack to make the demo work
    #             values.append(val)
    #         row['values'] = values
    #         row['decision_id'] = ""
    #         row.pop('decision')
    #         row.pop('decision_timestamp')
    #         rowdp = pJITAI.DataVector.from_dict(row)
    #         print(rowdp)
    #         event = (timestamp, 'upload', rowdp)
    #         allevents.append(event)

    #     i += 1
    # f.close()
    hs1_upload = {
        "user_id": 1,
        "timestamp": str(datetime.now()),
        "proximal_outcome": 0.5,
        "proximal_outcome_timestamp": "2024-10-23T16:57:39Z",
        "decision_id": 1,  # this will be used to connect with Decision table 
    }

    allevents.append(('upload', hs1_upload))
    return


def process_update():
    # f = open('update.csv')
    # i = 0
    # columns = None
    # for l in f:
    #     if i == 0:
    #         columns = l.strip().split(',')
    #         # print(columns)
    #     else:
    #         data = l.strip().split(',')
    #         # print(data)
    #         row = {}
    #         row[columns[0]] = data[0]  # user id
    #         timestamp = datetime.fromisoformat(data[0])

    #         event = (timestamp, 'update', row)
    #         allevents.append(event)

    #     i += 1

    # f.close()
    # Fake data to test upload
    user_id = 1

    row = {}
    row['user_id'] = user_id

    allevents.append(('update', row))
    return


def process_decision():
    # f = open('decision.csv')
    # i = 0
    # columns = None
    # for l in f:
    #     if i == 0:
    #         columns = l.strip().split(',')
    #     else:
    #         data = l.strip().split(',')
    #         row = {}
    #         row[columns[0]] = data[0]  # user id
    #         row[columns[1]] = data[1]  # timestamp
    #         timestamp = datetime.fromisoformat(data[1])
    #         values = []
    #         for idx in range(2, len(data)):
    #             val = {}
    #             val['name'] = columns[idx]
    #             val['value'] = float(data[idx])
    #             values.append(val)
    #         row['values'] = values
    #         rowdp = pJITAI.DecisionVector.from_dict(row)
    #         event = (timestamp, 'decision', rowdp)
    #         allevents.append(event)

    #     i += 1
    # f.close()

    hs1_state_data = { # state data, must match covariates? # Jane: Yes  # YS: These data should be attached from client session
        'Location_validation_status_code': ['SUCCESS'],
        'Location': 1, 
    }
    user_id = 1
    timestamp = str(datetime.now())

    row = {}
    row['user_id'] = user_id
    row['timestamp'] = timestamp
    row['state_data'] = hs1_state_data

    allevents.append(('decision', row))


if __name__ == '__main__':

    server = args.server
    service_id = args.service_id
    service_token = args.service_token

    session = pJITAI.Client(server, service_id, service_token)

    read_json_process_call()
    # process_list_call()

    # process_decision()
    # process_upload()
    # process_update()
    # print(f'All events = {len(allevents)}')

    # simulation
    # for event in allevents:
    #     if event[0] == 'upload':
    #         upload(event[1])
    #     elif event[0] == 'decision':
    #         decision(event[1])
    #     else:
    #         update(event[1])
        