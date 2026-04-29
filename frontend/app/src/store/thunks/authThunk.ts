import { createAsyncThunk } from '@reduxjs/toolkit';
import type { RootState } from '../store';
import type { ErrorResponse, ValidationErrorResponse, LoginDataType, RegisterDataType, ProfileDataType } from '../../interfaces/interfaces';

export const fetchUserProfile = createAsyncThunk<
    { profile: ProfileDataType },
    void,
    { rejectValue: ErrorResponse }
>(
    'auth/fetchUserProfile',
    async (
        _,
        thunkAPI
    ) => {
    const state: RootState = thunkAPI.getState() as RootState;
    const token = state.auth.accessToken;
        const response = await fetch(`${ process.env.DJANGO_BACKEND_URL }/profiles/me/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${ token }`
            }
        });

        if (!response.ok) {
            throw new Error('Failed to fetch user profile.');
        }

        const profile: ProfileDataType = await response.json();
        return { profile };
    }
);

export const login = createAsyncThunk<
    { access: string; profile: ProfileDataType }, 
    LoginDataType,
    { rejectValue: ErrorResponse }
>(
    'auth/login',
    async (
        loginData: LoginDataType,
        thunkAPI
    ) => {
        const loginResponse = await fetch(`${ process.env.DJANGO_BACKEND_URL }/auth/login/`, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(loginData)
        });

        if (!loginResponse.ok) {
            const errorData: ErrorResponse = await loginResponse.json();
            return thunkAPI.rejectWithValue(errorData);
        }

        const loginResponseData = await loginResponse.json();
        const token = loginResponseData.access;

        const profileResponse = await fetch(`${ process.env.DJANGO_BACKEND_URL }/profiles/me/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${ token }`
            }
        });

        if (!profileResponse.ok) { throw new Error('Failed to fetch user profile.'); }
        const profileData = await profileResponse.json();

        return { access: token, profile: profileData };
    }
);

export const logout = createAsyncThunk<
    boolean,
    void,
    { rejectValue: string }
>
(
    'auth/logout',
    async (
        _,
        thunkAPI
    ) => {
        const state: RootState = thunkAPI.getState() as RootState;
        const token = state.auth.accessToken;

        const response = await fetch(`${ process.env.DJANGO_BACKEND_URL }/auth/logout/`, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${ token }`
            }
        });

        if (!response.ok) { throw new Error('Logout failed.'); }
        return true;
    }
);

export const register = createAsyncThunk<
    { access: string; profile: ProfileDataType }, 
    RegisterDataType,
    { rejectValue: ValidationErrorResponse | ErrorResponse }
>(
    'auth/registerUser',
    async (
        registerData: RegisterDataType,
        thunkAPI
    ) => {
        const response = await fetch(`${ process.env.DJANGO_BACKEND_URL }/auth/register/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(registerData)
        });

        if (!response.ok) {
            const registerErrorData: ValidationErrorResponse = await response.json();
            return thunkAPI.rejectWithValue(registerErrorData);
        }

        const loginData: LoginDataType = { username: registerData.username, password: registerData.password };
        const loginResponse = await fetch(`${ process.env.DJANGO_BACKEND_URL }/auth/login/`, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(loginData)
        });

        if (!loginResponse.ok) {
            const loginEerrorData: ErrorResponse = await loginResponse.json();
            return thunkAPI.rejectWithValue(loginEerrorData);
        }

        const loginResponseData = await loginResponse.json();
        const token = loginResponseData.access;

        const profileResponse = await fetch(`${ process.env.DJANGO_BACKEND_URL }/profiles/me/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${ token }`
            }
        });

        if (!profileResponse.ok) { throw new Error('Failed to fetch user profile.'); }
        const profileData = await profileResponse.json();

        return { access: token, profile: profileData };
    }
);

export const refreshToken = createAsyncThunk<
    { access: string },
    void,
    { rejectValue: ErrorResponse }
>(
    'auth/refreshToken',
    async (
        _,
        thunkAPI
    ) => {
        const response = await fetch(`${ process.env.DJANGO_BACKEND_URL }/auth/refresh/`, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            return thunkAPI.rejectWithValue({ detail: 'Refresh failed' });
        }

        const data = await response.json();

        return data.access; 
    }
);

export const bootstrapAuth = createAsyncThunk<
    { access: string; profile: ProfileDataType },
    void,
    { rejectValue: ErrorResponse }
>(
    'auth/bootstrap',
    async (_, thunkAPI) => {
        const refreshRes = await fetch(`${ process.env.DJANGO_BACKEND_URL }/auth/refresh/`, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!refreshRes.ok) {
            return thunkAPI.rejectWithValue({ detail: 'No valid session.'});
        }

        const refreshData = await refreshRes.json();
        const token = refreshData.access;

        const profileResponse = await fetch(`${ process.env.DJANGO_BACKEND_URL }/profiles/me/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${token}`
            },
        });

        if (!profileResponse.ok) {
            return thunkAPI.rejectWithValue({ detail: 'Failed to load user' });
        }

        const profile = await profileResponse.json();

        return {
            access: token,
            profile: profile,
        };
    }
);
