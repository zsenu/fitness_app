import { Box } from '@mui/material';
import type { FoodEntryType } from '../interfaces/interfaces';

type EntryRowProps = {
    entry: FoodEntryType;
};

function EntryRow({ entry }: EntryRowProps) {
    return (
        <Box
            sx = {{
                display: 'flex',
                justifyContent: 'space-between',
                fontSize: 14,
                py: 0.5
            }}
        >
            <Box>
                { entry.food_item.name } ({ Number(entry.quantity).toFixed(2) }g)
            </Box>

            <Box>
                { (Number(entry.food_item.calories) * Number(entry.quantity) / 100).toFixed(2) } kcal
            </Box>
        </Box>
    );
}

export default EntryRow;
