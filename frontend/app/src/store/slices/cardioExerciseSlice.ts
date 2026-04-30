import { createSlice } from '@reduxjs/toolkit';
import type { CardioExerciseState } from '../../interfaces/interfaces.ts';
import { fetchAllCardioExercises, createCardioExercise } from '../thunks/cardioExerciseThunk.ts';

const initialState: CardioExerciseState = {
    exercises: [],
    loading: false,
    error: null
};

const cardioExerciseSlice = createSlice({
    name: 'cardioExercise',
    initialState,
    reducers: {},
    extraReducers: (builder) => {
        builder
            .addCase(fetchAllCardioExercises.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchAllCardioExercises.fulfilled, (state, action) => {
                state.exercises = action.payload || [];
                state.loading = false;
            })
            .addCase(fetchAllCardioExercises.rejected, (state, action) => {
                state.error = action.payload || { detail: ['Failed to fetch cardio exercises.'] };
                state.loading = false;
            })
            .addCase(createCardioExercise.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(createCardioExercise.fulfilled, (state, action) => {
                state.exercises = action.payload || [];
                state.loading = false;
            })
            .addCase(createCardioExercise.rejected, (state, action) => {
                state.error = action.payload || { detail: ['Failed to create cardio exercise.'] };
                state.loading = false;
            });
    }
});

export default cardioExerciseSlice.reducer;
