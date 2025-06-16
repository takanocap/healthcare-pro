// utils/auth.ts
export const isAuthenticated = (): boolean => {
  const user = JSON.parse(localStorage.getItem('user') || 'null');
  return !!user?.username;
};
