export interface Token {
  access_token: string;
  token_type: string;
  refresh_token?: string | null;
}

export interface TokenData {
  email?: string | null;
}