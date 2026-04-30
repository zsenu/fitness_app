import { useState, useEffect } from 'react';
import { Box, TextField, Button } from '@mui/material';
import { useSelector, useDispatch } from 'react-redux';
import type { RootState, AppDispatch } from '../store/store';
import type { HealthLogType } from '../interfaces/interfaces';
import { updateHealthLog, createHealthLog } from '../store/thunks/healthLogThunk';
import { fetchUserProfile } from '../store/thunks/authThunk';

function HealthDashboard() {

    const dispatch = useDispatch<AppDispatch>();

    const healthLog = useSelector((state: RootState) => state.healthLog.activeLog) as HealthLogType | null;
    const loading = useSelector((state: RootState) => state.healthLog.loading);
    const activeDate = useSelector((state: RootState) => state.dashboard.activeDate);
    const errors = useSelector((state: RootState) => state.healthLog.error);
    
    const [bodyweight, setBodyweight] = useState<string | null>(healthLog?.bodyweight?.toString() || '');
    const [hoursSlept, setHoursSlept] = useState<string | null>(healthLog?.hours_slept?.toString() || '');
    const [liquidConsumed, setLiquidConsumed] = useState<string | null>(healthLog?.liquid_consumed?.toString() || '');
    const isEditing = (
        bodyweight !== (healthLog?.bodyweight || null) ||
        hoursSlept !== (healthLog?.hours_slept || null) ||
        liquidConsumed !== (healthLog?.liquid_consumed || null)
    );
    const canBeCreated = (
        healthLog === null && (
            bodyweight !== null && bodyweight !== '' ||
            hoursSlept !== null && hoursSlept !== '' ||
            liquidConsumed !== null && liquidConsumed !== ''
        )
    );

    useEffect(() => {
        if (healthLog) {
            setBodyweight(healthLog.bodyweight ? Number(healthLog.bodyweight).toFixed(2) : null);
            setHoursSlept(healthLog.hours_slept ? Number(healthLog.hours_slept).toFixed(2) : null);
            setLiquidConsumed(healthLog.liquid_consumed ? Number(healthLog.liquid_consumed).toFixed(2) : null);
        }
        else {
            setBodyweight(null);
            setHoursSlept(null);
            setLiquidConsumed(null);
        }
    }, [activeDate, healthLog]);

    const handleSave = () => {
    
        if (healthLog) {
            const requestBody = {
                bodyweight: bodyweight ? parseFloat(bodyweight) : null,
                hours_slept: hoursSlept ? parseFloat(hoursSlept) : null,
                liquid_consumed: liquidConsumed ? parseFloat(liquidConsumed) : null
            };
            dispatch(updateHealthLog({ id: healthLog.id, data: requestBody }));
            dispatch(fetchUserProfile());
        }
        else if (bodyweight || hoursSlept || liquidConsumed) {
            const requestBody = {
                date: activeDate,
                bodyweight: bodyweight ? parseFloat(bodyweight) : null,
                hours_slept: hoursSlept ? parseFloat(hoursSlept) : null,
                liquid_consumed: liquidConsumed ? parseFloat(liquidConsumed) : null
            };
            dispatch(createHealthLog({ data: requestBody }));
            dispatch(fetchUserProfile());
        }
    }

    return (
        <Box
            sx = {{
                padding: 2,
                height: 400,
                background: '#ceb5ce',
                borderRadius: 2
            }}
        >
        <Box
            sx = {{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: 18,
                fontWeight: 'bold'
            }}
        >
            Health Log
        </Box>
        { loading ?
            <Box
                sx = {{
                    height: '100%',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: 18,
                    fontWeight: 'bold'
                }}
            >
                Loading...
            </Box>
            : healthLog ? (
            <Box
                sx = {{
                    height: '100%',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'white',
                    fontSize: 18,
                    fontWeight: 'bold',
                    gap: 1
                }}
            >
                <TextField
                    label = 'Bodyweight (kg)'
                    type = 'number'
                    value = { bodyweight ?? '' }
                    onChange = {(e) =>
                        setBodyweight(e.target.value === '' ? null : e.target.value )
                    }
                    onBlur = {() => {
                        if (bodyweight) {
                            setBodyweight(Number(bodyweight).toFixed(2));
                        }
                    }}
                    size = 'small'
                    fullWidth
                    error = { !!errors?.bodyweight }
                    helperText = { errors?.bodyweight ? errors.bodyweight.join(' ') : '' }
                />
                <TextField
                    label = 'Hours Slept'
                    value = { hoursSlept ?? '' }
                    onChange = {(e) =>
                        setHoursSlept(e.target.value)
                    }
                    onBlur = {() => {
                        if (hoursSlept) {
                            setHoursSlept(Number(hoursSlept).toFixed(2));
                        }
                    }}
                    size = 'small'
                    fullWidth
                    error = { !!errors?.hours_slept }
                    helperText = { errors?.hours_slept ? errors.hours_slept.join(' ') : '' }
                />
                <TextField
                    label = 'Liquid Consumed (L)'
                    value = { liquidConsumed ?? '' }
                    onChange = {(e) =>
                        setLiquidConsumed(e.target.value)
                    }
                    onBlur = {() => {
                        if (liquidConsumed) {
                            setLiquidConsumed(Number(liquidConsumed).toFixed(2));
                        }
                    }}
                    size = 'small'
                    fullWidth
                    error = { !!errors?.liquid_consumed }
                    helperText = { errors?.liquid_consumed ? errors.liquid_consumed.join(' ') : '' }
                />
                { isEditing && (
                    <Button
                        variant = 'contained'
                        color = 'secondary'
                        onClick = { handleSave }
                        sx = {{ background: '#746674', }}
                    >
                        Save Changes
                    </Button>
                )}
            </Box>
            )
            :
            (
            <Box
                sx = {{
                    height: '100%',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'white',
                    fontSize: 18,
                    fontWeight: 'bold',
                    gap: 1
                }}
            >
                <TextField
                    sx = {{ backgroundColor: 'transparent' }}
                    label = 'Bodyweight (kg)'
                    type = 'number'
                    value = { bodyweight ?? '' }
                    onChange = {(e) =>
                        setBodyweight(e.target.value === '' ? null : e.target.value )
                    }
                    onBlur = {() => {
                        if (bodyweight) {
                            setBodyweight(Number(bodyweight).toFixed(2));
                        }
                    }}
                    size = 'small'
                    fullWidth
                    error = { !!errors?.bodyweight }
                    helperText = { errors?.bodyweight ? errors.bodyweight.join(' ') : '' }
                />
                <TextField
                    label = 'Hours Slept'
                    value = { hoursSlept ?? '' }
                    onChange = {(e) =>
                        setHoursSlept(e.target.value)
                    }
                    onBlur = {() => {
                        if (hoursSlept) {
                            setHoursSlept(Number(hoursSlept).toFixed(2));
                        }
                    }}
                    size = 'small'
                    fullWidth
                    error = { !!errors?.hours_slept }
                    helperText = { errors?.hours_slept ? errors.hours_slept.join(' ') : '' }
                />
                <TextField
                    label = 'Liquid Consumed (L)'
                    value = { liquidConsumed ?? '' }
                    onChange = {(e) =>
                        setLiquidConsumed(e.target.value)
                    }
                    onBlur = {() => {
                        if (liquidConsumed) {
                            setLiquidConsumed(Number(liquidConsumed).toFixed(2));
                        }
                    }}
                    size = 'small'
                    fullWidth
                    error = { !!errors?.liquid_consumed }
                    helperText = { errors?.liquid_consumed ? errors.liquid_consumed.join(' ') : '' }
                />
                { canBeCreated &&
                    <Button
                        variant = 'contained'
                        color = 'secondary'
                        onClick = { handleSave }
                        sx = {{ background: '#746674', }}
                    >
                        No Log Present - Click to Create.
                    </Button>
                }
            </Box>
            )
        }
        </Box>
    );
}

export default HealthDashboard;