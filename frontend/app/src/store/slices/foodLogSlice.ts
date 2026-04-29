import { createSlice } from '@reduxjs/toolkit';
import type { FoodLogState } from '../../interfaces/interfaces.ts';
import { fetchFoodLogByDate, createFoodLog, createFoodEntry, updateFoodEntry, deleteFoodEntry } from '../thunks/foodLogThunk';

const initialState: FoodLogState = {
    activeLog: null,
    loading: false,
    error: null
};

const foodLogSlice = createSlice({
    name: 'foodLog',
    initialState,
    reducers: {},
    extraReducers: (builder) => {
        builder
            // FETCH LOG
            .addCase(fetchFoodLogByDate.pending, (state) => {
                state.loading = true;
            })
            .addCase(fetchFoodLogByDate.fulfilled, (state, action) => {
                state.loading = false;
                state.activeLog = action.payload;
            })
            .addCase(fetchFoodLogByDate.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload || {
                    non_field_errors: ['Unknown error']
                };
            })

            // CREATE LOG
            .addCase(createFoodLog.pending, (state) => {
                state.loading = true;
            })
            .addCase(createFoodLog.fulfilled, (state, action) => {
                state.loading = false;
                state.activeLog = action.payload;
            })
            .addCase(createFoodLog.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload || {
                    non_field_errors: ['Unknown error']
                };
            })

            // CREATE ENTRY
            .addCase(createFoodEntry.pending, (state) => {
                state.loading = true;
            })
            .addCase(createFoodEntry.fulfilled, (state) => {
                state.loading = false;
            })
            .addCase(createFoodEntry.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload || {
                    non_field_errors: ['Unknown error']
                };
            })

            // UPDATE ENTRY
            .addCase(updateFoodEntry.pending, (state) => {
                state.loading = true;
            })
            .addCase(updateFoodEntry.fulfilled, (state) => {
                state.loading = false;
            })
            .addCase(updateFoodEntry.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload || {
                    non_field_errors: ['Unknown error']
                };
            })

            // DELETE ENTRY
            .addCase(deleteFoodEntry.pending, (state) => {
                state.loading = true;
            })
            .addCase(deleteFoodEntry.fulfilled, (state) => {
                state.loading = false;
            })
            .addCase(deleteFoodEntry.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload || {
                    non_field_errors: ['Unknown error']
                };
            });
    }
});

export default foodLogSlice.reducer;