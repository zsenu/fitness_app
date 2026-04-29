import { Container, Grid } from '@mui/material';
import NavBar from '../components/NavBar';
import DateSelector from '../components/DateSelector';
import ExerciseDashboard from '../components/ExerciseDashboard';
import FoodDashboard from '../components/FoodDashboard';
import HealthDashboard from '../components/HealthDashboard';

export default function DashboardPage() {
    return (
    <>
    <NavBar parent = { 'dashboard' } />
    <DateSelector />

    <Container maxWidth = 'lg' sx = {{ mt: 4 }}>
        <Grid container spacing = { 3 }>
            <Grid size = {{ xs: 12, md: 4 }}>
                <ExerciseDashboard />
            </Grid>

            <Grid size = {{ xs: 12, md: 4 }}>
                <FoodDashboard />
            </Grid>

            <Grid size = {{ xs: 12, md: 4 }}>
                <HealthDashboard />
            </Grid>
        </Grid>
    </Container>
    </>
    );
}