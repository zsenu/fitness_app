import { useState } from 'react';
import { Box } from '@mui/material';
import type { StrengthSetType } from '../../interfaces/interfaces';
import ModifyStrengthSetModal from './ModifyStrengthSetModal.tsx';

type EntryRowProps = {
    entry: StrengthSetType;
};

function StrengthSetRow({ entry }: EntryRowProps) {
    const [open, setOpen] = useState(false);

    return (
        <>
        <ModifyStrengthSetModal
                entry = { entry }
                open = { open }
                onClose = {() => setOpen(false)}
            />
        <Box
            sx = {{
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between',
                ":hover": { backgroundColor: 'action.hover', cursor: 'pointer' },
                fontSize: 14,
                py: 0.5
            }}
            onClick = {() => setOpen(true)}
        >
            <Box>
                { entry.exercise.name } ({ Number(entry.reps).toFixed(0) } x { Number(entry.weight).toFixed(2) } kg )
            </Box>
            <Box>
                { entry.exercise.target_muscle_groups.map((tg) => tg.name).join(', ') }
            </Box>
        </Box>
        </>
    );
}

export default StrengthSetRow;
