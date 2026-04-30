import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice.ts';
import dashboardReducer from './slices/dashboardSlice.ts';
import healthLogReducer from './slices/healthLogSlice.ts';
import foodLogReducer from './slices/foodLogSlice.ts';
import foodItemReducer from './slices/foodItemSlice.ts';
import strengthExerciseReducer from './slices/strengthExerciseSlice.ts';
import strengthTrainingReducer from './slices/strengthTrainingSlice.ts';
import cardioExerciseReducer from './slices/cardioExerciseSlice.ts';
import cardioTrainingReducer from './slices/cardioTrainingSlice.ts';

export const store = configureStore({
    reducer: {
        auth: authReducer,
        dashboard: dashboardReducer,
        healthLog: healthLogReducer,
        foodLog: foodLogReducer,
        foodItem: foodItemReducer,
        strengthExercise: strengthExerciseReducer,
        strengthTraining: strengthTrainingReducer,
        cardioExercise: cardioExerciseReducer,
        cardioTraining: cardioTrainingReducer
    }
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
