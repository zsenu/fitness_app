import { BrowserRouter, Routes, Route } from 'react-router-dom';
import LandingPage from './pages/LandingPage.tsx';
import DashboardPage from './pages/DashboardPage.tsx';
import ProfilePage from './pages/ProfilePage.tsx';
import AboutPage from './pages/AboutPage.tsx';
import ProtectedRoute from './components/ProtectedRoute.tsx';

function App() {
    return (
        <>
            <BrowserRouter>
                <Routes>
                    <Route path = '/'          element = { <LandingPage /> } />
                    <Route path = '/dashboard' element = { <ProtectedRoute><DashboardPage /></ProtectedRoute> } />
                    <Route path = '/profile'   element = { <ProtectedRoute><ProfilePage /></ProtectedRoute> } />
                    <Route path = '/about'     element = { <AboutPage /> } />
                </Routes>
            </BrowserRouter>
        </>
    );
};

export default App;
