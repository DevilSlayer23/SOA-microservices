class ClientConfig {    
    static getFastAPIBaseURL(): string {
        return process.env.FASTAPI_BASE_URL || 'http://localhost:8000';
    } 
    static getFastAPITimeout(): number {
        return parseInt(process.env.FASTAPI_TIMEOUT || '5000', 10);
    }
    static getFastAPIMaxRetries(): number {
        return parseInt(process.env.FASTAPI_MAX_RETRIES || '3', 10);
    }
    static getFastAPIBackoff(): number {
        return parseInt(process.env.FASTAPI_BACKOFF || '300', 10);
    }
}

export default ClientConfig;    