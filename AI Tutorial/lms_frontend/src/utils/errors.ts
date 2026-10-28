import { AxiosError } from 'axios';

export const getErrorMessage = (error: unknown, fallback = 'Something went wrong. Please try again.') => {
  if (error instanceof Error && error.message) {
    return error.message;
  }
  if (error instanceof AxiosError) {
    const data = error.response?.data as { message?: string; error?: string } | undefined;
    return data?.message || data?.error || error.message || fallback;
  }
  return fallback;
};
