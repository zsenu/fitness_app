import { useState } from "react";
import { Container, Button, Grid, Paper, Typography, ToggleButton, ToggleButtonGroup, Stack } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import LoginForm from '../components/LoginForm';
import RegisterForm from '../components/RegisterForm';

type Mode = 'login' | 'register';

function LandingPage() {

    const [mode, setMode] = useState<Mode>('login');
    const navigate = useNavigate();

    const handleModeChange = (_: React.MouseEvent<HTMLElement>, newMode: Mode | null) => {
        if (newMode !== null) {
                setMode(newMode);
        }
    };

    const handleLearnMoreClick = () => {
        navigate('/about');
    }

    return (
    <Container maxWidth = 'lg' sx = {{ mt: 8 }}>
        <Grid container spacing = { 4 }>
            <Grid size = {{ xs: 12, md: 6 }}>
                <Typography variant = 'h3' gutterBottom>
                    Fitness App 🏃‍➡️
                </Typography>
                <Typography variant = 'body1'>
                    Track your progress, manage your goals, and stay consistent.
                </Typography>
                <Button variant = 'contained' sx = {{ mt: 2 }} onClick = { handleLearnMoreClick }>
                    Learn More
                </Button>
            </Grid>

            <Grid size = {{ xs: 12, md: 6 }}>
                <Paper sx = {{ p: 4 }}>
                    {mode === 'login' ? <LoginForm /> : <RegisterForm />}

                    <Stack direction = 'row' sx = {{ justifyContent: 'center', mt: 2 }}>
                        <ToggleButtonGroup
                            value = { mode }
                            exclusive
                            onChange = { handleModeChange }
                            size = 'small'
                        >
                            <ToggleButton value = 'login'>Login</ToggleButton>
                            <ToggleButton value = 'register'>Register</ToggleButton>
                        </ToggleButtonGroup>
                    </Stack>
                </Paper>
            </Grid>
        </Grid>
    </Container>
    );
};

export default LandingPage;
