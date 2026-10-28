import axios from 'axios';
import type {
  AuthLoginRequest,
  AuthLoginResponse,
  AuthRegisterRequest,
} from './apiTypes';
import { parseOrThrow } from './schemas';
import { z } from 'zod';

export const authApi = {
  async login(payload: AuthLoginRequest): Promise<{ data: AuthLoginResponse }> {
    const form = new URLSearchParams();
    form.append('username', payload.email);
    form.append('password', payload.password);
    const response = await axios.post('/api/v1/auth/login', form, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });
    const raw = parseOrThrow(
      RawAuthLoginResponseSchema,
      response.data,
      'auth login',
    );
    return { data: { token: raw.access_token, role: raw.user.role } };
  },

  async register(payload: AuthRegisterRequest): Promise<{ data: unknown }> {
    const response = await axios.post('/api/v1/auth/signup', payload);
    return { data: response.data };
  },
};

const RawAuthLoginResponseSchema = z.object({
  access_token: z.string(),
  user: z.object({
    role: z.string(),
  }),
});
