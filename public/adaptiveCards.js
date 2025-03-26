
(async function() {
    // Load Adaptive Cards library
    const script = document.createElement('script');
    script.src = 'https://unpkg.com/adaptivecards/dist/adaptivecards.min.js';
    document.head.appendChild(script);
  
    // Wait for library to load
    await new Promise(resolve => script.onload = resolve);
  
    // Initialize Adaptive Cards renderer
    const adaptiveCards = new AdaptiveCards.AdaptiveCard();
    adaptiveCards.hostConfig = new AdaptiveCards.HostConfig({
      fontFamily: "Segoe UI, Helvetica Neue, sans-serif"
    });
  
    // Process existing messages
    processMessages();
    
    // Create mutation observer for new messages
    new MutationObserver(processMessages).observe(
      document.querySelector('[data-test="messages"]'), 
      { childList: true }
    );
  
    function processMessages() {
      document.querySelectorAll('.message-content').forEach(element => {
        try {
          const cardData = JSON.parse(element.textContent);
          if (cardData.type === "AdaptiveCard") {
            const card = adaptiveCards.parse(cardData);
            const renderedCard = card.render();
            element.innerHTML = '';
            element.appendChild(renderedCard);
          }
        } catch (e) {
          // Not a JSON card, leave as regular message
        }
      });
    }
  })();
  