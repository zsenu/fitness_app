import { useState } from 'react';
import { Box, Typography, Divider, Button } from '@mui/material';
import { useSelector, useDispatch } from 'react-redux';
import type { RootState, AppDispatch } from '../../store/store.ts';
import type { MealType, FoodEntryType, MacrosType } from '../../interfaces/interfaces.ts';
import MealSection from './MealSelection.tsx';
import MacrosDisplay from './MacrosDisplay.tsx';
import { createFoodLog } from '../../store/thunks/foodLogThunk.ts';
import AddFoodItemModal from './AddFoodItemModal.tsx';

const meals: MealType[] = ['breakfast', 'lunch', 'dinner', 'misc'];

function FoodDashboard() {
    const foodLog = useSelector((state: RootState) => state.foodLog.activeLog);
    const activeDate = useSelector((state: RootState) => state.dashboard.activeDate);
    const dispatch = useDispatch<AppDispatch>();

    const [open, setOpen] = useState(false);

    return (
        <Box
            sx={{
                p: 2,
                minHeight: 300,
                backgroundColor: '#caaa8d',
                borderRadius: 2,
                display: 'flex',
                flexDirection: 'column',
                gap: 2
            }}
        >
            <AddFoodItemModal
                open = { open }
                onClose = {() => setOpen(false)}
            />
            <Box
                sx = {{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: 18,
                    fontWeight: 'bold'
                }}
            >
                Food Log
            </Box>
            {!foodLog ? (
                <>
                    <Box
                        sx = {{
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            fontSize: 18,
                            fontWeight: 'bold'
                        }}
                    >
                        No log for { activeDate }
                    </Box>
                    <Button
                        sx = {{
                            color: 'white',
                            background: '#6b5b4c'
                        }}
                        onClick = {() => {
                            dispatch(createFoodLog(activeDate));
                        }}
                    >
                        Create Food Log
                    </Button>
                </>
            ) : (
                <>
                    { meals.map((meal) => {
                        const entries: FoodEntryType[] = foodLog.entries.filter(
                            (e) => e.meal_type === meal
                        );

                        const macros: MacrosType =
                            foodLog[`${meal}_macros` as const];

                        return (
                            <MealSection
                                key = { meal }
                                title = { capitalize(meal) }
                                mealType = { meal }
                                entries = { entries }
                                macros = { macros }
                            />
                        );
                    })}

                    <Divider />

                    <Box>
                        <Typography variant = 'h6'>Total</Typography>
                        <MacrosDisplay macros = { foodLog.total_macros } />
                    </Box>
                    <Button
                        onClick = {() => setOpen(true)}
                        variant = 'contained'
                        sx = {{
                            backgroundColor: '#6b5b4c',
                            color: 'white',
                            alignSelf: 'center'
                        }}
                    >
                        Add Food Item
                    </Button>
                </>
            )}
        </Box>
    );
}

export default FoodDashboard;

const capitalize = (str: string) =>
    str.charAt(0).toUpperCase() + str.slice(1);
