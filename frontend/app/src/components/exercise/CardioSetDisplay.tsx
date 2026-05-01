import { useState } from 'react';
import { Box, Typography, Button } from '@mui/material';
import type { CardioSetType } from '../../interfaces/interfaces.ts';
import CardioSetRow from './CardioSetRow.tsx';
import AddCardioSetModal from './AddCardioSetModal.tsx';
import { useSelector } from 'react-redux';
import type { RootState } from '../../store/store.ts';

function CardioSetDisplay() {
    const [open, setOpen] = useState(false);
    const entries: CardioSetType[] = useSelector((state: RootState) => state.cardioTraining.activeLog?.sets || []);

    return (
        <Box
            sx = {{
                backgroundColor: 'rgba(255,255,255,0.2)',
                borderRadius: 2,
                p: 1.5
            }}
        >
            <AddCardioSetModal
                open = { open }
                onClose = {() => setOpen(false)}
            />
            <Box
                sx = {{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center'
                }}
            >
                <Typography variant = 'h6'>Cardio sets</Typography>

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
                        <CardioSetRow key = { entry.id } entry = { entry } />
                    ))
                )}
            </Box>
        </Box>
    );
}

export default CardioSetDisplay;
