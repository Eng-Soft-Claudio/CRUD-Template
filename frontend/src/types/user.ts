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
  is_active: boolean; // Não opcional na leitura
  is_superuser: boolean; // Não opcional na leitura
}

// Adicione outros tipos de User se necessário (UserUpdate, etc.)