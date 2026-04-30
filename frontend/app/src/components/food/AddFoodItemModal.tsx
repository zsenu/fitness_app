import { Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField, Box } from '@mui/material';

import { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';

import type { AppDispatch, RootState } from '../../store/store';
import { createFoodItem } from '../../store/thunks/foodItemThunk';

type AddItemModalProps = {
    open: boolean;
    onClose: () => void;
};

function AddFoodItemModal({ open, onClose }: AddItemModalProps) {
    const foodItems = useSelector((state: RootState) => state.foodItem.foodItems);
    const dispatch = useDispatch<AppDispatch>();

    const [name, setName] = useState('');
    const [nameError, setNameError] = useState<string | null>(null);

    const [description, setDescription] = useState('');

    const [calories, setCalories] = useState('');
    const [caloriesError, setCaloriesError] = useState<string | null>(null);

    const [fat, setFat] = useState('');
    const [fatError, setFatError] = useState<string | null>(null);

    const [carbohydrates, setCarbohydrates] = useState('');
    const [carbohydratesError, setCarbohydratesError] = useState<string | null>(null);

    const [protein, setProtein] = useState('');
    const [proteinError, setProteinError] = useState<string | null>(null);

    const wrongTotalNutrients: boolean = Number(fat) + Number(carbohydrates) + Number(protein) > 100;
    const valid: boolean = name !== '' && calories !== '' && !nameError && !caloriesError && !fatError && !carbohydratesError && !proteinError && !wrongTotalNutrients;

    const handleNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setNameError(null);

        if (foodItems.some(item => item.name.toLowerCase() === e.target.value.toLowerCase())) {
            setNameError('A food item with this name already exists');
        }
        
        setName(e.target.value);
    };

    const handleCaloriesChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setCaloriesError(null);

        const value = e.target.value;
        if (!(0 < Number(value) && Number(value) < 2000)) {
            setCaloriesError('Calories per 100g must be between 0 and 2000.');
        }
        
        setCalories(value);
    };

    const handleFatChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFatError(null);

        const value = e.target.value;
        if (!(0 <= Number(value) && Number(value) <= 100)) {
            setFatError('Fat content per 100g must be between 0 and 100g.');
        }

        setFat(value);
    };

    const handleCarbohydratesChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setCarbohydratesError(null);

        const value = e.target.value;
        if (!(0 <= Number(value) && Number(value) <= 100)) {
            setCarbohydratesError('Carbohydrates content per 100g must be between 0 and 100g.');
        }

        setCarbohydrates(value);
    };

    const handleProteinChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setProteinError(null);

        const value = e.target.value;
        if (!(0 <= Number(value) && Number(value) <= 100)) {
            setProteinError('Protein content per 100g must be between 0 and 100g.');
        }

        setProtein(value);
    };


    const handleSubmit = () => {
        if (!valid) { return; }

        dispatch(
            createFoodItem({
                name: name,
                description: description,
                calories: calories,
                fat: fat,
                carbohydrates: carbohydrates,
                protein: protein
            })
        );

        onClose();
    };

    return (
        <Dialog open = { open } onClose = { onClose } fullWidth maxWidth = 'sm'>
            <DialogTitle>Add Food Item</DialogTitle>

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
                        label = 'Calories per 100g'
                        type = 'number'
                        value = { calories }
                        onChange = { handleCaloriesChange }
                        error = { !!caloriesError }
                        helperText = { caloriesError }
                    />
                    <TextField
                        label = 'Fat per 100g'
                        type = 'number'
                        value = { fat }
                        onChange = { handleFatChange }
                        error = { !!fatError }
                        helperText = { fatError }
                    />
                    <TextField
                        label = 'Carbohydrates per 100g'
                        type = 'number'
                        value = { carbohydrates }
                        onChange = { handleCarbohydratesChange }
                        error = { !!carbohydratesError }
                        helperText = { carbohydratesError }
                    />
                    <TextField
                        label = 'Protein per 100g'
                        type = 'number'
                        value = { protein }
                        onChange = { handleProteinChange }
                        error = { !!proteinError }
                        helperText = { proteinError }
                    />
                    { wrongTotalNutrients && <Box sx = {{ color: 'error.main' }}>The sum of fat, carbohydrates and protein cannot exceed 100g per 100g of the food item.</Box> }
                </Box>
            </DialogContent>

            <DialogActions>
                <Button onClick = { onClose }>Cancel</Button>
                <Button
                    variant = 'contained'
                    onClick = { handleSubmit }
                    disabled = { !valid }
                >
                    Add Item
                </Button>
            </DialogActions>
        </Dialog>
    );
}

export default AddFoodItemModal;
