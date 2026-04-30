import { createSlice } from '@reduxjs/toolkit';
import type { StrengthExerciseState } from '../../interfaces/interfaces.ts';
import { fetchAllMuscleGroups, fetchAllStrengthExercises, createStrengthExercise } from '../thunks/strengthExerciseThunk.ts';

const initialState: StrengthExerciseState = {
    muscleGroups: [],
    exercises: [],
    loading: false,
    error: null
};

const strengthExerciseSlice = createSlice({
    name: 'strengthExercise',
    initialState,
    reducers: {},
    extraReducers: (builder) => {
        builder
            .addCase(fetchAllMuscleGroups.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchAllMuscleGroups.fulfilled, (state, action) => {
                state.muscleGroups = action.payload || [];
                state.loading = false;
            })
            .addCase(fetchAllMuscleGroups.rejected, (state, action) => {
                state.error = action.payload || { detail: ['Failed to fetch muscle groups.'] };
                state.loading = false;
            })
            .addCase(fetchAllStrengthExercises.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchAllStrengthExercises.fulfilled, (state, action) => {
                state.exercises = action.payload || [];
                state.loading = false;
            })
            .addCase(fetchAllStrengthExercises.rejected, (state, action) => {
                state.error = action.payload || { detail: ['Failed to fetch strength exercises.'] };
                state.loading = false;
            })
            .addCase(createStrengthExercise.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(createStrengthExercise.fulfilled, (state, action) => {
                state.exercises = action.payload || [];
                state.loading = false;
            })
            .addCase(createStrengthExercise.rejected, (state, action) => {
                state.error = action.payload || { detail: ['Failed to create strength exercise.'] };
                state.loading = false;
            });
    }
});

export default strengthExerciseSlice.reducer;
