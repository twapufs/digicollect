import { apiClient } from './client';
import type { Token, RegisterRequest, UserResponse } from './types';

export interface LoginParams {
  username: string;
  password: string;
}

export async function login(params: LoginParams): Promise<Token> {
  const body = new URLSearchParams({ username: params.username, password: params.password });
  const { data } = await apiClient.post<Token>('/auth/token', body, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  });
  return data;
}

export async function register(request: RegisterRequest): Promise<UserResponse> {
  const { data } = await apiClient.post<UserResponse>('/auth/register', request);
  return data;
}
