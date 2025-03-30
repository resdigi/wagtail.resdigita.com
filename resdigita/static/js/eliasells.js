let userName = '';
let step = 0; // Rastrea el progreso de las preguntas
let isChatInitialized = false; // Controla si la conversación ya fue inicializada

function toggleChat() {
    const chatbot = document.getElementById('chatbot');
    chatbot.classList.toggle('hidden');

    if (!chatbot.classList.contains('hidden') && !isChatInitialized) {
        iniciarChat();
        isChatInitialized = true; // La conversación solo se inicializa una vez
    }
}

function iniciarChat() {
    const chatContent = document.getElementById('chat-content');
    const userInput = document.getElementById('user-input');

    // Detectar ENTER para enviar el mensaje
    userInput.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            handleUserInput();
        }
    });

    // Mensaje de bienvenida con ícono
    addMessage('Robotin', '¡Hola! Bienvenido a nuestro chatbot.', 'bot');

    setTimeout(() => {
        addMessage('Robotin', '¿Cómo te llamas?', 'bot');
    }, 1000);
}

function handleUserInput() {
    const userInput = document.getElementById('user-input');
    const message = userInput.value.trim();

    if (message !== '') {
        // Agrega mensaje del usuario
        addMessage('YO', message, 'user');
        userInput.value = '';

        // Simula animación de escritura antes de responder
        showTypingIndicator();

        setTimeout(() => {
            let botMessage = '';

            if (step === 0) {
                userName = message;
                botMessage = `¡Hola, ${userName}! ¿Cuántos años tienes?`;
                step++;
            } else if (step === 1) {
                botMessage = `¡Genial! ¿A qué te dedicas, ${userName}?`;
                step++;
            } else if (step === 2) {
                botMessage = `¡Interesante! ¿Qué comiste hoy?`;
                step++;
            } else if (step === 3) {
                botMessage = `Gracias por compartir, ${userName}. Esto puede interesarte:`;
                hideTypingIndicator();
                addMessage('Robotin', botMessage, 'bot');

                // Envia el mensaje con enlace
                setTimeout(() => {
                    sendLinkMessage(
                        'https://ejemplo.com',
                        'Súper promoción',
                        [
                            '25% de descuento reservando online.',
                            'Descuento aplica para servicios adicionales contratados.',
                        ],
                        'VER MÁS'
                    );
                }, 1000);
                return; // Salir aquí para que no agregue más mensajes después
            }

            hideTypingIndicator();
            addMessage('Robotin', botMessage, 'bot');
        }, 1500); // Tiempo de respuesta tras la animación de escritura
    }
}

function addMessage(sender, text, type) {
    const chatContent = document.getElementById('chat-content');
    const lastMessageContainer = chatContent.lastElementChild;
    const isSameSender =
        lastMessageContainer && lastMessageContainer.classList.contains(type);

    const messageContainer = document.createElement('div');
    messageContainer.className = `message-container ${type}`;
    if (isSameSender) {
        messageContainer.classList.add('hide-sender'); // Ocultar el emisor si es el mismo
    }

    if (!isSameSender) {
        const senderRow = document.createElement('div');
        senderRow.className = 'sender-row';

        if (sender === 'Robotin') {
            const senderIcon = document.createElement('span');
            senderIcon.className = 'sender-icon';
            senderIcon.innerHTML = `
            <svg width="16" height="16" viewBox="0 0 128 128" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" role="img" class="iconify iconify--noto" preserveAspectRatio="xMidYMid meet">

<path d="M12.53 53.05c-4.57.01-8.28 3.72-8.28 8.29v38.38a8.297 8.297 0 0 0 8.28 8.28h5.55V53l-5.55.05z" fill="#c62828">

</path>

<path d="M115.72 53.05c4.57.01 8.28 3.72 8.28 8.29v38.38c-.01 4.57-3.71 8.28-8.28 8.29h-5.55v-55l5.55.04z" fill="#c62828">

</path>

<path d="M113.17 54.41l-.12-10c-.03-4.3-3.53-7.77-7.83-7.75H67.05V23.25c5.11-1.69 7.89-7.2 6.2-12.31c-1.69-5.11-7.2-7.89-12.31-6.2s-7.89 7.2-6.2 12.31a9.743 9.743 0 0 0 6.2 6.2v13.46H22.78c-4.28.01-7.75 3.47-7.78 7.75v71.78c.03 4.28 3.5 7.74 7.78 7.76h82.44c4.3.01 7.8-3.46 7.83-7.76v-7.37h.12V54.41z" fill="#90a4ae">

</path>

<path d="M64 18c-2.21 0-4-1.79-4-4s1.79-4 4-4s4 1.79 4 4s-1.79 4-4 4z" fill="#c62828">

</path>

<g>

<linearGradient id="IconifyId17ecdb2904d178eab19904" gradientUnits="userSpaceOnUse" x1="64.005" y1="22.44" x2="64.005" y2="35.55" gradientTransform="matrix(1 0 0 -1 0 130)">

<stop offset=".12" stop-color="#e0e0e0">

</stop>

<stop offset=".52" stop-color="#ffffff">

</stop>

<stop offset="1" stop-color="#eaeaea">

</stop>

</linearGradient>

<path d="M44.15 94.45h39.71c3.46 0 6.27 2.81 6.27 6.27v.57c0 3.46-2.81 6.27-6.27 6.27H44.15c-3.46 0-6.27-2.81-6.27-6.27v-.57c0-3.46 2.81-6.27 6.27-6.27z" fill="url(#IconifyId17ecdb2904d178eab19904)">

</path>

<linearGradient id="IconifyId17ecdb2904d178eab19905" gradientUnits="userSpaceOnUse" x1="54.85" y1="22.44" x2="54.85" y2="35.53" gradientTransform="matrix(1 0 0 -1 0 130)">

<stop offset="0" stop-color="#333">

</stop>

<stop offset=".55" stop-color="#666">

</stop>

<stop offset="1" stop-color="#333">

</stop>

</linearGradient>

<path fill="url(#IconifyId17ecdb2904d178eab19905)" d="M53.67 94.47h2.36v13.09h-2.36z">

</path>

<linearGradient id="IconifyId17ecdb2904d178eab19906" gradientUnits="userSpaceOnUse" x1="64.06" y1="22.44" x2="64.06" y2="35.53" gradientTransform="matrix(1 0 0 -1 0 130)">

<stop offset="0" stop-color="#333">

</stop>

<stop offset=".55" stop-color="#666">

</stop>

<stop offset="1" stop-color="#333">

</stop>

</linearGradient>

<path fill="url(#IconifyId17ecdb2904d178eab19906)" d="M62.88 94.47h2.36v13.09h-2.36z">

</path>

<linearGradient id="IconifyId17ecdb2904d178eab19907" gradientUnits="userSpaceOnUse" x1="73.15" y1="22.44" x2="73.15" y2="35.53" gradientTransform="matrix(1 0 0 -1 0 130)">

<stop offset="0" stop-color="#333">

</stop>

<stop offset=".55" stop-color="#666">

</stop>

<stop offset="1" stop-color="#333">

</stop>

</linearGradient>

<path fill="url(#IconifyId17ecdb2904d178eab19907)" d="M71.97 94.47h2.36v13.09h-2.36z">

</path>

<linearGradient id="IconifyId17ecdb2904d178eab19908" gradientUnits="userSpaceOnUse" x1="82.8" y1="22.44" x2="82.8" y2="35.53" gradientTransform="matrix(1 0 0 -1 0 130)">

<stop offset="0" stop-color="#333">

</stop>

<stop offset=".55" stop-color="#666">

</stop>

<stop offset="1" stop-color="#333">

</stop>

</linearGradient>

<path fill="url(#IconifyId17ecdb2904d178eab19908)" d="M81.62 94.47h2.36v13.09h-2.36z">

</path>

<linearGradient id="IconifyId17ecdb2904d178eab19909" gradientUnits="userSpaceOnUse" x1="45.2" y1="22.46" x2="45.2" y2="35.55" gradientTransform="matrix(1 0 0 -1 0 130)">

<stop offset="0" stop-color="#333">

</stop>

<stop offset=".55" stop-color="#666">

</stop>

<stop offset="1" stop-color="#333">

</stop>

</linearGradient>

<path fill="url(#IconifyId17ecdb2904d178eab19909)" d="M44.02 94.45h2.36v13.09h-2.36z">

</path>

<g>

<path d="M64 85.33h-5.33c-.55 0-1-.45-1-1c0-.16.04-.31.11-.45l2.74-5.41l2.59-4.78a.996.996 0 0 1 1.76 0l2.61 5l2.71 5.19c.25.49.06 1.09-.43 1.35c-.14.07-.29.11-.45.11L64 85.33z" fill="#c62828">

</path>

</g>

<g>

<radialGradient id="IconifyId17ecdb2904d178eab19910" cx="42.64" cy="63.19" r="11.5" gradientTransform="matrix(1 0 0 -1 0 130)" gradientUnits="userSpaceOnUse">

<stop offset=".48" stop-color="#ffffff">

</stop>

<stop offset=".77" stop-color="#fdfdfd">

</stop>

<stop offset=".88" stop-color="#f6f6f6">

</stop>

<stop offset=".96" stop-color="#ebebeb">

</stop>

<stop offset="1" stop-color="#e0e0e0">

</stop>

</radialGradient>

<circle cx="42.64" cy="66.81" r="11.5" fill="url(#IconifyId17ecdb2904d178eab19910)">

</circle>

<linearGradient id="IconifyId17ecdb2904d178eab19911" gradientUnits="userSpaceOnUse" x1="30.14" y1="63.19" x2="55.14" y2="63.19" gradientTransform="matrix(1 0 0 -1 0 130)">

<stop offset="0" stop-color="#333">

</stop>

<stop offset=".55" stop-color="#666">

</stop>

<stop offset="1" stop-color="#333">

</stop>

</linearGradient>

<circle cx="42.64" cy="66.81" r="11.5" fill="none" stroke="url(#IconifyId17ecdb2904d178eab19911)" stroke-width="2" stroke-miterlimit="10">

</circle>

<radialGradient id="IconifyId17ecdb2904d178eab19912" cx="84.95" cy="63.22" r="11.5" gradientTransform="matrix(1 0 0 -1 0 130)" gradientUnits="userSpaceOnUse">

<stop offset=".48" stop-color="#ffffff">

</stop>

<stop offset=".77" stop-color="#fdfdfd">

</stop>

<stop offset=".88" stop-color="#f6f6f6">

</stop>

<stop offset=".96" stop-color="#ebebeb">

</stop>

<stop offset="1" stop-color="#e0e0e0">

</stop>

</radialGradient>

<path d="M85 55.28c-6.35 0-11.5 5.15-11.5 11.5s5.15 11.5 11.5 11.5s11.5-5.15 11.5-11.5c-.01-6.35-5.15-11.49-11.5-11.5z" fill="url(#IconifyId17ecdb2904d178eab19912)">

</path>

<linearGradient id="IconifyId17ecdb2904d178eab19913" gradientUnits="userSpaceOnUse" x1="72.45" y1="63.22" x2="97.45" y2="63.22" gradientTransform="matrix(1 0 0 -1 0 130)">

<stop offset="0" stop-color="#333">

</stop>

<stop offset=".55" stop-color="#666">

</stop>

<stop offset="1" stop-color="#333">

</stop>

</linearGradient>

<path d="M85 55.28c-6.35 0-11.5 5.15-11.5 11.5s5.15 11.5 11.5 11.5s11.5-5.15 11.5-11.5h0c-.01-6.35-5.15-11.49-11.5-11.5z" fill="none" stroke="url(#IconifyId17ecdb2904d178eab19913)" stroke-width="2" stroke-miterlimit="10">

</path>

</g>

</g>

</svg>`;
            senderRow.appendChild(senderIcon);
        }

        const senderLabel = document.createElement('span');
        senderLabel.className = 'sender';
        senderLabel.textContent = sender;
        senderRow.appendChild(senderLabel);

        messageContainer.appendChild(senderRow);
    }

    const message = document.createElement('div');
    message.className = `message ${type}`;
    message.textContent = text;

    messageContainer.appendChild(message);
    chatContent.appendChild(messageContainer);

    chatContent.scrollTop = chatContent.scrollHeight;
}

function sendLinkMessage(link, title, benefits, buttonText) {
    const chatContent = document.getElementById('chat-content');

    // Crea el contenedor del mensaje con enlace
    const linkContainer = document.createElement('div');
    linkContainer.className = 'message-container bot link-message visible';

    // Inserta contenido HTML con la imagen - título - lista de beneficios y botón
    linkContainer.innerHTML = `
        <div class="link-image-container">
            <img src="https://picsum.photos/id/237/200/300" alt="Imagen del beneficio" class="link-image visible">
        </div>
        <h4 class="link-title">${title}</h4>
        <ul class="benefits-list">
            ${benefits.map(benefit => `<li>${benefit}</li>`).join('')}
        </ul>
        <a href="${link}" target="_blank" class="link-button_chat">${buttonText}</a>
    `;

    // Agrega el mensaje al contenido del chat
    chatContent.appendChild(linkContainer);

    // Asegurarse de que el chat haga scroll hacia abajo
    chatContent.scrollTop = chatContent.scrollHeight;
}


function showTypingIndicator() {
    const chatContent = document.getElementById('chat-content');
    const typingIndicator = document.createElement('div');
    typingIndicator.id = 'typing-indicator';
    typingIndicator.className = 'message-container bot';

    const typingDots = document.createElement('div');
    typingDots.className = 'message bot typing';
    typingDots.innerHTML = '<span></span><span></span><span></span>';

    typingIndicator.appendChild(typingDots);
    chatContent.appendChild(typingIndicator);

    chatContent.scrollTop = chatContent.scrollHeight;
}

function hideTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}