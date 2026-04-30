import { Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField, Box, Autocomplete } from '@mui/material';

import { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';

import type { AppDispatch, RootState } from '../../store/store';
import type { CardioExerciseType } from '../../interfaces/interfaces';
import { createCardioSet } from '../../store/thunks/cardioTrainingThunk';

type AddEntryModalProps = {
    open: boolean;
    onClose: () => void;
};

function AddCardioSetModal({ open, onClose }: AddEntryModalProps) {
    const dispatch = useDispatch<AppDispatch>();
    const cardioTraining = useSelector((state: RootState) => state.cardioTraining.activeLog);
    const cardioExercises = useSelector((state: RootState) => state.cardioExercise.exercises);
    const [selectedExercise, setSelectedExercise] = useState<CardioExerciseType | null>(null);
    const [duration, setDuration] = useState('');
    const [description, setDescription] = useState('');
    const [durationError, setDurationError] = useState<string | null>(null);
    const valid = !!cardioTraining && !!selectedExercise && !!duration && !durationError;

    const handleDurationChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;
        setDuration(value);
        setDurationError(null);

        if (!(0.1 < Number(value) && Number(value) < 1440)) {
            setDurationError('Exercise duration must be between 0.1 and 1440 minutes.');
            return;
        }
    };

    const handleCloseModal = () => {
        setSelectedExercise(null);
        setDuration('');
        setDescription('');

        onClose();
    }

    const handleSubmit = () => {
        if (!valid) { return; }

        dispatch(
            createCardioSet({
                logId: cardioTraining.id,
                data: {
                    exercise_id: selectedExercise.id,
                    duration: duration,
                    description: description || ''
                }
            })
        );
        handleCloseModal();
    };

    return (
        <Dialog open = { open } onClose = { handleCloseModal } fullWidth maxWidth = 'sm'>
            <DialogTitle>Add Cardio Set</DialogTitle>

            <DialogContent>
                <Box sx = {{ display: 'flex', flexDirection: 'column', gap: 2, mt: 1 }}>

                    <Autocomplete
                        options = { cardioExercises }
                        getOptionLabel = {(option) => option.name + (option.description ? ` - ${option.description}` : '')}
                        value = { selectedExercise }
                        onChange = {(_, value) => setSelectedExercise(value)}
                        renderInput = {(params) => (
                            <TextField { ...params } label = 'Cardio Exercise' />
                        )}
                    />

                    <TextField
                        label = 'Duration (minutes)'
                        type = 'number'
                        value = { duration }
                        onChange = { handleDurationChange }
                        error = { !!durationError }
                        helperText = { durationError }
                    />

                    <TextField
                        label = 'Description (optional)'
                        value = { description }
                        onChange = {(e) => setDescription(e.target.value)}
                        multiline
                        rows = {2}
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
                    Add Set
                </Button>
            </DialogActions>
        </Dialog>
    );
}

export default AddCardioSetModal;
