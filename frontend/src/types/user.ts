export interface UserBase {
  full_name?: string | null;
  is_active?: boolean;
  is_superuser?: boolean;
}

export interface UserCreate extends UserBase {
  email: string;
  password: string;
}

export interface UserRead extends UserBase {
  id: number;
  email: string;
  is_active: boolean; 
  is_superuser: boolean; 
}

export interface UserPasswordChange {
  current_password: string;
  new_password: string;
  new_password_confirm: string;
}

export interface PasswordRecoveryRequest {
  email: string;
}

export interface PasswordResetForm {
  token: string;
  new_password: string;
  new_password_confirm: string;
}

export interface UserUpdate {
  email?: string | null;       
  password?: string | null;    
  full_name?: string | null;
  is_active?: boolean;
  is_superuser?: boolean;
}