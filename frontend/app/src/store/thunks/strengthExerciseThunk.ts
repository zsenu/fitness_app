import { createAsyncThunk } from '@reduxjs/toolkit';
import type { RootState } from '../store';
import type { MuscleGroupType, StrengthExerciseType, StrengthExercisePayloadType, ValidationErrorResponse } from '../../interfaces/interfaces';

export const fetchAllMuscleGroups = createAsyncThunk<
    MuscleGroupType[],
    void,
    { state: RootState, rejectValue: ValidationErrorResponse }
>(
    'strengthExercise/fetchAllMuscleGroups',
    async (_, { getState, rejectWithValue }) => {
        const token = getState().auth.accessToken;

        const response = await fetch(`${ process.env.DJANGO_BACKEND_URL }/muscle-groups/`, {
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

export const fetchAllStrengthExercises = createAsyncThunk<
    StrengthExerciseType[],
    void,
    { state: RootState, rejectValue: ValidationErrorResponse }
>(
    'strengthExercise/fetchAllStrengthExercises',
    async (_, { getState, rejectWithValue }) => {
        const token = getState().auth.accessToken;

        const response = await fetch(`${ process.env.DJANGO_BACKEND_URL }/strength-exercises/`, {
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

export const createStrengthExercise = createAsyncThunk<
    StrengthExerciseType[],
    StrengthExercisePayloadType,
    { state: RootState, rejectValue: ValidationErrorResponse }
>(
    'strengthExercise/create',
    async (data, { getState, rejectWithValue }) => {
        const token = getState().auth.accessToken;

        const response = await fetch(`${ process.env.DJANGO_BACKEND_URL }/strength-exercises/`, {
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

        const refetchResponse = await fetch(`${ process.env.DJANGO_BACKEND_URL }/strength-exercises/`, {
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
