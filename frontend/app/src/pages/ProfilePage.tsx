import { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { Container, Paper, Typography, Stack, TextField, MenuItem, CircularProgress, Button } from '@mui/material';
import { fetchUserProfile } from '../store/thunks/authThunk';
import type { RootState, AppDispatch } from '../store/store';
import type { ProfileDataType } from '../interfaces/interfaces';
import NavBar from '../components/NavBar';
import targetCalorieCalculator from '../helpers/targetCalorieCalculator';
import calorieBoundaryCalculator from '../helpers/calorieBoundaryCalculator';
import StatisticsContainer from '../components/StatisticsContainer';

function ProfilePage() {

    const user: ProfileDataType | null = useSelector((state: RootState) => state.auth.userProfile);
    const token: string | null = useSelector((state: RootState) => state.auth.accessToken);
    const [isSaving, setIsSaving] = useState<boolean>(false);

    const dispatch = useDispatch<AppDispatch>();
    
    const [activityLevel, setActivityLevel] = useState<string>(user?.activity_level || '');
    const [targetWeight, setTargetWeight] = useState<string>(user?.target_weight.toString() || '');
    const [targetDate, setTargetDate] = useState<string>(user?.target_date || '');
    const [targetCalories, setTargetCalories] = useState<string>(user?.target_calories.toString() || '');
    const [errors, setErrors] = useState<Record<string, string[]> | null>(null);
    const isEditing = (
        activityLevel !== user?.activity_level ||
        Number(targetWeight) !== Number(user?.target_weight) ||
        targetDate !== user?.target_date ||
        Number(targetCalories) !== Number(user?.target_calories)
    );

    const gender: string | null = user?.gender || null;
    const birthDate: string | null = user?.birth_date || null;
    const height: string | null = user?.height.toString() || null;
    const currentWeight: string | null = user?.current_weight.toString() || null;
            
    const validateTargetDate = (date: string): boolean => {
        const today = new Date();
        const target = new Date(date);
        const farFuture = new Date();
        farFuture.setFullYear(farFuture.getFullYear() + 100);
        return (today < target && target < farFuture);
    }

    const validateWeight = (value: string): boolean => {
        const weight = parseFloat(value);
        return (weight >= 40 && weight <= 140);
    }

    const calculatedCalories =
        gender &&
        birthDate &&
        height &&
        currentWeight &&
        activityLevel &&
        targetWeight &&
        targetDate &&
        validateTargetDate(targetDate) &&
        validateWeight(targetWeight)
            ? targetCalorieCalculator(
                gender,
                birthDate,
                parseFloat(currentWeight),
                parseFloat(height),
                activityLevel,
                parseFloat(targetWeight),
                targetDate
            )
            : null;

    const { minCalories, maxCalories } = 
        gender &&
        birthDate &&
        height &&
        currentWeight &&
        activityLevel &&
        validateTargetDate(targetDate) &&
        validateWeight(targetWeight)
            ? calorieBoundaryCalculator(
                gender,
                birthDate,
                parseFloat(currentWeight),
                parseFloat(height),
                activityLevel
            )
            : { minCalories: null, maxCalories: null };

    const handleSaveChanges = async () => {
        if (!token) {
            setErrors({ non_field_errors: ['No authorization token found.'] });
            return;
        }
        const endpoint = `${ process.env.DJANGO_BACKEND_URL }/profiles/me/`;
        const body = {
            activity_level: activityLevel,
            target_weight: Number(targetWeight),
            target_date: targetDate,
            target_calories: Number(targetCalories)
        };

        setIsSaving(true);
        const response = await fetch(endpoint, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${ token }`
            },
            body: JSON.stringify(body)
        });

        if (!response.ok) {
            const errorData = await response.json();
            setErrors(errorData);
            setIsSaving(false);
            return;
        }

        dispatch(fetchUserProfile());
        setIsSaving(false);
    };

    if (!user) {
        return (
            <>
                <NavBar parent = 'profile' />
                <Container sx = {{ mt: 6, textAlign: 'center' }}>
                    <CircularProgress />
                    <Typography sx = {{ mt: 2 }}>Loading profile...</Typography>
                </Container>
            </>
        );
    }

    return (
        <>
            <NavBar parent = 'profile' />

            <Container maxWidth = 'sm' sx = {{ mt: 6 }}>
                <Paper sx = {{ p: 4 }}>
                    <Typography variant = 'h4' gutterBottom>
                        Profile
                    </Typography>

                    <Stack spacing = {2}>
                        <TextField label = 'Username' value = { user.username } fullWidth disabled />
                        <TextField label = 'Email' value = { user.email } fullWidth disabled />
                        <TextField label = 'Gender' value = { user.gender } fullWidth disabled />
                        <TextField
                            label = 'Birth Date'
                            value = { user.birth_date }
                            fullWidth
                            disabled
                        />
                        <TextField
                            label = 'Height (cm)'
                            type = 'number'
                            value = { Number(user.height).toFixed(2) }
                            fullWidth
                            disabled
                        />
                        <TextField
                            label = 'Starting Weight (kg)'
                            type = 'number'
                            value = { Number(user.starting_weight).toFixed(2) }
                            fullWidth
                            disabled
                        />
                        <TextField
                            label = 'Current Weight (kg)'
                            type = 'number'
                            value = { Number(user.current_weight).toFixed(2) }
                            fullWidth
                            disabled
                        />

                        <TextField
                            select
                            label = 'Activity Level'
                            value = { activityLevel }
                            onChange = {(e) => {
                                setErrors(null);
                                setActivityLevel(e.target.value);
                            }}
                            fullWidth
                            error = { !!errors?.activity_level }
                            helperText = { errors?.activity_level ? errors.activity_level.join(' ') : '' }
                        >
                            <MenuItem value = 'sedentary'>Sedentary (little or no exercise)</MenuItem>
                            <MenuItem value = 'lightly_active'>Lightly active (light exercise/sports 1-3 days/week)</MenuItem>
                            <MenuItem value = 'moderately_active'>Moderately active (moderate exercise/sports 3-5 days/week)</MenuItem>
                            <MenuItem value = 'very_active'>Very active (hard exercise/sports 6-7 days a week)</MenuItem>
                            <MenuItem value = 'extra_active'>Extra active (very hard exercise/sports & physical job or 2x training)</MenuItem>
                        </TextField>
                        <TextField
                            label = 'Target Weight (kg)'
                            type = 'number'
                            value = { targetWeight }
                            onChange = {(e) =>
                            {
                                setErrors(null);
                                setTargetWeight(e.target.value)
                            }}
                            onBlur = {() => {
                                if (targetWeight) {
                                    setTargetWeight(Number(targetWeight).toFixed(2));
                                }
                            }}
                            fullWidth
                            error = { !!errors?.target_weight }
                            helperText = { errors?.target_weight ? errors.target_weight.join(' ') : '' }
                        />
                        <TextField
                            label = 'Target Date'
                            type = 'date'
                            value = { targetDate }
                            onChange = {(e) => {
                                setErrors(null);
                                setTargetDate(e.target.value)
                            }}
                            slotProps = {{ inputLabel: { shrink: true } }}
                            fullWidth
                            error = { !!errors?.target_date }
                            helperText = { errors?.target_date ? errors.target_date.join(' ') : '' }
                        />
                        <TextField
                            label = 'Target Calories'
                            type = 'number'
                            value = { targetCalories }
                            onChange = {(e) => {
                                setErrors(null);
                                setTargetCalories(e.target.value)
                            }}
                            fullWidth
                            error = { !!errors?.target_calories }
                            helperText = { errors?.target_calories ? errors.target_calories.join(' ') : '' }
                        />
                        { calculatedCalories !== null &&
                            <Typography>
                                Based on your inputs, your target daily calorie intake to reach your goal is approximately { calculatedCalories } calories.
                                { minCalories !== null && calculatedCalories < minCalories && ` This is below the recommended minimum of ${ minCalories } calories.` }
                                { maxCalories !== null && calculatedCalories > maxCalories && ` This is above the recommended maximum of ${ maxCalories } calories.` }
                            </Typography>
                        }

                        <TextField
                            label = 'BMR (kcal/day)'
                            type = 'number'
                            value = { Number(user.bmr).toFixed(2) }
                            fullWidth
                            disabled
                        />
                        <TextField
                            label = 'TDEE (kcal/day)'
                            type = 'number'
                            value = { Number(user.tdee).toFixed(2) }
                            fullWidth
                            disabled
                        />
                    </Stack>
                    { errors?.non_field_errors &&
                        <Typography color = 'error' sx = {{ mt: 2 }}>
                            { errors.non_field_errors.join(' ') }
                        </Typography>
                    }
                    {
                        isEditing &&
                        <Button variant = 'contained' sx = {{ mt: 3 }} onClick = { handleSaveChanges } disabled = { isSaving }>
                            { isSaving ? 'Saving...' : 'Save Changes' }
                        </Button>
                    }
                </Paper>
            </Container>
            <StatisticsContainer />
        </>
    );
};

export default ProfilePage;
