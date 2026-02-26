# Chatbot Municipal - Estado Actual

## Infraestructura
- Backend: FastAPI
- Hosting: Render
- DB: PostgreSQL interno Render
- WhatsApp: Cloud API Meta

## Funciona:
- Webhook recibe mensajes
- Extrae número y texto
- Envía respuesta automática
- Guarda mensajes en tabla `messages`

## Próximo paso:
- Lógica por palabras clave
- Manejo de flujos
- Estado del usuario


Estoy haciendo un chatbot municipal con FastAPI, PostgreSQL en Render y WhatsApp Cloud API.
Ya tengo el webhook funcionando y guardo mensajes en la tabla messages.
Ahora quiero continuar desde la parte de lógica conversacional.



MVC

BOT
|
|__database/
|       |_ __init__.py
|       |_ db.py
|
|__flows/
|    |_router.py
|
|__models/
|     |_ __init__.py
|     |_ message.py
|     |_ service.py
|     |_ user.py
|     |_ user_state.py
|     |_ section.py
|     |_ document.py
|     |_ document_chunk.py
|
|__routes/
|     |_webhook.py
|
|__services/
|      |__translations/
|      |        |__ __init__.py
|      |        |__ en.py
|      |        |__ es.py
|      |        |__ i18n.py
|      |_ __init__.py
|      |_ flow.py
|      |_ intent.py
|      |_ menus.py
|      |_ ai_service.py
|      |_ embedding_service.py
|      |_ rag_service.py
|      |_ service_search.py
|      |_ user_service.py
|      |_ weather_service.py
|      |_ weather.py
|      |_ whatsapp_service.py
|      |_ whatsapp.py
|
|_.gitignore
|_config.py
|_main.py
|_requirements.txt
