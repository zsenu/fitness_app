import { Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField, Box, Autocomplete } from '@mui/material';

import { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';

import type { AppDispatch, RootState } from '../../store/store';
import type { FoodItemType, MealType, FoodEntryType } from '../../interfaces/interfaces';
import { updateFoodEntry, deleteFoodEntry } from '../../store/thunks/foodLogThunk';

type ModifyEntryModalProps = {
    entry: FoodEntryType;
    open: boolean;
    onClose: () => void;
};

function ModifyFoodEntryModal({ entry, open, onClose }: ModifyEntryModalProps) {
    const dispatch = useDispatch<AppDispatch>();
    const foodLog = useSelector((state: RootState) => state.foodLog.activeLog);
    const foodItems = useSelector((state: RootState) => state.foodItem.foodItems);
    const mealType: MealType = entry.meal_type;
    const [selectedFood, setSelectedFood] = useState<FoodItemType | null>(entry.food_item || null);
    const [quantity, setQuantity] = useState(entry.quantity.toString() || '');
    const [description, setDescription] = useState(entry.description || '');
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

    const handleSubmit = () => {
        if (!valid) { return; }

        dispatch(
            updateFoodEntry({
                entryId: entry.id,
                data: {
                    meal_type: mealType,
                    food_item_id: selectedFood.id,
                    quantity,
                    description
                }
            })
        );
        onClose();
    };

    const handleDeletion = () => {
        dispatch(deleteFoodEntry({
            entryId: entry.id
        }));
        onClose();
    };

    return (
        <Dialog open = { open } onClose = { onClose } fullWidth maxWidth = 'sm'>
            <DialogTitle>Modify Entry ({ mealType })</DialogTitle>

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
                <Button onClick = { onClose }>Cancel</Button>
                <Button
                    variant = 'contained'
                    onClick = { handleSubmit }
                    disabled = { !valid }
                >
                    Save Entry
                </Button>
                <Button
                    variant = 'contained'
                    sx = {{ backgroundColor: 'error.main' }}
                    onClick = { handleDeletion }
                >
                    Delete Entry
                </Button>
            </DialogActions>
        </Dialog>
    );
}

export default ModifyFoodEntryModal;
