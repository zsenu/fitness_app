import { Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField, Box, Autocomplete } from '@mui/material';

import { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';

import type { AppDispatch, RootState } from '../../store/store';
import type { StrengthExerciseType } from '../../interfaces/interfaces';
import { createStrengthSet } from '../../store/thunks/strengthTrainingThunk';

type AddEntryModalProps = {
    open: boolean;
    onClose: () => void;
};

function AddStrengthSetModal({ open, onClose }: AddEntryModalProps) {
    const dispatch = useDispatch<AppDispatch>();
    const strengthTraining = useSelector((state: RootState) => state.strengthTraining.activeLog);
    const strengthExercises = useSelector((state: RootState) => state.strengthExercise.exercises);
    const [selectedExercise, setSelectedExercise] = useState<StrengthExerciseType | null>(null);
    const [reps, setReps] = useState('');
    const [weight, setWeight] = useState('');
    const [description, setDescription] = useState('');
    const [repsError, setRepsError] = useState<string | null>(null);
    const [weightError, setWeightError] = useState<string | null>(null);
    const valid = !!strengthTraining && !!selectedExercise && !!reps && !!weight && !repsError && !weightError;

    const handleRepsChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;
        setReps(value);
        setRepsError(null);

        if (Number(value) < 1) {
            setRepsError('You must perform at least 1 repetition.');
            return;
        }
    };

    const handleWeightChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;
        setWeight(value);
        setWeightError(null);

        if (!(0 < Number(value) && Number(value) < 1000)) {
            setWeightError('Weight must be between 0 and 1000 kg.');
            return;
        }
    };

    const handleCloseModal = () => {
        setSelectedExercise(null);
        setReps('');
        setWeight('');
        setDescription('');
        onClose();
    }

    const handleSubmit = () => {
        if (!valid) { return; }

        dispatch(
            createStrengthSet({
                logId: strengthTraining.id,
                data: {
                    exercise_id: selectedExercise.id,
                    reps: Number(reps),
                    weight: weight,
                    description: description || ''
                }
            })
        );
        handleCloseModal();
    };

    return (
        <Dialog open = { open } onClose = { handleCloseModal } fullWidth maxWidth = 'sm'>
            <DialogTitle>Add Strength Set</DialogTitle>

            <DialogContent>
                <Box sx = {{ display: 'flex', flexDirection: 'column', gap: 2, mt: 1 }}>

                    <Autocomplete
                        options = { strengthExercises }
                        getOptionLabel = {(option) => option.name + (option.description ? ` - ${option.description}` : '')}
                        value = { selectedExercise }
                        onChange = {(_, value) => setSelectedExercise(value)}
                        renderInput = {(params) => (
                            <TextField { ...params } label = 'Strength Exercise' />
                        )}
                    />

                    <TextField
                        label = 'Repetitions'
                        type = 'number'
                        value = { reps }
                        onChange = { handleRepsChange }
                        error = { !!repsError }
                        helperText = { repsError }
                    />
                    <TextField
                        label = 'Weight (kg)'
                        type = 'number'
                        value = { weight }
                        onChange = { handleWeightChange }
                        error = { !!weightError }
                        helperText = { weightError }
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

export default AddStrengthSetModal;
