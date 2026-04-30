import { createAsyncThunk } from '@reduxjs/toolkit';
import type { RootState } from '../store';
import type { CardioLogType, CardioSetPayloadType, ValidationErrorResponse } from '../../interfaces/interfaces';

export const fetchCardioTrainingByDate = createAsyncThunk<
    CardioLogType | null,
    string,
    { state: RootState, rejectValue: ValidationErrorResponse }
>(
    'cardioTraining/fetchByDate',
    async (date, { getState, rejectWithValue }) => {
        const token = getState().auth.accessToken;

        const response = await fetch(`${ process.env.DJANGO_BACKEND_URL }/cardio-trainings/date/${ date }/`, {
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

export const createCardioTraining = createAsyncThunk<
    CardioLogType,
    string,
    { state: RootState, rejectValue: ValidationErrorResponse }
>(
    'cardioTraining/create',
    async (date, { getState, rejectWithValue }) => {
        const token = getState().auth.accessToken;
        const response = await fetch(`${ process.env.DJANGO_BACKEND_URL }/cardio-trainings/`, {
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

export const createCardioSet = createAsyncThunk<
    void,
    { logId: number | null; data: CardioSetPayloadType },
    { state: RootState, rejectValue: ValidationErrorResponse }
>(
    'cardioTraining/createEntry',
    async ({ logId, data }, { getState, dispatch, rejectWithValue }) => {
        const token = getState().auth.accessToken;
        const date = getState().dashboard.activeDate;

        if (logId === null) {
            const createResponse = await fetch(`${ process.env.DJANGO_BACKEND_URL }/cardio-trainings/`, {
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
            const newLog: CardioLogType = await createResponse.json();
            logId = newLog.id;
        }

        const response = await fetch(`${ process.env.DJANGO_BACKEND_URL }/cardio-trainings/${ logId }/sets/`, {
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

        dispatch(fetchCardioTrainingByDate(date));

        return await response.json();
    }
);

export const updateCardioSet = createAsyncThunk<
    void,
    { entryId: number; data: CardioSetPayloadType },
    { state: RootState, rejectValue: ValidationErrorResponse }
>(
    'cardioTraining/updateEntry',
    async ({ entryId, data }, { getState, dispatch, rejectWithValue }) => {
        const token = getState().auth.accessToken;
        const response = await fetch(`${ process.env.DJANGO_BACKEND_URL }/cardio-trainings/sets/${ entryId }/`, {
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
        dispatch(fetchCardioTrainingByDate(date));

        return await response.json();
    }
);

export const deleteCardioSet = createAsyncThunk<
    void,
    { entryId: number },
    { state: RootState, rejectValue: ValidationErrorResponse }
>(
    'cardioTraining/deleteEntry',
    async ({ entryId }, { getState, dispatch, rejectWithValue }) => {
        const token = getState().auth.accessToken;

        const response = await fetch(`${ process.env.DJANGO_BACKEND_URL }/cardio-trainings/sets/${ entryId }/`, {
            method: 'DELETE',
            headers: {
                Authorization: `Bearer ${ token }`
            }
        });

        if (!response.ok) {
            return rejectWithValue(await response.json());
        }

        const date = getState().dashboard.activeDate;
        dispatch(fetchCardioTrainingByDate(date));
    }
);
