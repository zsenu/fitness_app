import { Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField, Box, Autocomplete } from '@mui/material';

import { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';

import type { AppDispatch, RootState } from '../../store/store';
import type { FoodItemType, MealType } from '../../interfaces/interfaces';
import { createFoodEntry } from '../../store/thunks/foodLogThunk';

type AddEntryModalProps = {
    open: boolean;
    onClose: () => void;
    mealType: MealType;
};

function AddFoodEntryModal({ open, onClose, mealType }: AddEntryModalProps) {
    const dispatch = useDispatch<AppDispatch>();
    const foodLog = useSelector((state: RootState) => state.foodLog.activeLog);
    const foodItems = useSelector((state: RootState) => state.foodItem.foodItems);
    const [selectedFood, setSelectedFood] = useState<FoodItemType | null>(null);
    const [quantity, setQuantity] = useState('');
    const [description, setDescription] = useState('');
    const [foodError, setFoodError] = useState<string | null>(null);
    const [quantityError, setQuantityError] = useState<string | null>(null);
    const valid = !!foodLog && !!selectedFood && !!quantity && !foodError && !quantityError;

    const handleQuantityChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;
        setQuantity(value);
        setQuantityError(null);

        if (Number(value) < 0.1) {
            setQuantityError('Quantity must be at least 0.1 grams');
            return;
        }
    };

    const handleFoodChange = (value: FoodItemType | null) => {
        setFoodError(null);
        setSelectedFood(value);
        if (!foodLog || !value) { return; }
        const present_foods = (foodLog.entries.filter(entry => entry.meal_type === mealType).map(entry => entry.food_item.id));
        
        if (present_foods.includes(Number(value.id))) {
            setFoodError('This food item has already been added for this meal type');
        }
    }

    const handleCloseModal = () => {
        setSelectedFood(null);
        setQuantity('');
        setDescription('');
        onClose();
    };

    const handleSubmit = () => {
        if (!valid) { return; }

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
        handleCloseModal();
    };

    return (
        <Dialog open = { open } onClose = { handleCloseModal } fullWidth maxWidth = 'sm'>
            <DialogTitle>Add Entry ({ mealType })</DialogTitle>

            <DialogContent>
                <Box sx = {{ display: 'flex', flexDirection: 'column', gap: 2, mt: 1 }}>

                    <Autocomplete
                        options = { foodItems }
                        getOptionLabel = {(option) => option.name + (option.description ? ` - ${option.description}` : '')}
                        value = { selectedFood }
                        onChange = {(_, value) => handleFoodChange(value)}
                        renderInput = {(params) => (
                            <TextField { ...params } label = 'Food Item' />
                        )}
                    />
                    { !!foodError && <Box sx = {{ color: 'error.main' }}>{ foodError }</Box> }

                    <TextField
                        label = 'Quantity (grams)'
                        type = 'number'
                        value = { quantity }
                        onChange = { handleQuantityChange }
                        error = { !!quantityError }
                        helperText = { quantityError }
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
                    Add Entry
                </Button>
            </DialogActions>
        </Dialog>
    );
}

export default AddFoodEntryModal;
