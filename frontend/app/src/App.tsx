import { useEffect } from 'react';
import { useDispatch } from 'react-redux';
import type { AppDispatch } from './store/store';
import { bootstrapAuth } from './store/thunks/authThunk';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import LandingPage from './pages/LandingPage.tsx';
import DashboardPage from './pages/DashboardPage.tsx';
import ProfilePage from './pages/ProfilePage.tsx';
import AboutPage from './pages/AboutPage.tsx';
import ProtectedRoute from './components/ProtectedRoute.tsx';
import UnauthenticatedRoute from './components/UnauthenticatedRoute.tsx';

function App() {
    const dispatch = useDispatch<AppDispatch>();

    useEffect(() => {
        dispatch(bootstrapAuth());
    }, [dispatch]);

    return (
        <>
            <BrowserRouter>
                <Routes>
                    <Route path = '/'          element = { <UnauthenticatedRoute><LandingPage /></UnauthenticatedRoute> } />
                    <Route path = '/dashboard' element = { <ProtectedRoute><DashboardPage /></ProtectedRoute> } />
                    <Route path = '/profile'   element = { <ProtectedRoute><ProfilePage /></ProtectedRoute> } />
                    <Route path = '/about'     element = { <AboutPage /> } />
                </Routes>
            </BrowserRouter>
        </>
    );
};

export default App;
