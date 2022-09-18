from opentele.td import TDesktop
from opentele.tl import TelegramClient
from opentele.api import API, UseCurrentSession, CreateNewSession

import asyncio
import os
import json

path_to_acc = os.path.join(os.getcwd(), 'accounts')


async def main(path=path_to_acc):
    proccesed_files = list()

    for session in os.listdir(path):
        if session not in proccesed_files and session.endswith('.session'):
            proccesed_files.append(session)

        for script_object in os.listdir(path):
            if script_object not in proccesed_files and script_object.endswith('.json') and session.replace('.session', '') == script_object.replace('.json', ''):
                proccesed_files.append(script_object)
                
                path_to_json = os.path.join(os.getcwd(), 'accounts', script_object)
                path_to_session = os.path.join(os.getcwd(), 'accounts', session)

                with open(path_to_json, 'r') as json_doc:
                    data = json.load(json_doc)
                    path_to_tdata = os.path.join(os.getcwd(), 'tdata', f'{data["phone"]}')
                    

                    client = TelegramClient(session=path_to_session, api_hash=data['app_hash'], api_id=data['app_id'])
                    await client.connect()
                    print(await client.get_me())

                    api = API.TelegramIOS.Generate()
                    tdesk = await client.ToTDesktop(flag=UseCurrentSession, password=data['twoFA'], api=api)

                    await asyncio.sleep(2)
                    tdesk.SaveTData(basePath=path_to_tdata)
                    await client.PrintSessions()

asyncio.run(main())