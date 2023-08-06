# DuoChat

# DuoChat

Chatting app using Django Channels and WebSockets with encryption support via SSL.

### Installation (staging/testing) :whale:
Change .env.staging, .env.staging.db, .env.staging.proxy-companion according to your needs.


    git clone https://github.com/atheless/DuoChat.git
    cd DuoChat
    docker compose up -f docker-compose.staging.yml up -d --build
    sudo docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
    sudo docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear
    docker compose up -f docker-compose.staging.yml down -v
### Installation (production) :whale:
Change .env.prod, .env.prod.db, .env.prod.proxy-companion according to your needs.

N.B: VIRTUAL_HOST,LETSENCRYPT_HOST should match your domain name not an IP address.

For SECRET_KEY use:
from django.core.management.utils import get_random_secret_key get_random_secret_key()

    
    git clone https://github.com/atheless/DuoChat.git
    cd DuoChat
    docker compose up -f docker-compose.prod.yml up -d --build
    sudo docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
    sudo docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear
Check for generated cerficates:

    docker compose -f docker-compose.prod.yml exec nginx-proxy ls /etc/nginx/cert/
Shutdown: 

    docker compose up -f docker-compose.staging.yml down



### Video (old)
https://github.com/atheless/DuoChat/assets/86173165/0ac8e141-7956-433b-a7f5-a806439dcc2f



### List of implemented features:
- All WebSocket messages are secured via SSL and automatically encrypted  (wss://)
- User Registration/Authentication: To access the application, users must register and authenticate by providing their credentials.
- User Search: Users can search for other users of the application and invite them to start a conversation.
- Recent Contacts List: The application keeps track of users with whom recent conversations have taken place, making it easier to initiate new conversations.
- Emojis & GIFs: The application supports the use of emojis and GIFs to enrich conversations.
- Unique Conversation Identifier (UUID4): Each conversation between two users has a unique identifier, ensuring the security and isolation of conversations between users.
- Presence (online status in memory caching, typing indicator): Users can see the online status of other users and receive indications of real-time text typing.
- Message History: The application keeps track of all messages sent and received in a conversation, allowing users to review the conversation history.
- Last User Access: Users can see the last access time of other application users.
- Front-end UI elements (avatars, auto-scrolling, auto words-wrap, animated background): The user interface is enriched with elements such as avatars, automatic scrolling, automatic word wrapping, and an animated background.
- Asynchronous Consumer: The back-end utilizes an asynchronous consumer to handle real-time communication between clients and the server.
- Redis Channel Layer Back-end (channel and group management): The application uses Redis as a back-end to manage communication channels and groups.
- DOMPurify: The application protects users from XSS-stored and reflected attacks by sanitizing sent/received messages.


### Future Developments:
- Improve UI/UX
- Read receipts for messages (two blue ticks)
- Enhanced authentication (Multi-factor authentication)
- Support for group and private chats
- Better caching methods for online status
...
