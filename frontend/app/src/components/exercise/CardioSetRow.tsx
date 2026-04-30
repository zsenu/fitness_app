import { useState } from 'react';
import { Box } from '@mui/material';
import type { CardioSetType } from '../../interfaces/interfaces';
import ModifyCardioSetModal from './ModifyCardioSetModal.tsx';

type EntryRowProps = {
    entry: CardioSetType;
};

function CardioSetRow({ entry }: EntryRowProps) {
    const [open, setOpen] = useState(false);

    return (
        <>
        <ModifyCardioSetModal
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
                { entry.exercise.name } ({ Number(entry.duration).toFixed(2) } minutes - { Number(entry.exercise.calories_per_minute) * Number(entry.duration) } calories)
            </Box>
        </Box>
        </>
    );
}

export default CardioSetRow;
