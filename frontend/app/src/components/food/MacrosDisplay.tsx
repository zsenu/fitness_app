import { Box } from '@mui/material';
import type { MacrosType } from '../../interfaces/interfaces';

type MacrosDisplayProps = {
    macros: MacrosType;
};

function MacrosDisplay({ macros }: MacrosDisplayProps) {

    return (
        <Box
            sx = {{
                display: 'flex',
                gap: 2,
                fontSize: 12,
                opacity: 0.8
            }}
        >
            <Box>Cal: { macros.calories.toFixed(2) }</Box>
            <Box>Fat: { macros.fat.toFixed(2) }</Box>
            <Box>Carbs: { macros.carbohydrates.toFixed(2) }</Box>
            <Box>Protein: { macros.protein.toFixed(2) }</Box>

        </Box>
    );
}

export default MacrosDisplay;
