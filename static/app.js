if ('serviceWorker' in navigator) {

    window.addEventListener('load', async () => {

        try {
            const registro = await navigator.serviceWorker.register('/sw.js');

            console.log('JardinesTV PWA lista:', registro);

        } catch (error) {
            console.error('Error registrando PWA:', error);
        }

    });

}