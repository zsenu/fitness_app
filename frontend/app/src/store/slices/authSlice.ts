import { createSlice }    from '@reduxjs/toolkit';
import type { AuthState } from '../../interfaces/interfaces';
import { fetchUserProfile, login, logout, register }  from '../thunks/authThunk';

const initialState: AuthState = {
    isAuthenticated: false,
    userProfile:     null,
    accessToken:     null,
    loading:         false,
    error:           null
};

const authSlice = createSlice({
    name: 'auth',
    initialState,
    reducers: { },
    extraReducers: (builder) => {
        builder
            // FETCH USER PROFILE
            .addCase(fetchUserProfile.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchUserProfile.fulfilled, (state, action) => {
                state.loading = false;
                state.userProfile = action.payload.profile;
            })
            .addCase(fetchUserProfile.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload?.detail as string;
            })
            
            // LOGIN
            .addCase(login.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(login.fulfilled, (state, action) => {
                state.loading = false;
                state.isAuthenticated = true;
                state.accessToken = action.payload.access;
                state.userProfile = action.payload.profile;
            })
            .addCase(login.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload?.detail as string;
            })
            
            // LOGOUT
            .addCase(logout.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(logout.fulfilled, (state) => {
                state.loading = false;
                state.isAuthenticated = false;
                state.accessToken = null;
                state.userProfile = null;
            })
            .addCase(logout.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload as string;
            })

            // REGISTER
            .addCase(register.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(register.fulfilled, (state, action) => {
                state.loading = false;
                state.isAuthenticated = true;
                state.accessToken = action.payload.access;
                state.userProfile = action.payload.profile;
            })
            .addCase(register.rejected, (state, action) => {
                state.loading = false;
                state.error = action.payload?.detail as string;
            });
    }
});

export default authSlice.reducer;
