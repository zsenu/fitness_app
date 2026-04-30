import { useState } from 'react';
import { Box, Typography, Button } from '@mui/material';
import type { FoodEntryType, MacrosType, MealType } from '../../interfaces/interfaces.ts';
import MacrosDisplay from './MacrosDisplay.tsx';
import FoodEntryRow from './FoodEntryRow.tsx';
import AddFoodEntryModal from './AddFoodEntryModal.tsx';

type MealSectionProps = {
    title: string;
    mealType: MealType;
    entries: FoodEntryType[];
    macros: MacrosType;
};

function MealSection({ title, mealType, entries, macros, }: MealSectionProps) {
    const [open, setOpen] = useState(false);

    return (
        <Box
            sx = {{
                backgroundColor: 'rgba(255,255,255,0.2)',
                borderRadius: 2,
                p: 1.5
            }}
        >
            <AddFoodEntryModal
                open = { open }
                onClose = {() => setOpen(false)}
                mealType = { mealType }
            />
            <Box
                sx = {{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center'
                }}
            >
                <Typography variant = 'h6'>{ title }</Typography>

                <Button
                    size = 'small'
                    variant = 'contained'
                    onClick = {() => setOpen(true)}
                >
                    Add
                </Button>
            </Box>

            <Box sx = {{ mt: 1 }}>
                { entries.length === 0 ? (
                    <Typography variant = 'body2'>No entries</Typography>
                ) : (
                    entries.map((entry) => (
                        <FoodEntryRow key = { entry.id } entry = { entry } />
                    ))
                )}
            </Box>

            <Box sx = {{ mt: 1 }}>
                <MacrosDisplay macros = { macros } />
            </Box>
        </Box>
    );
}

export default MealSection;