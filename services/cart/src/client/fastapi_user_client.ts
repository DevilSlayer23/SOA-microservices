import axios, { AxiosInstance } from "axios";
import ClientConfig from "./client_config";

const config = {
  FASTAPI_URL: ClientConfig.getFastAPIBaseURL(),
  TIMEOUT: ClientConfig.getFastAPITimeout(),
  MAX_RETRIES: ClientConfig.getFastAPIMaxRetries(),
  BACKOFF: ClientConfig.getFastAPIBackoff(),
};


const MAX_RETRIES = 3;
const BACKOFF = 300;

class FastAPIClient {
  client: AxiosInstance;
  constructor() {
    this.client = axios.create({
      baseURL: config.FASTAPI_URL,
      timeout: config.TIMEOUT,
      
    });
  }

  private async requestWithRetry(method: string, path: string, data?: any, token?: string) {
    let attempt = 0;
    let lastError: any = null;
    const headers: any = {};
    if (token) headers.Authorization = `Bearer ${token}`;

    while (attempt < MAX_RETRIES) {
      try {
        const res = await this.client.request({ method, url: path, data, headers });
        console.log(`Request to ${path} succeeded on attempt ${attempt + 1}`);
        return res.data;
      } catch (err: any) {
        lastError = err;
        attempt++;
        await new Promise((r) => setTimeout(r, BACKOFF * Math.pow(2, attempt - 1)));
      }
    }
    throw lastError;
  }

  async getProduct(productId: number, token?: string) {
    return this.requestWithRetry("GET", `/products/${productId}`, undefined, token);
  }

  async getUser(userId: number, token?: string) {
    return this.requestWithRetry("GET", `/users/${userId}`, undefined, token);
  }

  async login(email: string, password: string) {
    return this.requestWithRetry("POST", `/users/login`, { email, password }, undefined);
  }
}

export const fastapiClient = new FastAPIClient();

export default fastapiClient;