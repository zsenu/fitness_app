import { useState } from 'react';
import { Box, Typography, Button } from '@mui/material';
import type { StrengthSetType } from '../../interfaces/interfaces.ts';
import StrengthSetRow from './StrengthSetRow.tsx';
import AddStrengthSetModal from './AddStrengthSetModal.tsx';
import { useSelector } from 'react-redux';
import type { RootState } from '../../store/store.ts';

function StrengthSetDisplay() {
    const [open, setOpen] = useState(false);
    const entries: StrengthSetType[] = useSelector((state: RootState) => state.strengthTraining.activeLog?.sets || []);

    return (
        <Box
            sx = {{
                backgroundColor: 'rgba(255,255,255,0.2)',
                borderRadius: 2,
                p: 1.5
            }}
        >
            <AddStrengthSetModal
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
                <Typography variant = 'h6'>Strength exercises</Typography>

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
                        <StrengthSetRow key = { entry.id } entry = { entry } />
                    ))
                )}
            </Box>
        </Box>
    );
}

export default StrengthSetDisplay;
