import { Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField, Box } from '@mui/material';

import { Autocomplete } from '@mui/material';
import { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';

import type { AppDispatch, RootState } from '../store/store';
import type { FoodItemType, MealType } from '../interfaces/interfaces';
import { createFoodEntry } from '../store/thunks/foodLogThunk';

type AddEntryModalProps = {
    open: boolean;
    onClose: () => void;
    mealType: MealType;
};

function AddFoodEntryModal({ open, onClose, mealType }: AddEntryModalProps) {
    const dispatch = useDispatch<AppDispatch>();
    const foodLog = useSelector((state: RootState) => state.foodLog.activeLog);

    const [selectedFood, setSelectedFood] = useState<FoodItemType | null>(null);
    const [quantity, setQuantity] = useState('');
    const [description, setDescription] = useState('');

    // TODO: replace with real API data
    const foodOptions: FoodItemType[] = [
        { id: 1, name: 'Apple', description: '', calories: '52', fat: '0.2', carbohydrates: '14', protein: '0.3' },
        { id: 2, name: 'Chicken Breast', description: '', calories: '165', fat: '3.6', carbohydrates: '0', protein: '31' }
    ];

    const handleSubmit = () => {
        if (!foodLog || !selectedFood || !quantity) { return; }

        dispatch(
            createFoodEntry({
                logId: foodLog.id,
                data: {
                    meal_type: mealType,
                    food_item_id: selectedFood.id,
                    quantity,
                    description
                }
            })
        );

        setSelectedFood(null);
        setQuantity('');
        setDescription('');

        onClose();
    };

    return (
        <Dialog open = { open } onClose = { onClose } fullWidth maxWidth = 'sm'>
            <DialogTitle>Add Entry ({ mealType })</DialogTitle>

            <DialogContent>
                <Box sx = {{ display: 'flex', flexDirection: 'column', gap: 2, mt: 1 }}>

                    <Autocomplete
                        options = { foodOptions }
                        getOptionLabel = {(option) => option.name}
                        value = { selectedFood }
                        onChange = {(_, value) => setSelectedFood(value)}
                        renderInput = {(params) => (
                            <TextField { ...params } label = 'Food Item' />
                        )}
                    />

                    <TextField
                        label = 'Quantity (grams)'
                        type = 'number'
                        value = { quantity }
                        onChange = {(e) => setQuantity(e.target.value)}
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
                    disabled = { !selectedFood || !quantity }
                >
                    Add Entry
                </Button>
            </DialogActions>
        </Dialog>
    );
}

export default AddFoodEntryModal;
