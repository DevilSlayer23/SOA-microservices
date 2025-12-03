import { AxiosError } from "axios";

export interface ApiClientOptions {
baseURL?: string;
timeout?: number;
headers?: Record<string, string>;
retries?: number; // number of retry attempts on network/5xx errors
retryDelay?: number; // base ms delay for exponential backoff
/**
 * Optional function to refresh auth when a 401 occurs.
 * Should return a new token string or null if refresh failed.
 */
refreshAuth?: (error: AxiosError) => Promise<string | null>;
/**
 * Called when refresh failed (e.g., force logout).
 */
onAuthFailure?: () => void;
}