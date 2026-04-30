import { createSlice } from '@reduxjs/toolkit';
import type { StrengthLogState } from '../../interfaces/interfaces.ts';
import { fetchStrengthTrainingByDate, createStrengthTraining, createStrengthSet, updateStrengthSet, deleteStrengthSet } from '../thunks/strengthTrainingThunk.ts';
const initialState: StrengthLogState = {
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
            .addCase(fetchStrengthTrainingByDate.pending, (state) => {
                state.loading = true;
            })
            .addCase(fetchStrengthTrainingByDate.fulfilled, (state, action) => {
                state.loading = false;
                state.activeLog = action.payload;
            })
            .addCase(fetchStrengthTrainingByDate.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload || {
                    non_field_errors: ['Unknown error']
                };
            })

            // CREATE LOG
            .addCase(createStrengthTraining.pending, (state) => {
                state.loading = true;
            })
            .addCase(createStrengthTraining.fulfilled, (state, action) => {
                state.loading = false;
                state.activeLog = action.payload;
            })
            .addCase(createStrengthTraining.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload || {
                    non_field_errors: ['Unknown error']
                };
            })

            // CREATE ENTRY
            .addCase(createStrengthSet.pending, (state) => {
                state.loading = true;
            })
            .addCase(createStrengthSet.fulfilled, (state) => {
                state.loading = false;
            })
            .addCase(createStrengthSet.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload || {
                    non_field_errors: ['Unknown error']
                };
            })

            // UPDATE ENTRY
            .addCase(updateStrengthSet.pending, (state) => {
                state.loading = true;
            })
            .addCase(updateStrengthSet.fulfilled, (state) => {
                state.loading = false;
            })
            .addCase(updateStrengthSet.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload || {
                    non_field_errors: ['Unknown error']
                };
            })

            // DELETE ENTRY
            .addCase(deleteStrengthSet.pending, (state) => {
                state.loading = true;
            })
            .addCase(deleteStrengthSet.fulfilled, (state) => {
                state.loading = false;
            })
            .addCase(deleteStrengthSet.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload || {
                    non_field_errors: ['Unknown error']
                };
            });
    }
});

export default foodLogSlice.reducer;
