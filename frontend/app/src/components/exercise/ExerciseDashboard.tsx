import { useState } from 'react';
import { Box, Divider, Button } from '@mui/material';
import { useSelector, useDispatch } from 'react-redux';
import type { RootState, AppDispatch } from '../../store/store.ts';
import AddCardioExerciseModal from './AddCardioExerciseModal.tsx';
import AddStrengthExerciseModal from './AddStrengthExerciseModal.tsx';
import { createStrengthTraining } from '../../store/thunks/strengthTrainingThunk.ts';
import { createCardioTraining } from '../../store/thunks/cardioTrainingThunk.ts';
import StrengthSetDisplay from './StrengthSetDisplay.tsx';
import CardioSetDisplay from './CardioSetDisplay.tsx';

function ExerciseDashboard() {
    const strengthTraining = useSelector((state: RootState) => state.strengthTraining.activeLog);
    const cardioTraining = useSelector((state: RootState) => state.cardioTraining.activeLog);
    const activeDate = useSelector((state: RootState) => state.dashboard.activeDate);
    const dispatch = useDispatch<AppDispatch>();

    const [openStrengthExercise, setOpenStrengthExercise] = useState(false);
    const [openCardioExercise, setOpenCardioExercise] = useState(false);

    return (
        <Box
            sx={{
                p: 2,
                minHeight: 400,
                backgroundColor: '#94b6d6',
                borderRadius: 2,
                display: 'flex',
                flexDirection: 'column',
                gap: 2
            }}
        >
            <AddCardioExerciseModal
                open = { openCardioExercise }
                onClose = {() => setOpenCardioExercise(false)}
            />
            <AddStrengthExerciseModal
                open = { openStrengthExercise }
                onClose = {() => setOpenStrengthExercise(false)}
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
                Exercise Log
            </Box>
            {!strengthTraining ? (
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
                        No Strength Training for { activeDate }
                    </Box>
                    <Button
                        sx = {{
                            color: 'white',
                            background: '#455564'
                        }}
                        onClick = {() => {
                            dispatch(createStrengthTraining(activeDate));
                        }}
                    >
                        Create Strength Training
                    </Button>
                </>
            ) : (
                <StrengthSetDisplay />
            )}
            <Button
                onClick = {() => setOpenStrengthExercise(true)}
                variant = 'contained'
                sx = {{
                    backgroundColor: '#455564',
                    color: 'white',
                    alignSelf: 'center'
                }}
            >
                Add Strength Exercise
            </Button>
            <Divider />
            {!cardioTraining ? (
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
                        No Cardio Training for { activeDate }
                    </Box>
                    <Button
                        sx = {{
                            color: 'white',
                            background: '#455564'
                        }}
                        onClick = {() => {
                            dispatch(createCardioTraining(activeDate));
                        }}
                    >
                        Create Cardio Training
                    </Button>
                </>
            ) : (
                <CardioSetDisplay />
            )}
            <Button
                onClick = {() => setOpenCardioExercise(true)}
                variant = 'contained'
                sx = {{
                    backgroundColor: '#455564',
                    color: 'white',
                    alignSelf: 'center'
                }}
            >
                Add Cardio Exercise
            </Button>
        </Box>
    );
}

export default ExerciseDashboard;
