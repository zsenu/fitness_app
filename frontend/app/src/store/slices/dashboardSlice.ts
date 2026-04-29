import { createSlice }    from '@reduxjs/toolkit';
import type { DashboardState } from '../../interfaces/interfaces.ts';

const initialState: DashboardState = {
    activeDate: new Date().toISOString().split('T')[0] // YYYY-MM-DD
};

const validateDate = (dateStr: string): boolean => {
    // action.payload must be between [2026-01-01, tomorrow], otherwise ignore
    const maxDate = new Date();
    maxDate.setDate(new Date().getDate() + 1);
    const minDate = new Date('2026-01-01');
    const newDate = new Date(dateStr);
    return (minDate <= newDate && newDate < maxDate);
}

const dashboardSlice = createSlice({
    name: 'dashboard',
    initialState,
    reducers: {
        incrementDate(state) {
            const targetDate = new Date(state.activeDate);
            targetDate.setDate(targetDate.getDate() + 1);
            const newDateStr = targetDate.toISOString().split('T')[0];
            if (validateDate(newDateStr)) {
                state.activeDate = newDateStr;
            }
        },
        decrementDate(state) {
            const targetDate = new Date(state.activeDate);
            targetDate.setDate(targetDate.getDate() - 1);
            const newDateStr = targetDate.toISOString().split('T')[0];
            if (validateDate(newDateStr)) {
                state.activeDate = newDateStr;
            }
        },
        setActiveDate(state, action) {
            if (validateDate(action.payload)) {
                state.activeDate = action.payload;
            }
        }
    }
});

export const { incrementDate, decrementDate, setActiveDate } = dashboardSlice.actions;
export default dashboardSlice.reducer;
