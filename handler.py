import requests
import json

from topdesk import Topdesk as topdesk
from config import settings
from model import IncidentsModel

class BotApi:

    def __init__(self) -> None:
        self.username = settings.USER_BOT_API
        self.password = settings.PASSWORD_BOT_API 
        self.host = settings.URL_BOT_API
        self.token = self.get_token()
        self.header = {"Authorization": self.token}

    def get_token(self):
        url = f"{self.host}/api/login"
        payload = {
            "username": self.username,
            "password": self.password
        }
        result = requests.post(url=url, data=json.dumps(payload)).json()

        return result['token']
        
    def get_all_incidents(self) -> list[IncidentsModel]:
        url = f"{self.host}/api/all_incidents"
        
        result = requests.get(url=url, headers=self.header).json()

        list_incidents = []
        for incidents in result:
            list_incidents.append(IncidentsModel(
                cod_incident=incidents['cod_incident'], 
                last_update=incidents['last_update'],
                last_update_description=incidents['last_update_description'],
                status=incidents['status'],
                operator_name=incidents['operator_name'])
            )

        return list_incidents

    def update_incident(self, incident:IncidentsModel) -> requests.status_codes: 
        url = f"{self.host}/api/last_update_incident/{incident.cod_incident}"

        payload = { 
            "last_update_description": incident.last_update_description,
            "status": incident.status,
            "operator_name": incident.operator_name
        }

        result = requests.patch(url=url, headers=self.header, data=json.dumps(payload))

        return result.status_code
    
class TopDesk: 

    def __init__(self) -> None:
        self.username = settings.USER_TOP_DESK
        self.password = settings.PASSWORD_TOP_DESK
        self.host = settings.URL_TOP_DESK
        self.topdesk = topdesk(url=settings.URL_TOP_DESK, app_creds=(settings.USER_TOP_DESK, settings.PASSWORD_TOP_DESK))

    def get_actions(self, id_incident):
        url = f"{self.host}/tas/api/incidents/id/{id_incident}/actions"
        actions = requests.get(url=url, auth=(self.username, self.password))
        
        if actions.status_code == 200: 
            return actions.json()[0]['plainText']
        
        return None
    
    def get_incident(self, cod_incident) -> dict:
        try:
            incident_model = self.topdesk.incident(cod_incident+" ")
            action_by_incident = self.get_actions(incident_model['id'])

            return {
                "cod_incident":incident_model['number'],
                "operator_name":incident_model['operator']['name'], 
                "status":incident_model['processingStatus']['name'] if incident_model['processingStatus'] else "",
                "last_update_description":action_by_incident if action_by_incident else ""
            }

        except Exception as ex:
            return None