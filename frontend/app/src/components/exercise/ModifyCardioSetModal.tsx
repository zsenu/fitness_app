import { Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField, Box, Autocomplete } from '@mui/material';

import { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';

import type { AppDispatch, RootState } from '../../store/store';
import type { CardioExerciseType, CardioSetType } from '../../interfaces/interfaces';
import { updateCardioSet, deleteCardioSet } from '../../store/thunks/cardioTrainingThunk';

type ModifyEntryModalProps = {
    entry: CardioSetType;
    open: boolean;
    onClose: () => void;
};

function AddCardioSetModal({ entry, open, onClose }: ModifyEntryModalProps) {
    const dispatch = useDispatch<AppDispatch>();
    const cardioExercises = useSelector((state: RootState) => state.cardioExercise.exercises);
    const [selectedExercise, setSelectedExercise] = useState<CardioExerciseType | null>(entry.exercise || null);
    const [duration, setDuration] = useState(entry.duration.toString() || '');
    const [description, setDescription] = useState(entry.description || '');
    const [durationError, setDurationError] = useState<string | null>(null);
    const valid = !!selectedExercise && !!duration && !durationError;

    const handleDurationChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;
        setDuration(value);
        setDurationError(null);

        if (!(0.1 < Number(value) && Number(value) < 1440)) {
            setDurationError('Exercise duration must be between 0.1 and 1440 minutes.');
            return;
        }
    };

    const handleModalClose = () => {
        setSelectedExercise(entry.exercise || null);
        setDuration(entry.duration.toString() || '');
        setDescription(entry.description || '');
        setDurationError(null);
        onClose();
    }

    const handleSubmit = () => {
        if (!valid) { return; }

        dispatch(
            updateCardioSet({
                entryId: entry.id,
                data: {
                    exercise_id: selectedExercise.id,
                    duration: duration,
                    description: description || ''
                }
            })
        );
        onClose();
    };

    const handleDeletion = () => {
        dispatch(deleteCardioSet({ entryId: entry.id }));
        onClose();
    };

    return (
        <Dialog open = { open } onClose = { handleModalClose } fullWidth maxWidth = 'sm'>
            <DialogTitle>Modify Cardio Set</DialogTitle>

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
                <Button onClick = { handleModalClose }>Cancel</Button>
                <Button
                    variant = 'contained'
                    onClick = { handleSubmit }
                    disabled = { !valid }
                >
                    Save Set
                </Button>
                <Button
                    variant = 'contained'
                    sx = {{ backgroundColor: 'error.main' }}
                    onClick = { handleDeletion }
                    disabled = { !valid }
                >
                    Delete Entry
                </Button>
            </DialogActions>
        </Dialog>
    );
}

export default AddCardioSetModal;
