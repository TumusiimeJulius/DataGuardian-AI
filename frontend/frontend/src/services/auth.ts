import api from "./api";

export interface User {
  id: number;
  name: string;
  email: string;
  profile_picture?: string | null;
  created_at?: string;
}

export interface AuthResponse {
  status: string;
  token?: string;
  user?: User;
  message?: string;
}

export const authService = {
  // Register a new user with name, email, password
  register: async (name: string, email: string, password: string): Promise<AuthResponse> => {
    const res = await api.post<AuthResponse>("/auth/register", { name, email, password });
    return res.data;
  },

  // Login with email and password
  login: async (email: string, password: string): Promise<AuthResponse> => {
    const res = await api.post<AuthResponse>("/auth/login", { email, password });
    return res.data;
  },

  // Login/Signup with Google credential ID token
  googleLogin: async (credential: string): Promise<AuthResponse> => {
    const res = await api.post<AuthResponse>("/auth/google", { credential });
    return res.data;
  },

  // Fetch details of the currently authenticated user
  getMe: async (): Promise<AuthResponse> => {
    const res = await api.get<AuthResponse>("/auth/me");
    return res.data;
  },

  // Logout the user and remove local storage token
  logout: async (): Promise<void> => {
    try {
      await api.post("/auth/logout");
    } catch (e) {
      console.error("Logout request failed on server, cleaning local storage", e);
    } finally {
      localStorage.removeItem("dg_auth_token");
      localStorage.removeItem("dg_user");
    }
  },

  // Request password reset code
  forgotPassword: async (email: string): Promise<any> => {
    const res = await api.post("/auth/forgot-password", { email });
    return res.data;
  },

  // Complete password reset using email, code, and new password
  resetPassword: async (email: string, code: string, newPassword: string): Promise<any> => {
    const res = await api.post("/auth/reset-password", { email, code, new_password: newPassword });
    return res.data;
  }
};

