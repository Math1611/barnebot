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