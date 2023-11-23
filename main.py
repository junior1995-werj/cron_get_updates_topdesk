from handler import BotApi, TopDesk

def controller(): 
    bot = BotApi()
    topdesk = TopDesk()
    list_incidents = bot.get_all_incidents()

    if list_incidents != []:
        for incident in list_incidents:
            dict_topdesk_incident =  topdesk.get_incident(cod_incident=incident.cod_incident)
            if dict_topdesk_incident:
                if (dict_topdesk_incident['operator_name'] == incident.operator_name or 
                    dict_topdesk_incident['status'] == incident.status or
                    incident.last_update_description == dict_topdesk_incident['last_update_description']):
                        print(f"{incident.cod_incident} -> Nao atualizado")
                else: 
                        incident.operator_name = dict_topdesk_incident['operator_name']
                        incident.status = dict_topdesk_incident['status']
                        incident.last_update_description = dict_topdesk_incident['last_update_description']
                        status_code = bot.update_incident(incident)

                        if status_code == 200: 
                            print(f"{incident.cod_incident} -> Atualizado")
                        else: 
                            print(f"{incident.cod_incident} -> status code: {status_code} -> Nao atualizado")
            else: 
                 print(f"{incident.cod_incident} -> Nao encontrado")
    else: 
        print(f"Sem chamados para atualizar!")
    
    print(f"Fim execucao!")

if __name__ == "__main__": 
    controller()
