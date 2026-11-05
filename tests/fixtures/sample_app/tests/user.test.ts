import { UserService } from '../src/services/userService';

describe('UserService', () => {
  let service: UserService;

  beforeEach(() => {
    service = new UserService();
  });

  it('creates and retrieves a user', async () => {
    const user = await service.createUser({ name: 'Alice', email: 'alice@example.com' });
    expect(user.id).toBeDefined();
    expect(user.name).toBe('Alice');

    const fetched = await service.getUserById(user.id);
    expect(fetched).toEqual(user);
  });
});
