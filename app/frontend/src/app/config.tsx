const config = {
    backend_api_url: process.env.BACKEND_API_URL || window.location.protocol + '//' + window.location.hostname + '/api',
};

export default config;