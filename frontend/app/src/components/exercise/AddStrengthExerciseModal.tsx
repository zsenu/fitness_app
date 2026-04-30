import { Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField, Box, Autocomplete } from '@mui/material';

import { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';

import type { AppDispatch, RootState } from '../../store/store';
import { createStrengthExercise } from '../../store/thunks/strengthExerciseThunk';

import type { MuscleGroupType } from '../../interfaces/interfaces';

type AddItemModalProps = {
    open: boolean;
    onClose: () => void;
};

function AddStrengthExerciseModal({ open, onClose }: AddItemModalProps) {
    const muscleGroups = useSelector((state: RootState) => state.strengthExercise.muscleGroups);
    const strengthExercises = useSelector((state: RootState) => state.strengthExercise.exercises);
    const dispatch = useDispatch<AppDispatch>();

    const [name, setName] = useState('');
    const [nameError, setNameError] = useState<string | null>(null);

    const [description, setDescription] = useState('');

    const [targetMuscleGroups, setTargetMuscleGroups] = useState<MuscleGroupType[]>([]);

    const valid: boolean = name !== '' && !nameError;

    const handleNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setNameError(null);

        if (strengthExercises.some(item => item.name.toLowerCase() === e.target.value.toLowerCase())) {
            setNameError('A cardio exercise with this name already exists');
        }
        
        setName(e.target.value);
    };

    const handleSubmit = () => {
        if (!valid) { return; }

        dispatch(
            createStrengthExercise({
                name: name,
                description: description,
                target_muscle_group_ids: targetMuscleGroups.map(g => g.id)
            })
        );

        setName('');
        setDescription('');
        setTargetMuscleGroups([]);

        onClose();
    };

    return (
        <Dialog open = { open } onClose = { onClose } fullWidth maxWidth = 'sm'>
            <DialogTitle>Add Strength Exercise</DialogTitle>

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

                    <Autocomplete
                        multiple
                        options = { muscleGroups }
                        getOptionLabel = { (option) => option.name }
                        value = { targetMuscleGroups }
                        onChange = {(_, value) => setTargetMuscleGroups(value)}
                        renderInput = {(params) => (
                            <TextField { ...params } label = 'Target muscle groups' />
                        )}
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
                    Add Exercise
                </Button>
            </DialogActions>
        </Dialog>
    );
}

export default AddStrengthExerciseModal;
