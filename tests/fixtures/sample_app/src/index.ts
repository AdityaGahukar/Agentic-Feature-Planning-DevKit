import express from 'express';
import { userRouter } from './routes/user';

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());
app.use('/api/users', userRouter);

app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

if (process.env.NODE_ENV !== 'test') {
  app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
  });
}

export default app;
