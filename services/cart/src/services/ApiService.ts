import axios, {

AxiosInstance,
AxiosRequestConfig,
AxiosResponse,
AxiosError,
CancelTokenSource,
InternalAxiosRequestConfig,
} from "axios";
import { ApiClientOptions } from "./ApiClientType";



/**
 * Lightweight, fully-modular Axios wrapper with:
 * - typed responses
 * - retries + exponential backoff
 * - optional auth-refresh handler
 * - request/response interceptors management
 * - cancel token helpers
 * - convenience verb methods
 */
export class ApiClient {
private axios: AxiosInstance;
private retries: number;
private retryDelay: number;
private refreshAuth?: (error: AxiosError) => Promise<string | null>;
private onAuthFailure?: () => void;

constructor(opts: ApiClientOptions = {}) {
    this.axios = axios.create({
        baseURL: opts.baseURL ?? undefined,
        timeout: opts.timeout ?? 30_000,
        headers: opts.headers ?? { "Content-Type": "application/json" },
    });

    this.retries = Math.max(0, opts.retries ?? 0);
    this.retryDelay = Math.max(100, opts.retryDelay ?? 300);
    this.refreshAuth = opts.refreshAuth;
    this.onAuthFailure = opts.onAuthFailure;

    // Default response interceptor to unwrap data, you can add more via addResponseInterceptor
    this.axios.interceptors.response.use(
        (r) => r,
        (e) => Promise.reject(e)
    );
}

setBaseURL(url: string | undefined) {
    this.axios.defaults.baseURL = url;
}

setDefaultHeaders(headers: Record<string, string>) {
    this.axios.defaults.headers.common = {
        ...(this.axios.defaults.headers.common || {}),
        ...headers,
    };
}

setAuthToken(token: string | null) {
    if (token) {
        this.axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
    } else {
        delete this.axios.defaults.headers.common["Authorization"];
    }
}

addRequestInterceptor(
    onFulfilled?: (value: InternalAxiosRequestConfig) => InternalAxiosRequestConfig | Promise<InternalAxiosRequestConfig>,
    onRejected?: (error: any) => any
) {
    return this.axios.interceptors.request.use(onFulfilled, onRejected);
}


ejectRequestInterceptor(id: number) {
    this.axios.interceptors.request.eject(id);
}

addResponseInterceptor<T = any>(
    onFulfilled?: (value: AxiosResponse<T>) => AxiosResponse<T> | Promise<AxiosResponse<T>>,
    onRejected?: (error: any) => any
) {
    return this.axios.interceptors.response.use(onFulfilled, onRejected);
}

ejectResponseInterceptor(id: number) {
    this.axios.interceptors.response.eject(id);
}

createCancelToken(): CancelTokenSource {
    return axios.CancelToken.source();
}

cancelRequest(source: CancelTokenSource, message?: string) {
    source.cancel(message ?? "canceled");
}

private isRetriableError(err: AxiosError): boolean {
    if (axios.isCancel(err)) return false;
    if (!err || !err.config) return false;
    // network or 5xx
    if (!err.response) return true; // network error
    const status = err.response.status;
    return status >= 500 && status < 600;
}

private sleep(ms: number) {
    return new Promise((res) => setTimeout(res, ms));
}

async request<T = any>(config: AxiosRequestConfig): Promise<T> {
    // ensure mutable copy
    const cfg = { ...config };
    (cfg as any).__retryCount = (cfg as any).__retryCount ?? 0;

    while (true) {
        try {
            const resp = await this.axios.request<T>(cfg);
            return resp.data;
        } catch (err) {
            const error = err as AxiosError;

            // 401 handling + optional refreshAuth
            if (error.response && error.response.status === 401 && this.refreshAuth) {
                try {
                    const newToken = await this.refreshAuth(error);
                    if (newToken) {
                        this.setAuthToken(newToken);
                        // retry original request once after token refresh
                        (cfg as any).__retryCount = (cfg as any).__retryCount || 0;
                        if ((cfg as any).__retryCount < 1) {
                            (cfg as any).__retryCount += 1;
                            continue;
                        }
                    } else {
                        this.onAuthFailure?.();
                        throw error;
                    }
                } catch (refreshErr) {
                    this.onAuthFailure?.();
                    throw error;
                }
            }

            // retry network or 5xx errors if configured
            if (this.retries > 0 && this.isRetriableError(error)) {
                const current = (cfg as any).__retryCount ?? 0;
                if (current < this.retries) {
                    (cfg as any).__retryCount = current + 1;
                    const delay = this.retryDelay * Math.pow(2, current);
                    await this.sleep(delay);
                    continue;
                }
            }

            // otherwise throw
            throw error;
        }
    }
}

// convenience methods
get<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
    return this.request<T>({ ...config, method: "GET", url });
}

post<T = any, B = any>(url: string, body?: B, config?: AxiosRequestConfig): Promise<T> {
    return this.request<T>({ ...config, method: "POST", url, data: body });
}

put<T = any, B = any>(url: string, body?: B, config?: AxiosRequestConfig): Promise<T> {
    return this.request<T>({ ...config, method: "PUT", url, data: body });
}

patch<T = any, B = any>(url: string, body?: B, config?: AxiosRequestConfig): Promise<T> {
    return this.request<T>({ ...config, method: "PATCH", url, data: body });
}

delete<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
    return this.request<T>({ ...config, method: "DELETE", url });
}
}

/**
 * Factory helper for modular creation:
 * const api = createApiClient({ baseURL: "...", retries: 2 });
 */
export function createApiClient(opts: ApiClientOptions = {}) {
return new ApiClient(opts);
}

export default createApiClient;