import { createAsyncThunk } from '@reduxjs/toolkit';
import type { RootState } from '../store';
import type { StrengthLogType, StrengthSetPayloadType, ValidationErrorResponse } from '../../interfaces/interfaces';

export const fetchStrengthTrainingByDate = createAsyncThunk<
    StrengthLogType | null,
    string,
    { state: RootState, rejectValue: ValidationErrorResponse }
>(
    'strengthTraining/fetchByDate',
    async (date, { getState, rejectWithValue }) => {
        const token = getState().auth.accessToken;

        const response = await fetch(`${ process.env.DJANGO_BACKEND_URL }/strength-trainings/date/${ date }/`, {
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

export const createStrengthTraining = createAsyncThunk<
    StrengthLogType,
    string,
    { state: RootState, rejectValue: ValidationErrorResponse }
>(
    'strengthTraining/create',
    async (date, { getState, rejectWithValue }) => {
        const token = getState().auth.accessToken;
        const response = await fetch(`${ process.env.DJANGO_BACKEND_URL }/strength-trainings/`, {
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

export const createStrengthSet = createAsyncThunk<
    void,
    { logId: number | null; data: StrengthSetPayloadType },
    { state: RootState, rejectValue: ValidationErrorResponse }
>(
    'strengthTraining/createEntry',
    async ({ logId, data }, { getState, dispatch, rejectWithValue }) => {
        const token = getState().auth.accessToken;
        const date = getState().dashboard.activeDate;

        if (logId === null) {
            const createResponse = await fetch(`${ process.env.DJANGO_BACKEND_URL }/strength-trainings/`, {
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
            const newLog: StrengthLogType = await createResponse.json();
            logId = newLog.id;
        }

        const response = await fetch(`${ process.env.DJANGO_BACKEND_URL }/strength-trainings/${ logId }/sets/`, {
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

        dispatch(fetchStrengthTrainingByDate(date));

        return await response.json();
    }
);

export const updateStrengthSet = createAsyncThunk<
    void,
    { entryId: number; data: StrengthSetPayloadType },
    { state: RootState, rejectValue: ValidationErrorResponse }
>(
    'strengthTraining/updateEntry',
    async ({ entryId, data }, { getState, dispatch, rejectWithValue }) => {
        const token = getState().auth.accessToken;
        const response = await fetch(`${ process.env.DJANGO_BACKEND_URL }/strength-trainings/sets/${ entryId }/`, {
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
        dispatch(fetchStrengthTrainingByDate(date));

        return await response.json();
    }
);

export const deleteStrengthSet = createAsyncThunk<
    void,
    { entryId: number },
    { state: RootState, rejectValue: ValidationErrorResponse }
>(
    'strengthTraining/deleteEntry',
    async ({ entryId }, { getState, dispatch, rejectWithValue }) => {
        const token = getState().auth.accessToken;

        const response = await fetch(`${ process.env.DJANGO_BACKEND_URL }/strength-trainings/sets/${ entryId }/`, {
            method: 'DELETE',
            headers: {
                Authorization: `Bearer ${ token }`
            }
        });

        if (!response.ok) {
            return rejectWithValue(await response.json());
        }

        const date = getState().dashboard.activeDate;
        dispatch(fetchStrengthTrainingByDate(date));
    }
);
