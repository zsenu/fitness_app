import { Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField, Box, Autocomplete } from '@mui/material';

import { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';

import type { AppDispatch, RootState } from '../../store/store';
import type { StrengthExerciseType, StrengthSetType } from '../../interfaces/interfaces';
import { updateStrengthSet, deleteStrengthSet } from '../../store/thunks/strengthTrainingThunk';

type ModifyEntryModalProps = {
    entry: StrengthSetType;
    open: boolean;
    onClose: () => void;
};

function AddStrengthSetModal({ entry, open, onClose }: ModifyEntryModalProps) {
    const dispatch = useDispatch<AppDispatch>();
    const strengthExercises = useSelector((state: RootState) => state.strengthExercise.exercises);
    const [selectedExercise, setSelectedExercise] = useState<StrengthExerciseType | null>(entry.exercise || null);
    const [reps, setReps] = useState(entry.reps.toString() || '');
    const [weight, setWeight] = useState(entry.weight.toString() || '');
    const [description, setDescription] = useState(entry.description || '');
    const [repsError, setRepsError] = useState<string | null>(null);
    const [weightError, setWeightError] = useState<string | null>(null);
    const valid = !!selectedExercise && !!reps && !!weight && !repsError && !weightError;

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

    const handleSubmit = () => {
        if (!valid) { return; }

        dispatch(
            updateStrengthSet({
                entryId: entry.id,
                data: {
                    exercise_id: selectedExercise.id,
                    reps: Number(reps),
                    weight: weight,
                    description: description || ''
                }
            })
        );
        onClose();
    };

    const handleDeletion = () => {
        dispatch(deleteStrengthSet({ entryId: entry.id }));
        onClose();
    };

    return (
        <Dialog open = { open } onClose = { onClose } fullWidth maxWidth = 'sm'>
            <DialogTitle>Modify Strength Set</DialogTitle>

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
                <Button onClick = { onClose }>Cancel</Button>
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

export default AddStrengthSetModal;
