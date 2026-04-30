import { createAsyncThunk } from '@reduxjs/toolkit';
import type { RootState } from '../store';
import type { CardioExerciseType, ValidationErrorResponse } from '../../interfaces/interfaces';

export const fetchAllCardioExercises = createAsyncThunk<
    CardioExerciseType[],
    void,
    { state: RootState, rejectValue: ValidationErrorResponse }
>(
    'cardioExercise/fetchAllCardioExercises',
    async (_, { getState, rejectWithValue }) => {
        const token = getState().auth.accessToken;

        const response = await fetch(`${ process.env.DJANGO_BACKEND_URL }/cardio-exercises/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
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

export const createCardioExercise = createAsyncThunk<
    CardioExerciseType[],
    Omit<CardioExerciseType, 'id'>,
    { state: RootState, rejectValue: ValidationErrorResponse }
>(
    'cardioExercise/create',
    async (data, { getState, rejectWithValue }) => {
        const token = getState().auth.accessToken;

        const response = await fetch(`${ process.env.DJANGO_BACKEND_URL }/cardio-exercises/`, {
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

        const refetchResponse = await fetch(`${ process.env.DJANGO_BACKEND_URL }/cardio-exercises/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${ token }`
            }
        });

        if (!refetchResponse.ok) {
            return rejectWithValue(await refetchResponse.json());
        }

        return await refetchResponse.json();
     }
);
