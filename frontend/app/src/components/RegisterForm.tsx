import { useState } from 'react';
import { useDispatch } from 'react-redux';
import { register } from '../store/thunks/authThunk';
import type { RegisterDataType } from '../interfaces/interfaces';
import type { AppDispatch } from '../store/store';
import { useNavigate } from 'react-router-dom';
import { Button, MenuItem, Stack, TextField, Typography } from '@mui/material';

const MIN_AGE = 18;
const MAX_AGE = 150;

function RegisterForm() {

    const [username,       setUsername]       = useState('');
    const [email,          setEmail]          = useState('');
    const [password,       setPassword]       = useState('');
    const [repeatPassword, setRepeatPassword] = useState('');
    const [gender,         setGender]         = useState('');
    const [birthDate,      setBirthDate]      = useState('');
    const [height,         setHeight]         = useState('');
    const [startingWeight, setStartingWeight] = useState('');
    const [activityLevel,  setActivityLevel]  = useState('');
    const [targetWeight,   setTargetWeight]   = useState('');
    const [targetDate,     setTargetDate]     = useState('');
    const [targetCalories, setTargetCalories] = useState('');
    const [errors,         setErrors]         = useState({
        username: '',
        email: '',
        password: '',
        repeatPassword: '',
        birthDate: '',
        height: '',
        startingWeight: '',
        targetWeight: '',
        targetDate: '',
        targetCalories: '',
    });

    const dispatch = useDispatch<AppDispatch>();
    const navigate = useNavigate();

    const validateBirthDate = (date: string): boolean => {

        const today = new Date();
        const birth = new Date(date);
        let age = today.getFullYear() - birth.getFullYear();
        const monthDiff = today.getMonth() - birth.getMonth();
        if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
            age -= 1;
        }
        return (MIN_AGE <= age && age <= MAX_AGE);
    }

    const validateTargetDate = (date: string): boolean => {
        const today = new Date();
        const target = new Date(date);
        const farFuture = new Date();
        farFuture.setFullYear(farFuture.getFullYear() + 100);
        return (today < target && target < farFuture);
    }

    const handleFormSubmission = async (e: React.SubmitEvent) => {
        e.preventDefault();
        let valid: boolean = true;
        const newErrors = {
            username: '',
            email: '',
            password: '',
            repeatPassword: '',
            birthDate: '',
            height: '',
            startingWeight: '',
            targetWeight: '',
            targetDate: '',
            targetCalories: '',
        }

        if (password.length < 8) {
            newErrors.password = 'Password must be at least 8 characters long';
            valid = false;
        }
        else if (/^\d+$/.test(password)) {
            newErrors.password = 'Password cannot be entirely numeric';
            valid = false;
        }

        if (password !== repeatPassword) {
            newErrors.repeatPassword = 'Passwords do not match';
            valid = false;
        }

        if (!validateBirthDate(birthDate)) {
            newErrors.birthDate = `You must be between ${MIN_AGE} and ${MAX_AGE} years old`;
            valid = false;
        }

        if (!validateTargetDate(targetDate)) {
            newErrors.targetDate = 'Target date must be in the future and within a reasonable range';
            valid = false;
        }

        if (valid) {
            const registerData: RegisterDataType = {
                username,
                password,
                password2: repeatPassword,
                email,
                gender,
                birth_date: birthDate,
                height: parseFloat(height),
                starting_weight: parseFloat(startingWeight),
                activity_level: activityLevel,
                target_weight: parseFloat(targetWeight),
                target_date: targetDate,
                target_calories: parseFloat(targetCalories),
            };
            try {
                const resultAction = await dispatch(register(registerData));
                if (register.fulfilled.match(resultAction)) {
                    navigate('/dashboard');
                }
                else if (register.rejected.match(resultAction)) {
                    const errorPayload = resultAction.payload;
                    if (errorPayload) {
                        Object.entries(errorPayload).forEach(([field, messages]) => {
                            console.log(`Field: ${ field }, Messages: ${ messages }`);
                            if (field in newErrors) {
                                newErrors[field as keyof typeof newErrors] = (messages as string[]).join(' ');
                            }
                        });
                    }
                }
            }
            catch (error: unknown) {
                if (error instanceof Error) {
                    alert(`Login failed: ${ error.message }`);
                }
            }
        }

        setErrors(newErrors);
    }

    return (
        <form onSubmit = { handleFormSubmission }>
        <Stack spacing = { 2 }>
            <Typography variant = 'h5'>Register</Typography>

            <TextField
                label = 'Username'
                value = { username }
                onChange = { (e) => setUsername(e.target.value) }
                fullWidth
                required
                autoComplete = 'new-username'
                error = { !!errors.username }
                helperText = { errors.username }
            />
            <TextField
                label = 'Email'
                type = 'email'
                value = { email }
                onChange = { (e) => setEmail(e.target.value) }
                fullWidth
                required
                error = { !!errors.email }
                helperText = { errors.email }
            />
            <TextField
                label = 'Password'
                type = 'password'
                value = { password }
                onChange = { (e) => setPassword(e.target.value) }
                fullWidth
                required
                autoComplete = 'new-password'
                error = { !!errors.password }
                helperText = { errors.password }
            />
            <TextField
                label = 'Repeat Password'
                type = 'password'
                value = { repeatPassword }
                onChange = { (e) => setRepeatPassword(e.target.value) }
                fullWidth
                required
                autoComplete = 'new-password'
                error = { !!errors.repeatPassword }
                helperText = { errors.repeatPassword }
            />

            <TextField
                select
                label = 'Gender'
                value = { gender }
                onChange = { (e) => setGender(e.target.value) }
                fullWidth
                required
            >
                <MenuItem value = 'M'>Male</MenuItem>
                <MenuItem value = 'F'>Female</MenuItem>
            </TextField>

            <TextField
                label = 'Birth Date'
                type = 'date'
                value = { birthDate }
                onChange = { (e) => setBirthDate(e.target.value) }
                slotProps = {{ inputLabel: { shrink: true } }}
                fullWidth
                required
                error = { !!errors.birthDate }
                helperText = { errors.birthDate }
            />

            <TextField
                label = 'Height (cm)'
                type = 'number'
                value = { height }
                onChange = { (e) => setHeight(e.target.value) }
                slotProps = {{ htmlInput: { min: 140, max: 240, step: 0.1 } }}
                fullWidth
                required
                error = { !!errors.height }
                helperText = { errors.height }
            />

            <TextField
                label = 'Starting Weight (kg)'
                type = 'number'
                value = { startingWeight }
                onChange = { (e) => setStartingWeight(e.target.value) }
                slotProps = {{ htmlInput: { min: 40, max: 140, step: 0.1 } }}
                fullWidth
                required
                error = { !!errors.startingWeight }
                helperText = { errors.startingWeight }
            />

            <TextField
                select
                label = 'Activity Level'
                value = { activityLevel }
                onChange = { (e) => setActivityLevel(e.target.value) }
                fullWidth
                required
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
                onChange = { (e) => setTargetWeight(e.target.value) }
                slotProps = {{ htmlInput: { min: 40, max: 140, step: 0.1 } }}
                fullWidth
                required
                error = { !!errors.targetWeight }
                helperText = { errors.targetWeight }
            />

            <TextField
                label = 'Target Date'
                type = 'date'
                value = { targetDate }
                onChange = { (e) => setTargetDate(e.target.value) }
                slotProps = {{ inputLabel: { shrink: true } }}
                fullWidth
                required
                error = { !!errors.targetDate }
                helperText = { errors.targetDate }
            />

            <TextField
                label = 'Target Calories'
                type = 'number'
                value = { targetCalories }
                onChange = { (e) => setTargetCalories(e.target.value) }
                slotProps = {{ htmlInput: { min: 100, max: 10000, step: 0.1 } }}
                fullWidth
                required
                error = { !!errors.targetCalories }
                helperText = { errors.targetCalories }
            />

            <Button variant = 'contained' fullWidth type = 'submit'>
                Register
            </Button>
        </Stack>
        </form>
    );
}
export default RegisterForm;
