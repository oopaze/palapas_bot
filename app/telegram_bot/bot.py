import os, time, json

from telegram.ext import Updater, CommandHandler
import requests as r

from app.src import settings


class Bot(Updater):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.actions = {
            "save_entrada": {
                "required_info": ["link"],
                "optional_info": ["valor"],
                "func": lambda x: print("execuntando save_entrada")
            }
        }
        
        self.dispatcher.add_handler(CommandHandler('nova', self.nova_entrada))
        self.dispatcher.add_handler(CommandHandler('pendencias', self.entradas_pendentes))
        self.dispatcher.add_handler(CommandHandler('deletar', self.deletar_entrada))

    
    def deletar_entrada(self, update, context):
        _id = context.args[0] 
        method = settings.API_ENDPOINTS["deletar_entrada"]['METHOD']
        url = settings.API_ENDPOINTS["deletar_entrada"]['URL'] + str(_id) + "/"

        response = getattr(r, method)(url)

        if response.status_code == 200:
            update.message.reply_text('Sua entrada foi deletada com sucesso')
        else:
            update.message.reply_text('Não foi possível deletar entrada, tente novamente.')


    def nova_entrada(self, update, context):
        link = context.args[0]
        valor = 5 

        if len(context.args) > 1:
            valor = context.args[1]

        user = update.message.from_user

        data = {
            "link": link,
            "valor": valor,
            "criador": f"{user.first_name} {user.last_name}"
        }
        
        method = settings.API_ENDPOINTS["create_entrada"]['METHOD']
        url = settings.API_ENDPOINTS["create_entrada"]['URL']

        response = getattr(r, method)(url, json=data)

        if response.status_code < 300:
            update.message.reply_text('Sua entrada foi criada com sucesso.')
        else:
            update.message.reply_text('Não foi possível criar entrada, tente novamente.')

    
    def entradas_pendentes(self, update, context):
        method = settings.API_ENDPOINTS["get_entradas"]['METHOD']
        url = settings.API_ENDPOINTS["get_entradas"]['URL']

        response = getattr(r, method)(url)

        entradas = response.json()

        if entradas:
            message = ''
            for entrada in entradas:

                link = entrada['link']
                _id = entrada['id']
                criador = entrada['criador']
                criado_em = entrada['criado_em'][:10]

                message += f"{_id} - {link} ({criador}) às {criado_em} - PENDENTE\n\n"
            
            update.message.reply_text(message)
            
        else:
            update.message.reply_text("Nenhuma entrada pendente")

        
   