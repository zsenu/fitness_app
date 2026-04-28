import { useState } from 'react';
import { useDispatch } from 'react-redux';
import { login } from '../store/thunks/authThunk';
import type { LoginDataType } from '../interfaces/interfaces';
import type { AppDispatch } from '../store/store';
import { useNavigate } from 'react-router-dom';
import { Button, Stack, TextField, Typography } from '@mui/material';

function LoginForm() {

    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const dispatch = useDispatch<AppDispatch>();
    const navigate = useNavigate();

    const handleFormSubmission = async (e: React.SubmitEvent) => {
        e.preventDefault();
        const loginData: LoginDataType = { username, password };
        try {
            const resultAction = await dispatch(login(loginData));
            if (login.fulfilled.match(resultAction)) {
                navigate('/dashboard');
            }
            else if (login.rejected.match(resultAction)) {
                alert(resultAction.payload?.detail || 'Login failed.');
            }
        }
        catch (error: unknown) {
            if (error instanceof Error) {
                alert(`Login failed: ${ error.message }`);
            }
        }
    }

    return (
        <form onSubmit = { handleFormSubmission }>
        <Stack spacing = { 2 }>
            <Typography variant = 'h5'>Login</Typography>

            <TextField
                label = 'Username'
                value = { username }
                onChange = { (e) => setUsername(e.target.value) }
                fullWidth
                required
                autoComplete = 'username'
            />
            <TextField
                label = 'Password'
                type = 'password'
                value = { password }
                onChange = { (e) => setPassword(e.target.value) }
                fullWidth
                required
                autoComplete = 'password'
            />

            <Button variant = 'contained' fullWidth type = 'submit'>
                Login
            </Button>
        </Stack>
        </form>
    );
}

export default LoginForm;
