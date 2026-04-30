import { Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField, Box } from '@mui/material';

import { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';

import type { AppDispatch, RootState } from '../../store/store';
import { createCardioExercise } from '../../store/thunks/cardioExerciseThunk';

type AddItemModalProps = {
    open: boolean;
    onClose: () => void;
};

function AddCardioExerciseModal({ open, onClose }: AddItemModalProps) {
    const cardioExercises = useSelector((state: RootState) => state.cardioExercise.exercises);
    const dispatch = useDispatch<AppDispatch>();

    const [name, setName] = useState('');
    const [nameError, setNameError] = useState<string | null>(null);

    const [description, setDescription] = useState('');

    const [caloriesPerMinute, setCaloriesPerMinute] = useState('');
    const [caloriesPerMinuteError, setCaloriesPerMinuteError] = useState<string | null>(null);

    const valid: boolean = name !== '' && caloriesPerMinute !== '' && !nameError && !caloriesPerMinuteError;

    const handleNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setNameError(null);

        if (cardioExercises.some(item => item.name.toLowerCase() === e.target.value.toLowerCase())) {
            setNameError('A cardio exercise with this name already exists');
        }
        
        setName(e.target.value);
    };

    const handleCloseModal = () => {
        setName('');
        setDescription('');
        setCaloriesPerMinute('');

        onClose();
    }

    const handleCaloriesPerMinuteChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setCaloriesPerMinuteError(null);

        const value = e.target.value;
        if (!(0.1 <= Number(value) && Number(value) <= 50)) {
            setCaloriesPerMinuteError('Calories burned per minute must be between 0.1 and 50.');
        }
        
        setCaloriesPerMinute(value);
    };

    const handleSubmit = () => {
        if (!valid) { return; }

        dispatch(
            createCardioExercise({
                name: name,
                description: description,
                calories_per_minute: Number(caloriesPerMinute)
            })
        );

        handleCloseModal();
    };

    return (
        <Dialog open = { open } onClose = { handleCloseModal } fullWidth maxWidth = 'sm'>
            <DialogTitle>Add Cardio Exercise</DialogTitle>

            <DialogContent>
                <Box sx = {{ display: 'flex', flexDirection: 'column', gap: 2, mt: 1 }}>
                    <TextField
                        label = 'Name (unique)'
                        value = { name }
                        onChange = { handleNameChange }
                        error = { !!nameError }
                        helperText = { nameError }
                    />

                    <TextField
                        label = 'Description (optional)'
                        value = { description }
                        onChange = {(e) => setDescription(e.target.value)}
                        multiline
                        rows = {2}
                    />

                    <TextField
                        label = 'Calories burned per minute'
                        type = 'number'
                        value = { caloriesPerMinute }
                        onChange = { handleCaloriesPerMinuteChange }
                        error = { !!caloriesPerMinuteError }
                        helperText = { caloriesPerMinuteError }
                    />
                </Box>
            </DialogContent>

            <DialogActions>
                <Button onClick = { handleCloseModal }>Cancel</Button>
                <Button
                    variant = 'contained'
                    onClick = { handleSubmit }
                    disabled = { !valid }
                >
                    Add Exercise
                </Button>
            </DialogActions>
        </Dialog>
    );
}

export default AddCardioExerciseModal;
