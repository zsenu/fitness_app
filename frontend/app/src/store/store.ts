import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice.ts';
import dashboardReducer from './slices/dashboardSlice.ts';
import healthLogReducer from './slices/healthLogSlice.ts';

export const store = configureStore({
    reducer: {
        auth: authReducer,
        dashboard: dashboardReducer,
        healthLog: healthLogReducer
    }
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
