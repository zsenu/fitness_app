import { createSlice } from '@reduxjs/toolkit';
import type { CardioLogState } from '../../interfaces/interfaces.ts';
import { fetchCardioTrainingByDate, createCardioTraining, createCardioSet, updateCardioSet, deleteCardioSet } from '../thunks/cardioTrainingThunk.ts';
const initialState: CardioLogState = {
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
            .addCase(fetchCardioTrainingByDate.pending, (state) => {
                state.loading = true;
            })
            .addCase(fetchCardioTrainingByDate.fulfilled, (state, action) => {
                state.loading = false;
                state.activeLog = action.payload;
            })
            .addCase(fetchCardioTrainingByDate.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload || {
                    non_field_errors: ['Unknown error']
                };
            })

            // CREATE LOG
            .addCase(createCardioTraining.pending, (state) => {
                state.loading = true;
            })
            .addCase(createCardioTraining.fulfilled, (state, action) => {
                state.loading = false;
                state.activeLog = action.payload;
            })
            .addCase(createCardioTraining.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload || {
                    non_field_errors: ['Unknown error']
                };
            })

            // CREATE ENTRY
            .addCase(createCardioSet.pending, (state) => {
                state.loading = true;
            })
            .addCase(createCardioSet.fulfilled, (state) => {
                state.loading = false;
            })
            .addCase(createCardioSet.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload || {
                    non_field_errors: ['Unknown error']
                };
            })

            // UPDATE ENTRY
            .addCase(updateCardioSet.pending, (state) => {
                state.loading = true;
            })
            .addCase(updateCardioSet.fulfilled, (state) => {
                state.loading = false;
            })
            .addCase(updateCardioSet.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload || {
                    non_field_errors: ['Unknown error']
                };
            })

            // DELETE ENTRY
            .addCase(deleteCardioSet.pending, (state) => {
                state.loading = true;
            })
            .addCase(deleteCardioSet.fulfilled, (state) => {
                state.loading = false;
            })
            .addCase(deleteCardioSet.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload || {
                    non_field_errors: ['Unknown error']
                };
            });
    }
});

export default foodLogSlice.reducer;
