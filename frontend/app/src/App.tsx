import { BrowserRouter, Routes, Route } from 'react-router-dom';
import LandingPage                      from './pages/LandingPage.tsx';
import DashboardPage                    from './pages/DashboardPage.tsx';
import ProfilePage                      from './pages/ProfilePage.tsx';
import AboutPage                        from './pages/AboutPage.tsx';

function App() {

    return (
        <>
            <BrowserRouter>
                <Routes>
                    <Route path = '/'          element = { <LandingPage />   } />
                    <Route path = '/dashboard' element = { <DashboardPage /> } />
                    <Route path = '/profile'   element = { <ProfilePage /> }   />
                    <Route path = '/about'     element = { <AboutPage /> }     />
                </Routes>
            </BrowserRouter>
        </>
    );
};

export default App;
