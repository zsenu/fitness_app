import { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { Container, Paper, Typography, Stack, TextField, MenuItem, CircularProgress, Button } from '@mui/material';
import { fetchUserProfile } from '../store/thunks/authThunk';
import type { RootState, AppDispatch } from '../store/store';
import type { ProfileDataType } from '../interfaces/interfaces';
import NavBar from '../components/NavBar';

function ProfilePage() {

    const user: ProfileDataType | null = useSelector((state: RootState) => state.auth.userProfile);
    const token: string | null = useSelector((state: RootState) => state.auth.accessToken);
    const [isSaving, setIsSaving] = useState<boolean>(false);

    const dispatch = useDispatch<AppDispatch>();
    
    const [activityLevel, setActivityLevel] = useState<string>(user?.activity_level || '');
    const [targetWeight, setTargetWeight] = useState<string>(user?.target_weight.toString() || '');
    const [targetDate, setTargetDate] = useState<string>(user?.target_date || '');
    const [targetCalories, setTargetCalories] = useState<string>(user?.target_calories.toString() || '');
    const isEditing = (
        activityLevel !== user?.activity_level ||
        Number(targetWeight) !== Number(user?.target_weight) ||
        targetDate !== user?.target_date ||
        Number(targetCalories) !== Number(user?.target_calories)
    );

    const handleActivityLevelChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setActivityLevel(event.target.value);
    };
    const handleTargetWeightChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setTargetWeight(event.target.value);
    };
    const handleTargetDateChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setTargetDate(event.target.value);
    };
    const handleTargetCaloriesChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setTargetCalories(event.target.value);
    };
    const handleSaveChanges = async () => {
        if (!token) {
            alert('Authorization error. Try logging in again.');
            return;
        }
        const API_BASE = process.env.DJANGO_BACKEND_URL;
        const endpoint = `${API_BASE}/profiles/me/`;
        const body = {
            activity_level: activityLevel,
            target_weight: Number(targetWeight),
            target_date: targetDate,
            target_calories: Number(targetCalories)
        };

        try {
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
                console.error('Error:', errorData);
                alert('Failed to save changes. Please try again.');
                return;
            }

            alert('Changes saved successfully!');
            dispatch(fetchUserProfile());
        }
        catch (error) {
            console.error('Error:', error);
            alert('An error occurred while saving changes. Please try again.');
        }
        finally {
            setIsSaving(false);
        }
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
                            onChange = { handleActivityLevelChange }
                            fullWidth
                        >
                            <MenuItem value = 'bmr'>Basal Metabolic Rate (BMR)</MenuItem>
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
                            onChange = { handleTargetWeightChange }
                            onBlur = {() => {
                                if (targetWeight) {
                                    setTargetWeight(Number(targetWeight).toFixed(2));
                                }
                            }}
                            fullWidth
                        />
                        <TextField
                            label = 'Target Date'
                            type = 'date'
                            value = { targetDate }
                            onChange = { handleTargetDateChange }
                            slotProps = {{ inputLabel: { shrink: true } }}
                            fullWidth
                        />
                        <TextField
                            label = 'Target Calories'
                            type = 'number'
                            value = { targetCalories }
                            onChange = { handleTargetCaloriesChange }
                            fullWidth
                        />

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

                    {
                        isEditing &&
                        <Button variant = 'contained' sx = {{ mt: 3 }} onClick = { handleSaveChanges } disabled = { isSaving }>
                            { isSaving ? 'Saving...' : 'Save Changes' }
                        </Button>
                    }
                </Paper>
            </Container>
        </>
    );
};

export default ProfilePage;
