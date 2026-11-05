import { Router, Request, Response } from 'express';
import { UserService } from '../services/userService';

export const userRouter = Router();
const userService = new UserService();

userRouter.get('/:id', async (req: Request, res: Response) => {
  try {
    const user = await userService.getUserById(req.params.id);
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }
    return res.json({ data: user });
  } catch (error) {
    return res.status(500).json({ error: 'Internal server error' });
  }
});

userRouter.post('/', async (req: Request, res: Response) => {
  try {
    const user = await userService.createUser(req.body);
    return res.status(201).json({ data: user });
  } catch (error) {
    return res.status(400).json({ error: 'Invalid user payload' });
  }
});
