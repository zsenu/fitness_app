import { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import type { RootState, AppDispatch } from '../store/store';
import { incrementDate, decrementDate, setActiveDate } from '../store/slices/dashboardSlice.ts';
import { AppBar, Toolbar, IconButton, Typography, Box, Dialog } from '@mui/material';

import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import CalendarMonthIcon from '@mui/icons-material/CalendarMonth';

import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';

const getMinDate = () => {
    return new Date('2026-01-01');
};

const getMaxDate = () => {
    const maxDate = new Date();
    maxDate.setDate(maxDate.getDate() + 1);
    return maxDate;
};

const DateSelector = () => {
    const dispatch = useDispatch<AppDispatch>();
    const activeDate = useSelector(
        (state: RootState) => state.dashboard.activeDate
    );

    const [open, setOpen] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const parsedDate = new Date(activeDate);

    const nextDate = new Date(parsedDate);
    nextDate.setDate(nextDate.getDate() + 1);
    const nextButtonDisabled = nextDate >= getMaxDate();

    const prevDate = new Date(parsedDate);
    prevDate.setDate(prevDate.getDate() - 1);
    const prevButtonDisabled = prevDate < getMinDate();

    const handleCalendarChange = (newValue: Date | null) => {
        if (newValue) {
            const minDate = getMinDate();
            const maxDate = getMaxDate();
            if (newValue < minDate) {
                setError('Active date cannot be before 2026-01-01.');
                return;
            }
            if (newValue >= maxDate) {
                setError('Active date cannot be more than one day in the future.');
                return;
            }
            setError(null);
            const iso = newValue.toISOString().split('T')[0];
            dispatch(setActiveDate(iso));
        }
    };

    return (
        <>
            <AppBar
                position = 'static'
                elevation = { 0 }
                sx = {{
                    background: 'transparent',
                    color: 'inherit'
                }}
            >
                <Toolbar sx = {{ justifyContent: 'space-between' }}>
                    
                    <IconButton disabled = { prevButtonDisabled } onClick = {() => { dispatch(decrementDate()); }}>
                        <ChevronLeftIcon />
                    </IconButton>

                    <Box
                        sx = {{
                            display: 'flex',
                            alignItems: 'center',
                            gap: 1,
                            cursor: 'pointer'
                        }}
                        onClick = {() => setOpen(true)}
                    >
                        <Typography variant = 'h6'>
                            { activeDate }
                        </Typography>

                        <IconButton size = 'small'>
                            <CalendarMonthIcon />
                        </IconButton>
                    </Box>

                    <IconButton disabled = { nextButtonDisabled } onClick = {() => { dispatch(incrementDate()); }}>
                        <ChevronRightIcon />
                    </IconButton>
                </Toolbar>
            </AppBar>

            <Dialog open = { open } onClose = {() => setOpen(false)}>
                <Box sx = {{ p: 2 }}>
                    <LocalizationProvider dateAdapter = { AdapterDateFns }>
                        <DatePicker
                            value = { parsedDate }
                            onChange = { handleCalendarChange }
                            disableFuture = { false }
                        />
                        { !!error && <Typography color = 'error' sx = {{ mt: 1 }}>{ error }</Typography> }
                    </LocalizationProvider>
                </Box>
            </Dialog>
        </>
    );
};

export default DateSelector;