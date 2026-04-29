import { createAsyncThunk } from '@reduxjs/toolkit';
import type { HealthLogType, UpdatePayload, ValidationErrorResponse } from '../../interfaces/interfaces.ts';
import type { RootState } from '../store.ts';

export const fetchHealthLogByDate = createAsyncThunk<
    HealthLogType | null,
    string,
    { rejectValue: ValidationErrorResponse }
>(
    'healthLog/fetchByDate',
    async (date, { getState, rejectWithValue }) => {
        try {
            const state = getState() as RootState;
            const token = state.auth.accessToken;
            if (!token) {
                return rejectWithValue({ non_field_errors: ['No authorization token found.'] });
            }
            const response = await fetch(`${ process.env.DJANGO_BACKEND_URL }/health-logs/date/${date}/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${ token }`
                }
            });

            if (response.status === 404) {
                return null;
            }

            if (!response.ok) {
                throw new Error('Failed to fetch');
            }

            return await response.json();
        } catch (error: unknown) {
            if (error instanceof Error) {
                return rejectWithValue({ non_field_errors: [`Error fetching health log: ${ error.message }`] });
            }
            return rejectWithValue({ non_field_errors: ['Fetch failed'] });
        }
    }
);

export const updateHealthLog = createAsyncThunk<
    HealthLogType,
    UpdatePayload,
    { rejectValue: ValidationErrorResponse }
>(
    'healthLog/update',
    async ({ id, data }, { getState, rejectWithValue }) => {
        try {
            const state = getState() as RootState;
            const token = state.auth.accessToken;
            if (!token) {
                return rejectWithValue({ non_field_errors: ['No authorization token found.'] });
            }
            const response = await fetch(`${ process.env.DJANGO_BACKEND_URL }/health-logs/${id}/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${ token }`
                },
                body: JSON.stringify(data)
            });

            if (response.status === 404) return null;

            if (!response.ok) {
                const errorData = await response.json();
                return rejectWithValue(errorData); 
            }

            return await response.json();
        } catch (error: unknown) {
            if (error instanceof Error) {
                return rejectWithValue({ non_field_errors: [`Error updating health log: ${ error.message }`] });
            }
            return rejectWithValue({ non_field_errors: ['Update failed'] });
        }
    }
);

export const createHealthLog = createAsyncThunk<
    HealthLogType,
    Omit<UpdatePayload, 'id'>,
    { rejectValue: ValidationErrorResponse }
>(
    'healthLog/create',
    async ({ data }, { getState, rejectWithValue }) => {
        try {
            const state = getState() as RootState;
            const token = state.auth.accessToken;
            if (!token) {
                return rejectWithValue({ non_field_errors: ['No authorization token found.'] });
            }
            const response = await fetch(`${ process.env.DJANGO_BACKEND_URL }/health-logs/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${ token }`
                },
                body: JSON.stringify(data)
            });
            
            if (response.status === 404) return null;

            if (!response.ok) {
                const errorData = await response.json();
                return rejectWithValue(errorData); 
            }

            return await response.json();
        } catch (error: unknown) {
            if (error instanceof Error) {
                return rejectWithValue({ non_field_errors: [`Error creating health log: ${ error.message }`] });
            }
            return rejectWithValue({ non_field_errors: ['Creation failed'] });
        }
    }
);