export interface User {
  id: string;
  name: string;
  email: string;
}

export class UserService {
  private users: Map<string, User> = new Map();

  async getUserById(id: string): Promise<User | null> {
    return this.users.get(id) || null;
  }

  async createUser(payload: { name: string; email: string }): Promise<User> {
    const user: User = {
      id: `usr_${Date.now()}`,
      name: payload.name,
      email: payload.email,
    };
    this.users.set(user.id, user);
    return user;
  }
}
