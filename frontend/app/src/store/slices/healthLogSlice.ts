import { createSlice }    from '@reduxjs/toolkit';
import type { HealthLogState } from '../../interfaces/interfaces.ts';
import { fetchHealthLogByDate, updateHealthLog, createHealthLog } from '../thunks/healthLogThunk';

const initialState: HealthLogState = {
    activeLog: null,
    loading: false,
    error: null
};

const healthLogSlice = createSlice({
    name: 'healthLog',
    initialState,
    reducers: {
        clearHealthLog(state) {
            state.activeLog = null;
            state.error = null;
        }
    },
    extraReducers: (builder) => {
        builder
            // FETCH
            .addCase(fetchHealthLogByDate.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchHealthLogByDate.fulfilled, (state, action) => {
                state.loading = false;
                state.activeLog = action.payload;
            })
            .addCase(fetchHealthLogByDate.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload || {
                    non_field_errors: ['Unknown error']
                };
            })

            // UPDATE
            .addCase(updateHealthLog.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(updateHealthLog.fulfilled, (state, action) => {
                state.loading = false;
                state.activeLog = action.payload;
            })
            .addCase(updateHealthLog.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload || {
                    non_field_errors: ['Unknown error']
                };
            })

            // CREATE
            .addCase(createHealthLog.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(createHealthLog.fulfilled, (state, action) => {
                state.loading = false;
                state.activeLog = action.payload;
            })
            .addCase(createHealthLog.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload || {
                    non_field_errors: ['Unknown error']
                };
            });
        }
});

export const { clearHealthLog } = healthLogSlice.actions;
export default healthLogSlice.reducer;
