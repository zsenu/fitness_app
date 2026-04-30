import { Container, Grid } from '@mui/material';
import NavBar from '../components/NavBar';
import DateSelector from '../components/DateSelector';
import ExerciseDashboard from '../components/ExerciseDashboard';
import FoodDashboard from '../components/food/FoodDashboard';
import HealthDashboard from '../components/HealthDashboard';
import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import type { AppDispatch, RootState } from '../store/store';
import { fetchHealthLogByDate } from '../store/thunks/healthLogThunk';
import { fetchUserProfile } from '../store/thunks/authThunk';
import { fetchFoodLogByDate } from '../store/thunks/foodLogThunk';
import { fetchAllFoodItems } from '../store/thunks/foodItemThunk';

export default function DashboardPage() {

    const dispatch = useDispatch<AppDispatch>();
    const activeDate = useSelector((state: RootState) => state.dashboard.activeDate);
    const activeHealthLog = useSelector((state: RootState) => state.healthLog.activeLog);

    useEffect(() => {
        dispatch(fetchAllFoodItems());
    }, [dispatch]);

    useEffect(() => {
        dispatch(fetchHealthLogByDate(activeDate));
        dispatch(fetchFoodLogByDate(activeDate));
    }, [activeDate, dispatch]);

    useEffect(() => {
        dispatch(fetchUserProfile());
    }, [dispatch, activeHealthLog]);

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