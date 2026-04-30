import { createAsyncThunk } from '@reduxjs/toolkit';
import type { RootState } from '../store';
import type { FoodLogType, FoodEntryPayloadType, ValidationErrorResponse } from '../../interfaces/interfaces';

export const fetchFoodLogByDate = createAsyncThunk<
    FoodLogType | null,
    string,
    { state: RootState, rejectValue: ValidationErrorResponse }
>(
    'foodLog/fetchByDate',
    async (date, { getState, rejectWithValue }) => {
        const token = getState().auth.accessToken;

        const response = await fetch(`${ process.env.DJANGO_BACKEND_URL }/food-logs/date/${ date }/`, {
            headers: {
                Authorization: `Bearer ${ token }`
            }
        });

        if (response.status === 404) return null;

        if (!response.ok) {
            return rejectWithValue(await response.json());
        }

        return await response.json();
    }
);

export const createFoodLog = createAsyncThunk<
    FoodLogType,
    string,
    { state: RootState, rejectValue: ValidationErrorResponse }
>(
    'foodLog/create',
    async (date, { getState, rejectWithValue }) => {
        const token = getState().auth.accessToken;
        const response = await fetch(`${ process.env.DJANGO_BACKEND_URL }/food-logs/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${ token }`
            },
            body: JSON.stringify({ date })
        });

        if (!response.ok) {
            return rejectWithValue(await response.json());
        }

        return await response.json();
    }
);

export const createFoodEntry = createAsyncThunk<
    void,
    { logId: number | null; data: FoodEntryPayloadType },
    { state: RootState, rejectValue: ValidationErrorResponse }
>(
    'foodLog/createEntry',
    async ({ logId, data }, { getState, dispatch, rejectWithValue }) => {
        const token = getState().auth.accessToken;
        const date = getState().dashboard.activeDate;

        if (logId === null) {
            const createResponse = await fetch(`${ process.env.DJANGO_BACKEND_URL }/food-logs/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${ token }`
                },
                body: JSON.stringify({ date })
            });

            if (!createResponse.ok) {
                return rejectWithValue(await createResponse.json());
            }
            const newLog: FoodLogType = await createResponse.json();
            logId = newLog.id;
        }

        const response = await fetch(`${ process.env.DJANGO_BACKEND_URL }/food-logs/${ logId }/entries/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${ token }`
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            return rejectWithValue(await response.json());
        }

        dispatch(fetchFoodLogByDate(date));

        return await response.json();
    }
);

export const updateFoodEntry = createAsyncThunk<
    void,
    { entryId: number; data: FoodEntryPayloadType },
    { state: RootState, rejectValue: ValidationErrorResponse }
>(
    'foodLog/updateEntry',
    async ({ entryId, data }, { getState, dispatch, rejectWithValue }) => {
        const token = getState().auth.accessToken;
        const response = await fetch(`${ process.env.DJANGO_BACKEND_URL }/food-logs/entries/${ entryId }/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${ token }`
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            return rejectWithValue(await response.json());
        }

        const date = getState().dashboard.activeDate;
        dispatch(fetchFoodLogByDate(date));

        return await response.json();
    }
);

export const deleteFoodEntry = createAsyncThunk<
    void,
    { entryId: number },
    { state: RootState, rejectValue: ValidationErrorResponse }
>(
    'foodLog/deleteEntry',
    async ({ entryId }, { getState, dispatch, rejectWithValue }) => {
        const token = getState().auth.accessToken;

        const response = await fetch(`${ process.env.DJANGO_BACKEND_URL }/food-logs/entries/${ entryId }/`, {
            method: 'DELETE',
            headers: {
                Authorization: `Bearer ${ token }`
            }
        });

        if (!response.ok) {
            return rejectWithValue(await response.json());
        }

        const date = getState().dashboard.activeDate;
        dispatch(fetchFoodLogByDate(date));
    }
);
