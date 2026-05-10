import { createContext, useContext, useEffect, useState, type ReactNode } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { login as loginApi, register as registerApi, type LoginParams } from '../api/auth';
import { getMe } from '../api/users';
import type { UserResponse, RegisterRequest } from '../api/types';

interface AuthContextValue {
  user: UserResponse | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (params: LoginParams) => Promise<void>;
  register: (request: RegisterRequest) => Promise<UserResponse>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const queryClient = useQueryClient();
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('access_token'));

  const { data: user, isLoading } = useQuery({
    queryKey: ['me'],
    queryFn: getMe,
    enabled: !!token,
    retry: false,
  });

  // Sync logout triggered by the 401 interceptor
  useEffect(() => {
    const handleUnauthorized = () => {
      localStorage.removeItem('access_token');
      setToken(null);
      queryClient.clear();
    };
    window.addEventListener('auth:unauthorized', handleUnauthorized);
    return () => window.removeEventListener('auth:unauthorized', handleUnauthorized);
  }, [queryClient]);

  const login = async (params: LoginParams) => {
    const tokenData = await loginApi(params);
    localStorage.setItem('access_token', tokenData.access_token);
    setToken(tokenData.access_token);
    await queryClient.invalidateQueries({ queryKey: ['me'] });
  };

  const register = (request: RegisterRequest) => registerApi(request);

  const logout = () => {
    localStorage.removeItem('access_token');
    setToken(null);
    queryClient.clear();
  };

  return (
    <AuthContext.Provider
      value={{
        user: user ?? null,
        isLoading: !!token && isLoading,
        isAuthenticated: !!user,
        login,
        register,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
}
