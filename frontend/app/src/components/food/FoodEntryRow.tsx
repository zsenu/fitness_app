import { useState } from 'react';
import { Box } from '@mui/material';
import type { FoodEntryType } from '../../interfaces/interfaces';
import ModifyFoodEntryModal from './ModifyFoodEntryModal.tsx';

type EntryRowProps = {
    entry: FoodEntryType;
};

function FoodEntryRow({ entry }: EntryRowProps) {
    const [open, setOpen] = useState(false);

    return (
        <>
        <ModifyFoodEntryModal
                entry = { entry }
                open = { open }
                onClose = {() => setOpen(false)}
            />
        <Box
            sx = {{
                display: 'flex',
                justifyContent: 'space-between',
                ":hover": { backgroundColor: 'action.hover', cursor: 'pointer' },
                fontSize: 14,
                py: 0.5
            }}
            onClick = {() => setOpen(true)}
        >
            <Box>
                { entry.food_item.name } ({ Number(entry.quantity).toFixed(2) }g)
            </Box>

            <Box>
                { (Number(entry.food_item.calories) * Number(entry.quantity) / 100).toFixed(2) } kcal
            </Box>
        </Box>
        </>
    );
}

export default FoodEntryRow;
