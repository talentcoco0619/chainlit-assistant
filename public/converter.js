window.onload = function() {
    console.log('ab');

    
    
}

document.addEventListener("DOMContentLoaded", function() {
    const targetNode = document.body; // Assuming the content is added to the body
    const config = { childList: true, subtree: true };

    const callback = function(mutationsList, observer) {
        for (const mutation of mutationsList) {
            if (mutation.type === 'childList') {
                const contentElement = document.getElementById('content');
                if (contentElement) {
                    upgradeHtmlContent();
                    observer.disconnect(); // Stop observing once the content is found and updated
                }
            }
        }
    };

    const observer = new MutationObserver(callback);
    observer.observe(targetNode, config);
});


function upgradeHtmlContent() {
    
    alert('fsdd');
    // Create a script element
    const script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = 'test.html'; // Assuming the script is in the same directory

    // Append the script to the body or head
    // document.body.appendChild(script);
    const contentElement = document.getElementById('content');
    if (contentElement) {
        contentElement.innerHTML = script;
    }
}